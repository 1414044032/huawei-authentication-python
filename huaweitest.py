#coding=utf-8
import json
import requests
import base64
import time

def requestbody(user, passwd, domainname, projectname):
    # 拼接Token
    jsonbody={
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
    jsonbody["auth"]["identity"]["password"]["user"]["name"]=user
    jsonbody["auth"]["identity"]["password"]["user"]["password"]=passwd
    jsonbody["auth"]["identity"]["password"]["user"]["domain"]["name"]=domainname
    jsonbody["auth"]["scope"]["project"]["name"]=projectname
    # print(json.dumps(jsonbody))
    # print(type(json.dumps(jsonbody)))
    return json.dumps(jsonbody)


# 请求鉴权接口，返回有效的加密token
def gettoken(username, domainname, password, regionname):
    bodyrequest = requestbody(username, password, domainname, regionname)
    requesturl = "https://iam.cn-north-1.myhuaweicloud.com/v3/auth/tokens"
    hearder={
        "Content-Type" : "application/json",
    }
    response=requests.post(requesturl,data=bodyrequest,headers=hearder)
    try:
        if response.status_code != 201:
            raise Exception
        token=response.headers.get("X-Subject-Token")
    except Exception as e :
        print("token生成失败。请检查username,password,等等")
    return token


# 上传语音解析任务，返回job_id.这里为长语音的上传地址，短语音请自行查看官方api
def requestbase64(token,fromfile):
    # https://ais.cn-north-1.myhuaweicloud.com/v1.0/voice/asr/sentence     短语音
    requesturl="https://ais.cn-north-1.myhuaweicloud.com/v1.0/voice/asr/long-sentence"
    hearder = {
        "Content-Type": "application/json",
        "X-Auth-Token":token,
    }
    # 对音频文件进行base64加密
    with open(fromfile,'rb') as f:
        bodyrequest=base64.b64encode(f.read()).decode('utf-8')
    data={
           "url" : "",
           "data" : bodyrequest
        }
    try:
        response=requests.post(requesturl, data=json.dumps(data), headers=hearder)
        if response.status_code != 200:
            raise Exception
        # 返回的content为bytes类型，转为str
        print(response.content)
        print(type(response.content))
        result=response.content.decode()
        dictresult=json.loads(result)
    except Exception as e:
        print("请求上传语音失败")
    return dictresult.get("result").get("job_id")

# 长语音请求结果并返回
def requestjob_id(token, job_id):
    requesturl="".join([r"https://ais.cn-north-1.myhuaweicloud.com/v1.0/voice/asr/long-sentence?job_id=",job_id])
    hearder = {
        "Content-Type": "application/json",
        "X-Auth-Token": token,
    }
    response=requests.get(requesturl, headers=hearder);
    code=response.status_code
    response_body=json.loads(response.content.decode())
    if code == 200:
        status_code=int(response_body.get("result").get("status_code"))
        if status_code == 2 :
            result= response_body.get("result").get("words")
            return result
        elif status_code == 0 or status_code == 1:
            return "again"
        elif status_code == -1:
            return None
    return None

if __name__ == "__main__":
    # 目前华为只一个区域支持语音识别 cn-north-1
    token = gettoken('yourusername','yourdomainname','yourpasswd','cn-north-1')
    # 86fb7118-584c-46d8-b5cc-6d0c0dc97866DZLYCH201805301736000001
    job_id = requestbase64(token, r'F:\10.mp3')
    # requestjob_id(token,"86fb7118-584c-46d8-b5cc-6d0c0dc97866DZLYCH201805301736000001")
    while True:
        words=requestjob_id(token, job_id)
        if words:
            if words == "again":
                time.sleep(1)
                continue
            else :
                print(words)
                break
        else:
            print("解析失败")
