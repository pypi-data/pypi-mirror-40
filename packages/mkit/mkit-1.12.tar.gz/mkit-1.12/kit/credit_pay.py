from datetime import datetime

from kit.dingding.notify import get_access_token, get_dept_member, get_user, send_text_to_users
from kit.util import properties


def main():
    now = datetime.now()
    mon = now.strftime('%m')
    day = now.strftime('%d')

    if day == config.remind_day:
        remind(config.remind_text)

    for credit in config.credits:
        if int(day) == int(credit) - 1:
            remind(config.send_text.format(mon, day, config.credits[credit]))


def remind(text):
    token = get_access_token()
    all_user_ids = get_dept_member(token)
    for user_id in all_user_ids:
        user = get_user(token, user_id)
        props = properties.mkit()
        if props.get("test_send") == 'true':
            users = config.test_users
        else:
            users = config.users
        if users.__contains__(user['name']):
            send_text_to_users(token, user['userid'], text)


class config(object):
    # 还款日

    credits = {20: "信用卡(车位贷)", 22: "房贷"}

    send_text = "媳妇儿，明天({0}月{1}日)就是{2}还款日,记得提前还款哦!\n"

    remind_day = 11

    remind_text = "媳妇儿，记得提前还信用卡哦。"

    users = ["刘金玲", "金玲"]
    test_users = ["卢秦"]

