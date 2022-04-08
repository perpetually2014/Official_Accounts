# -*-coding:utf-8-*-
import json
import requests

# 钉钉报警机器人
import config


def sendmessage(message):
    url = 'https://oapi.dingtalk.com/robot/send'  # 这里填写你自定义机器人的webhook地址
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8"
    }
    String_textMsg = {
        "msgtype": "text",
        "text": {"content": message},
        "at": {
            "atMobiles": [
                config.phone_number,
                # 如果需要@某人，这里写他的手机号
            ],
            "isAtAll": 0  # 如果需要@所有人，这里写1
        }
    }
    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(url, data=String_textMsg, headers=HEADERS)
    return res


if __name__ == '__main__':
    pass
    # message = "三农资讯：微信账号 {}cookie过期了，请登录"
    # sendmessage(message)

