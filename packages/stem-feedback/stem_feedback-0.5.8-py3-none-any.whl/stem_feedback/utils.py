import json


def get_json_event(feed_back_type, subject, message, customer_id, customer_erp_id,
                   customer_name, user_id, user_name, email):
    json_str = dict()
    json_str['type'] = str(feed_back_type)
    json_str['subject'] = str(subject)
    json_str['message'] = str(message)
    cust = {"customer_id": customer_id, "customer_erp_id": customer_erp_id, "customer_name": customer_name}
    usr = {"user_id": user_id, "user_name": user_name, "email": email, "customer": cust}
    json_str['user'] = usr
    return str(json_str)


def get_json_notification(feed_back_type, payment_type, subject, message, sum, currency_iso_id, currency_abbr,
                          customer_id, customer_erp_id, customer_name, user_id, user_name, email):
    json_str = dict()
    json_str['type'] = str(feed_back_type)
    json_str['subject'] = str(subject)
    json_str['message'] = str(message)
    cust = {"customer_id": customer_id, "customer_erp_id": customer_erp_id, "customer_name": customer_name}
    usr = {"user_id": user_id, "user_name": user_name, "email": email, "customer": cust}
    json_str['user'] = usr
    cur = {
            'iso_id': currency_iso_id.encode("utf-8"),
            'abbr': currency_abbr,
        }
    json_str['doc'] = {
        'payment_for': payment_type,
        'sum': sum,
        'currency': cur}
    return str(json_str)


def get_json_moneyback(feed_back_type, subject, message,
                       customer_id, customer_erp_id, customer_name, user_id, user_name, email, doc_number,
                       doc_date, reason, ship, tracking_number, attachments, products):
    json_str = dict()
    json_str['type'] = str(feed_back_type)
    json_str['subject'] = str(subject)
    json_str['message'] = str(message)
    cust = {"customer_id": customer_id, "customer_erp_id": customer_erp_id, "customer_name": customer_name}
    usr = {"user_id": user_id, "user_name": user_name, "email": email, "customer": cust}
    json_str['user'] = usr
    json_str['doc'] = {
        'type': 'РН',
        'number': doc_number,
        'date': doc_date},

    json_str['reason'] = reason,
    json_str['ship'] = ship,
    json_str['tracking_number'] = tracking_number
    for item in attachments:
        name = item['name'],
        url = item['url'],
    attachments = {"name": name, "url": url}
    json_str['attachments'] = attachments
    for item in products:
        row_num = item['row_num'],
        name = item['name'],
        article = item['article'],
        brand = item['brand'],
        price = item['price'],
        invoice_qty = item['invoice_qty'],
        return_qty = item['return_qty']

    products = {"row_num": row_num, "name": name, "article": article, "brand": brand, "price": price,
                "invoice_qty": invoice_qty, "return_qty": return_qty}
    json_str['products'] = products
