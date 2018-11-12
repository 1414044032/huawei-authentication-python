# -*- coding: utf-8 -*-

import json
import requests

class ProduceToken:

    def __init__(self,user, passwd, domainname, projectname):
        self.user = user
        self.passwd = passwd
        self.domainname = domainname
        self.projectname = projectname

    def SendBody(self):
        # 拼接Token
        jsonbody = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "name": "username",  # 用户名
                            "password": "password",  # 密码
                            "domain": {
                                "name": "domainname"  # 账户名
                            }
                        }
                    }
                },
                "scope": {
                    "project": {
                        "name": "cn-north-1"  # 语音识别所属区域为“华北-北京一”，默认项目名为“cn-north-1”
                    }
                }
            }
        }
        # 结构太多很容易错。可以在线网站分层查看 http://tool.oschina.net/codeformat/json
        jsonbody["auth"]["identity"]["password"]["user"]["name"] = self.user
        jsonbody["auth"]["identity"]["password"]["user"]["password"] = self.passwd
        jsonbody["auth"]["identity"]["password"]["user"]["domain"]["name"] = self.domainname
        jsonbody["auth"]["scope"]["project"]["name"] = self.projectname
        return json.dumps(jsonbody)

    def GetToken(self):
        bodyrequest = self.SendBody()
        requesturl = "https://iam.cn-north-1.myhuaweicloud.com/v3/auth/tokens"
        hearder = {
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(requesturl, data=bodyrequest, headers=hearder)
            if response.status_code != 201:
                raise Exception
            token = response.headers.get("X-Subject-Token")
        except Exception as e:
            print("token生成失败。请检查username,password,等等")
            return None
        return token

