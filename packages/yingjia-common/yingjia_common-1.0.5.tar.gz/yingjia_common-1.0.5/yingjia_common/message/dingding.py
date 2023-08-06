# codeing=utf-8

# https://oapi.dingtalk.com/robot/send?access_token=dc50105a25f58a4d490e37599d14134c85cf8e3f5e220f67616cca453bf9de37

import json
import urllib.request
from datetime import datetime


def send_msg(content):
    # 1、构建url
    url = "https://oapi.dingtalk.com/robot/send?access_token=dc50105a25f58a4d490e37599d14134c85cf8e3f5e220f67616cca453bf9de37"  # url为机器人的webhook
    # 2、构建一下请求头部
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    # 3、构建请求数据
    data = {
        "msgtype": "text",
        "text": {
            "content": str(content)
        },
        "at": {
            "isAtAll": False  # @全体成员（在此可设置@特定某人）
        }
    }
    # 4、对请求的数据进行json封装
    sendData = json.dumps(data)  # 将字典类型数据转化为json格式
    sendData = sendData.encode("utf-8")  # python3的Request要求data为byte类型
    # 5、发送请求
    request = urllib.request.Request(url=url, data=sendData, headers=header)
    # 6、将请求发回的数据构建成为文件格式
    opener = urllib.request.urlopen(request)
    # 7、打印返回的结果
    r = opener.read()  # b'{"errmsg":"ok","errcode":0}'
    return r


def is_worktime():
    '''
    周一到周五，9-17点发钉钉消息
    :return:
    '''
    r = False
    now = datetime.now()
    if now.weekday() >= 0 and now.weekday() <= 4:
        if now.hour >= 9 and now.hour < 17:
            r = True
    return r


def send_msg_worktime(content):
    '''
    工作时间发消息
    :return:
    '''
    if (is_worktime() == True):
        send_msg(content)


if __name__ == '__main__':
    send_msg('这是个测试消息[x]:d,，“”xxx')
