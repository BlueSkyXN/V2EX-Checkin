import requests, json, time, os, re, sys
sys.path.append('.')
requests.packages.urllib3.disable_warnings()
try:
    from pusher import pusher
except:
    pass

cookie = os.environ.get("cookie_v2ex")

def run(*arg):
    msg = ""
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'})

    # 获取签到的once
    url = "https://www.v2ex.com/mission/daily"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding' : 'gzip, deflate, br',
        'accept-language' : 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Cookie': cookie
    }
    r = s.get(url, headers=headers, verify=False, timeout=120)
    # print(r.text)
    if '需要先登录' in r.text:
        msg = "cookie失效啦！！！！\n"
        pusher("V2EX  Cookie失效啦！！！", r.text[:200])
        return msg
    elif '每日登录奖励已领取' in r.text:
        msg = '今天已经签到过啦！！！\n'
        return msg
    once = re.compile(r'once\=\d+').search(r.text)
    # print(once[0])

    # 签到
    sign_url = f"https://www.v2ex.com/mission/daily/redeem?{once[0]}"
    sign = s.get(sign_url, headers=headers, verify=False, timeout=120)
    # 获取签到情况
    r = s.get(url, headers=headers, verify=False)
    if '每日登录奖励已领取' in r.text:
        msg += '签到成功！'
        # 查看获取到的数量
        check_url = 'https://www.v2ex.com/balance'
        r = s.get(check_url, headers=headers, verify=False, timeout=120)
        data = re.compile(r'\d+?\s的每日登录奖励\s\d+\s铜币').search(r.text)
        msg += data[0] + '\n'
    elif '登录' in sign.text:
        msg = "cookie失效啦！！！！\n"
        pusher("V2EX  Cookie失效啦！！！")
        return msg
    else:
        msg = '签到失败！\n'
        pusher("V2EX  签到失败！！！", sign.text[:200])
    return msg

def main(*arg):
    msg = ""
    global cookie
    if "\\n" in cookie:
        clist = cookie.split("\\n")
    else:
        clist = cookie.split("\n")
    i = 0
    while i < len(clist):
        msg += f"第 {i+1} 个账号开始执行任务\n"
        cookie = clist[i]
        msg += run(cookie)
        i += 1
    print(msg[:-1])
    return msg[:-1]


if __name__ == "__main__":
    if cookie:
        print("----------V2EX开始尝试签到----------")
        main()
        print("----------V2EX签到执行完毕----------")
