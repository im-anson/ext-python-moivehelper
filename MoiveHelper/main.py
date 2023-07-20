import sys
import json
from websocket import WebSocketApp
import configparser
import requests
import re



def extract_first_url(string):
    pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    url = re.search(pattern, string)
    if url:
        return url.group()
    else:
        return None

def check_video_platform(string):
    keywords = ['youku', 'iqiyi', 'v.qq', 'mgtv', 'pptv', 'miguvideo', 'sohu', 'le', '1905', 'bilibili', 'wasu', 'ixigua']
    return any(keyword in string for keyword in keywords)
    
def on_message(ws:WebSocketApp,msg):
    msg = json.loads(msg)
    
    if msg['type']==1:
        # 测试示例
        first_url = extract_first_url(msg['data']['msg'])
        if first_url:
            if check_video_platform(first_url):
                response = requests.get("https://json.nxflv.com/?uid=47687618&key=imorsxzBDIJLNUW247&url="+first_url)
                data = response.json()
                if data['code'] == 200:
                    ws.send(json.dumps({"method": "sendText","wxid": msg['data']['fromid'],"msg": "资源已找到，请点击链接或者复制到浏览器打开"+data['url'],"pid": 0}))
                else:
                    ws.send(json.dumps({"method": "sendText","wxid": msg['data']['fromid'],"msg": "未找到相关资源","pid": 0}))

def on_open(ws):
    
    data = sys.argv
    key = data[data.index('--key') + 1]
    ws.send(json.dumps({
            "method": "sendText",
            "wxid": "filehelper",
            "msg": "影视助手已启动",
            "atid": "",
            "pid": 0
        }))
    

if __name__ == "__main__":
    data = sys.argv
    name = data[data.index('--name') + 1]
    key = data[data.index('--key') + 1]
    url = "ws://127.0.0.1:8202/wx?name=" + name + "&key=" + key
    ws = WebSocketApp(url=url,on_message=on_message,on_open=on_open)
    ws.run_forever()
