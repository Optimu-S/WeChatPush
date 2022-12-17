from itchat.config import PHONE_TYPE
from itchat.config import PUSH_REGID
from itchat.config import BLOCK_NAME
from itchat.config import MES_THROUGH
from itchat.config import WEBHOOK_URL
import requests
import socket
import json

farpush_url = "http://124.70.44.216:9090"

config_path = './src/config.json'

# 飞书报文信息
with open(config_path, 'r') as f:
    configs = json.load(f)


class farpush:
    def __init__(self):
        self.regid = PUSH_REGID
        self.phone = PHONE_TYPE
        self.block = BLOCK_NAME
        self.through = MES_THROUGH
        self.webhook_url = WEBHOOK_URL
        self.msg_headers = configs['msg_headers']
        self.msg_content = configs['msg_content']

    def push(self, title, content):
        # block name
        if PHONE_TYPE != 5 :
            for check in self.block:
                if check in title:
                    return
            data = {
                "content": content,
                "title": title,
                "regID": self.regid,
                'phone': self.phone,
                'through': self.through
            }
            headers = {'content-type': 'application/json'}
            r = requests.post(farpush_url + '/PushWeChatMes', data)
        else :
            for check in self.block:
                if check in title:
                    return
            self.title = title
            self.content = content
            self.webhook_notice()

    def mediapush(self, title, content, filename):
        if PHONE_TYPE != 5 :
            for check in self.block:
                if check in title:
                    return
            data = {
                "content": content,
                "title": title,
                "regID": self.regid,
                'phone': self.phone,
                'through': self.through
            }
            resource = {"filename": filename}
            data['resource'] = json.dumps(resource)
            headers = {'content-type': 'application/json'}
            r = requests.post(farpush_url + '/PushWeChatMes', data)
        else :
            for check in self.block:
                if check in title:
                    return
            self.title = title
            self.content = content
            self.webhook_notice()

    def webhook_notice(self):
        """
        飞书通知
        :param text: 微信新消息提醒
        :return: None
        """
        self.msg_content["card"]["header"]["title"]["content"] = self.title + "：" + self.content
        # self.msg_content["card"]["elements"][0]["text"]["content"] = self.content
        self.msg_content["card"]["elements"][0]["text"]["content"] = "请打开微信回复。"

        res = requests.post(self.webhook_url, json.dumps(self.msg_content), headers=self.msg_headers)
