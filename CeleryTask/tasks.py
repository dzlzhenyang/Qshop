from __future__ import absolute_import
from Qshop.celery import app


@app.task  # 将普通函数转换为celery任务
def add(x, y):
    return x + y


import json
import requests
from Qshop.settings import DING_URL


# 使用钉钉发送信息
@app.task
def ding_send_message(content="hello", to="18737616537"):
    headers = {
        "Content-Type": "application/json",
        "Charset": "utf-8"
    }
    request_data = {
        "msgtype": "text",
        "text": {"content": content},
        "at": {"atMobiles": [""], "isAtAll": True}
    }
    if to:
        request_data["at"]["atMobiles"].append(to)
        request_data["at"]["isAtAll"] = False
    else:
        request_data["at"]["atMobiles"].clear()
        request_data["at"]["isAtAll"] = True
    #  将数据转换为json的字符串格式
    send_data = json.dumps(request_data)
    response = requests.post(url=DING_URL, headers=headers, data=send_data)
    # 将结果转换为json格式
    content = response.json()
    return content
