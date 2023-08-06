import datetime
import os
import re
import time

import requests
import json

from kit.dingding.notify import get_access_token, get_dept_member, get_user, send_text_to_users
from kit.util import properties
from mizlicai import new_product_url, unique_id, recommend, total_amount, sold_amount, rate, status, name, term
from kit.db.db_helper import insert, query
from mizlicai.model import Product


def check_new_product(conn):
    result = requests.get(new_product_url)
    jsonObj = json.loads(result.text, encoding='utf-8')
    products = jsonObj['normalProductOnsell']
    token = get_access_token()

    props = properties.mkit()
    send_to_names = re.split(r',\s*', props.get('send_to'))
    miz_test_send_str = props.get('miz_test_send')
    miz_test_send = miz_test_send_str.lower() == 'true'

    for product in products:
        lastProduct = Product()
        lastProduct.id = product[unique_id]
        lastProduct.recommend = product[recommend]
        lastProduct.amount = int(product[total_amount]) - int(product[sold_amount])
        lastProduct.rate = float(product[rate])
        lastProduct.status = product[status]
        lastProduct.name = product[name]
        lastProduct.term = product[term]
        has_notify = False
        all_user_ids = get_dept_member(token)
        if query(lastProduct, conn) is None:
            if insert(lastProduct, conn):
                for user_id in all_user_ids:
                    user = get_user(token, user_id)
                    if user['name'] in send_to_names:
                        print("send message to user: %s" % user['name'])
                        print("meessage:")
                        print(lastProduct.__str__())
                        send_text_to_users(token, user['userid'], lastProduct.__str__())
                has_notify = True
        if not has_notify and miz_test_send:
            for user_id in get_dept_member(token):
                user = get_user(token, user_id)
                if user['name'] in send_to_names:
                    send_text_to_users(token, user['userid'], time.time())
                    print("send empty message to user: %s" % user['name'])
            pass
