import time

import requests
import re

def push(coinNum):
    token = "" #如果需要通知到微信的话，自行去pushplus.hxtrip.com获取token填到前面的引号里；不需要的话，可以空着
    requests.get(f"http://pushplus.hxtrip.com/send?token={token}&title=安徽创业云平台 - 金币领取成功&content=当前剩余可领取金币数为：{coinNum}&template=html")

cookies = {
    'ASP.NET_SessionId': '',
    'token': '',
    'SSID': '',
    'UM_distinctid': '',
    'CNZZDATA1262121790': '',
}# 自行在上面五个参数里填上自己的信息，获取方式通过网页登陆后点击F12获取

# 具体获取Cookies的方式，后续我会留一个教程，请持续关注项目Markdown文档。

while True:
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://www.ahcy.gov.cn/Member/ChuangYeQuan/ApplyCyqGuide',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    response = requests.get('https://www.ahcy.gov.cn/Member/ChuangYeQuan/ApplyVouchersPer/1ddb5d1035684c5982f902d51b6a41d8', headers=headers, cookies=cookies)
    enableCoin = re.findall('<span class="f_ora"><b id="applyBalance" class="size24">(.*?)</b>',response.text)
    coin = -1
    if(len(enableCoin)>0):
        coin = int(enableCoin[0])
    if(coin==0 or coin==-1):
        time.sleep(10)
        continue
    print("当前金币数：",coin)


    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://www.ahcy.gov.cn',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.ahcy.gov.cn/Member/ChuangYeQuan/ApplyVouchersPer/1ddb5d1035684c5982f902d51b6a41d8', #下面说的是这个
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    data = {
      'type': 'Local',# 虽然写的是金币类型，但是我测试了三种类型，均显示Local，所以这个参数不知道有什么用，具体请自行分析，个人推断根据上面headers里的Referer来判断
      'money': '2000',# 金币数量，按自己额度填写，太多了领取不了
      'quKey': ''
    }

    response = requests.post('https://www.ahcy.gov.cn/Member/ChuangYeQuan/GetCyqApplyPerRule', headers=headers, cookies=cookies, data=data)
    if(response.json().get("status") == True):
        push(str(coin-2000))
        break
    else:
        push("有额度，但是领取失败，请自行操作！！")