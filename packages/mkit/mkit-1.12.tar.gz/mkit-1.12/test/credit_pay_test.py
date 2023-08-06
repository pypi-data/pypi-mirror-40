from datetime import time, datetime

from kit import credit_pay
from kit.credit_pay import remind, config


def test_remind_days():
    now = datetime.now()
    mon = now.strftime('%m')
    day = now.strftime('%d')

    if day == config.remind_day:
        remind(config.remind_text)

    for credit in config.credits:
        if int(day) == int(credit) - 1:
            remind(config.send_text.format(mon, day, config.credits[credit]))


test_remind_days()
