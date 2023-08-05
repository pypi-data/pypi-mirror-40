from django.forms.fields import CharField
from stem_feedback.models import *
from django import forms
from django.utils.translation import ugettext as _
from stem_feedback.middleware import current_user


class FeedbackEmailForm(forms.ModelForm):
    from_email = forms.EmailField(required=True, label=_('Ваш email'))
    subject = CharField(max_length=30, required=False, label=_("Тема обращения"))
    type = forms.ModelChoiceField(queryset=FeedBackType.objects.all(),
                                            required=False,
                                            label=_('Тип обращения'))
    message = forms.CharField(widget=forms.Textarea, required=True, label=_('Текст'))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if self.user !='':
            self.fields['from_email'] = forms.EmailField(
                required=False,
                widget=forms.HiddenInput(),
            )

    class Meta:
        model = Feedback
        fields = (
            'from_email',
            'subject',
            'type',
            'message',
        )


SETTLEMENT_ACCOUNT = 'settlement_account'
CARD_ACCOUNT = 'card_account'
COURIER = 'courier'
PAYMENT_CHOICES = (
    (SETTLEMENT_ACCOUNT, 'Расчетный счет'),
    (CARD_ACCOUNT, 'Карточный счет'),
    (COURIER, 'Курьер'),
)


class PaymentNotificationForm(forms.Form):
    type = forms.ModelChoiceField(queryset=FeedBackType.objects.all(),
                                  required=False,
                                  label=_('Тип обращения'))
    payment_type = forms.ChoiceField(choices=PAYMENT_CHOICES,
                                     widget=forms.RadioSelect(), label=_("Форма оплаты"))
    sum = forms.CharField(max_length=255, required=False, label=_("Сумма"))

    currency = forms.ChoiceField(required=False,
                                 choices=[],
                                 widget=forms.Select,
                                 label=_('Валюта'))

    customer = forms.ChoiceField(
        required=False,
        choices=[],
        widget=forms.Select,
        label=_('Покупатель'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial = kwargs.get('initial', False)
        if initial:
            self.fields['customer'].choices = initial.get('customers', [])
            self.fields['currency'].choices = initial.get('currency', [])


DEFECT = 'Брак'
DAMAGED = 'Не соответствует артикулу/поврежден'
RETAINED = 'Не забрал клиент'
REFUSAL = 'Отказ клиента'
ERROR_CLIENT = 'Ошибка клиента'
ERROR_OF_SELECTION = 'Ошибка при подборе'

MONEYBACK_CHOICES = (
    (DEFECT, 'Брак'),
    (DAMAGED, 'Не соответствует артикулу/поврежден'),
    (RETAINED, 'Не забрал клиент'),
    (REFUSAL, 'Отказ клиента'),
    (ERROR_CLIENT, 'Ошибка клиента'),
    (ERROR_OF_SELECTION, 'Ошибка при подборе'),
)


class MoneyBackForm(forms.Form):

    # row_num = forms.IntegerField(min_value=1, label='Номер строки в накладной')
    comment = forms.CharField(widget=forms.Textarea, required=False, label=_("Комментарий"))
    tracking_number = forms.CharField(max_length=255, required=False, label=_("Номер декларации"))

    reason_for_the_return = forms.ChoiceField(
        required=False,
        choices=MONEYBACK_CHOICES,
        widget=forms.Select,
        label=_('Причина возврата'))

    ship = forms.ChoiceField(
        required=False,
        choices=[],
        widget=forms.Select,
        label=_('Доставка'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial = kwargs.get('initial', False)
        if initial:
            self.fields['ship'].choices = initial.get('ships', [])

class OrdersForm(forms.Form):
    name = forms.CharField(max_length=255, required=False, label=_("Наименование"))
    quantity =  forms.DecimalField(max_digits=15, decimal_places=3,initial=1, label='Количество товара в накладной')
    return_qty = forms.DecimalField(max_digits=15, decimal_places=3,initial=0, label='Возврат')

