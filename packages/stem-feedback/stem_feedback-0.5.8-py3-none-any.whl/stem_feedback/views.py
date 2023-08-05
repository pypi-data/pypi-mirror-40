from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import *
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
import os.path
import datetime
import stem_feedback.utils


class FeedbackEmailView(View):
    data = None

    def get(self, request):
        form = FeedbackEmailForm(user=request.user.id)
        return render(request, "feedback.html", {'form': form})

    def post(self, request, *args, **kwargs):
        form = FeedbackEmailForm(request.POST, user=request.user.id)
        if form.is_valid():
            feed_back_type = form.cleaned_data['type']
            subject = 'Feedback.' + form.cleaned_data['subject']
            message = form.cleaned_data['message']

            if request.user.is_active:
                user_name = request.user.username
                from_email = request.user.email
                templ = dict({'user': user_name,
                              'email': from_email,
                              'type': feed_back_type,
                              'subject': subject,
                              'text': message,
                              })

            else:
                from_email = form.cleaned_data['from_email']
                templ = dict({
                    'email': from_email,
                    'type': feed_back_type,
                    'subject': subject,
                    'text': message,
                })

            if args:
                customer_id = args[0]['customer_id']
                customer_erp_id = args[0]['customer_erp_id']
                customer_name = args[0]['customer_name']
            else:
                customer_id = ''
                customer_erp_id = ''
                customer_name = ''

            html = get_template('html-message.html')
            html_content = html.render(templ)
            try:
                if feed_back_type:

                    user_name = request.user.username
                    user_id = request.user.id
                    res = stem_feedback.utils.get_json_event(feed_back_type, subject, message, customer_id,
                                                             customer_erp_id, customer_name, user_id, user_name,
                                                             from_email)

                    f_name = str(customer_name + str(feed_back_type) + str(
                        datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")))
                    fs = 'files_media/' + f_name
                    os.mkdir(fs)
                    with open(fs + '/' + f_name + '.json', 'w') as json_f:
                        json_f.write(res)
                        json_f.close()
                    to_email = FeedBackType.objects.get(name=feed_back_type).email
                    msg = EmailMultiAlternatives(subject, message, from_email, [to_email])
                    msg.attach_alternative(html_content, "text/html")
                    for afile in request.FILES.getlist('sentFile'):
                        os.path.join(fs, afile)
                    os.path.join(fs, json_f.name)
                    direc = os.listdir(fs)
                    for i in direc:
                        msg.attach_file(fs+'/'+i)
                        msg.send()
                else:
                    to_email = settings.CONST_EMAIL
                    send_mail(subject, message, from_email, [to_email], html_message=html_content)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request, 'email_complete.html')
        return render(request, "feedback.html", {'form': form})


class PaymentNotificationView(View):

    def get(self, request, *args, **kwargs):

        curr = kwargs.get('currency', [])
        cust = kwargs.get('customers', [])

        dd = [pair for pair in enumerate(cust.keys())]
        ff = [pair for pair in enumerate(curr.keys())]

        form = PaymentNotificationForm(initial={'customers': dd, 'currency': ff})
        return render(request, "payment_notification.html", {'form': form})

    def post(self, request, *args, **kwargs):
        curr = kwargs.get('currency', [])
        cust = kwargs.get('customers')

        dd = [pair for pair in enumerate(cust.keys())]
        ff = [pair for pair in enumerate(curr.keys())]

        form = PaymentNotificationForm(
            request.POST, initial={
                'customers': dd, 'currency': ff,
            }
        )

        if form.is_valid():

            feed_back_type = form.cleaned_data['type']
            payment_type = form.cleaned_data['payment_type']
            sum = form.cleaned_data['sum']

            currency_index = int(form.cleaned_data['currency'])
            customer_index = int(form.cleaned_data['customer'])

            customer_name = dd[customer_index][1]
            customer_id = cust[customer_name][0]
            if cust[customer_name][1]:
                customer_erp_id = cust[customer_name][1]
            else:
                customer_erp_id = ''
            currency_name = ff[currency_index][1]
            currency_iso_id = curr[currency_name][1]
            currency_abbr = curr[currency_name][0]

            subject = 'Сообщение об оплате.' + customer_name + '.' + sum + currency_abbr
            user_name = request.user.username
            user_id = request.user.id
            from_email = request.user.email

            message = str('Дата:' + str(datetime.datetime.today()) + ',' + 'Пользователь:' + user_name + ','
                          + 'Клиент:' + customer_name + ',' + 'Тип оплаты:' + payment_type + ',' + 'Сумма:' +
                          str(sum + currency_abbr))
            templ = dict({'email': from_email,
                          'message': message})

            html = get_template('html-notification.html')
            html_content = html.render(templ)
            try:
                res = stem_feedback.utils.get_json_notification(feed_back_type, subject, payment_type, message, sum,
                                                                currency_iso_id,
                                                                currency_abbr, customer_id, customer_erp_id,
                                                                customer_name,
                                                                user_id, user_name, from_email)

                f_name = str(
                    customer_name + str(feed_back_type) + str(datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")))
                fs = 'files_media/' + f_name
                os.mkdir(fs)
                with open(fs + '/' + f_name + '.json', 'w') as json_f:
                    json_f.write(res)
                    json_f.close()
                to_email = FeedBackType.objects.get(name=feed_back_type).email

                msg = EmailMultiAlternatives(subject, message, from_email, [to_email])
                msg.attach_alternative(html_content, "text/html")
                for afile in request.FILES.getlist('sentFile'):
                    os.path.join(fs, afile)
                os.path.join(fs, json_f.name)
                direc = os.listdir(fs)
                for i in direc:
                    msg.attach_file(fs + '/' + i)
                    msg.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request, 'email_complete.html')
        return render(request, "payment_notification.html", {'form': form})


class MoneyBackView(View):

    def get(self, request, *args, **kwargs):
        form = MoneyBackForm()
        return render(request, "moneyback.html", {'form': form})


