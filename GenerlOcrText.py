# -*- coding: utf-8 -*-

from huawei.ProduceToken import ProduceToken
import base64
import requests
import json

class Img2Text:

    @staticmethod
    def requestOcrCustomsFormEnBase64(fromfile):
        Token = ProduceToken("your","your","your","cn-north-1").GetToken()
        # 通用文字识别接口
        requestUrl = "https://ais.cn-north-1.myhuaweicloud.com/v1.0/ocr/general-text"
        header = {
            "Content-Type": "application/json",
            "X-Auth-Token": Token,
        }
        with open(fromfile, 'rb') as f:
            bodyrequest = base64.b64encode(f.read()).decode('utf-8')
        data = {
         "image":bodyrequest,
         "url":"",
         "detect_direction":False
          }
        try:
            response = requests.post(requestUrl, data=json.dumps(data), headers=header)
            if response.status_code != 200:
                raise Exception
            # 返回的content为bytes类型，转为str
            result = response.content.decode()
            dictresult = json.loads(result)
            print(dictresult)
        except Exception as e:
            print("请求文字识别")
            return None
        return dictresult

if __name__ == "__main__":
    Img2Text.requestOcrCustomsFormEnBase64("C:\\Users\\14140\\Desktop\\V2Txt\\dabao\\img8.jpg")
