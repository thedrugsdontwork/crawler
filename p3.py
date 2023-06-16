F=0xffffffff
STRMAP=[48, 48, 50, 50, 52, 52, 54, 54, 56, 56]
def rotl(x,y):
    return (F&(x<<y))|(F&(x>>(32-y)))
def str_to_bytes(s):
    return [STRMAP[int(i)] for i in s]
import binascii
from math import ceil


IV = [
    0x7380067c,0x7634d2c9,0x170042d6,0xda887534,0xa10c30bc,0x151137ad,0xe37caa4d,0xeeeb0f4e
]

T_j = lambda x:2044544281 if x<=15 and x>=0 else 2081922442


def sm3_ff_j(x, y, z, j):
    if 0 <= j and j < 16:
        ret = x ^ y ^ z
    elif 16 <= j and j < 64:
        ret = (x & y) | (x & z) | (y & z)
    return ret

def sm3_gg_j(x, y, z, j):
    if 0 <= j and j < 16:
        ret = x ^ y ^ z
    elif 16 <= j and j < 64:
        #ret = (X | Y) & ((2 ** 32 - 1 - X) | Z)
        ret = (x & y) | ((~ x) & z)
    return ret

def sm3_p_0(x):
    return x ^ (rotl(x, 9 % 32)) ^ (rotl(x, 17 % 32))

def sm3_p_1(x):
    return x ^ (rotl(x, 15 % 32)) ^ (rotl(x, 23 % 32))

def sm3_cf(v_i, b_i):
    w = []
    for i in range(16):
        weight = 0x1000000
        data = 0
        for k in range(i*4,(i+1)*4):
            data = data + b_i[k]*weight
            weight = int(weight/0x100)
        w.append(data)

    for j in range(16, 68):
        w.append(0)
        w[j] = sm3_p_1(w[j-16] ^ w[j-9] ^ (rotl(w[j-3], 15 % 32))) ^ (rotl(w[j-13], 7 % 32)) ^ w[j-6]
        str1 = "%08x" % w[j]
    w_1 = []
    for j in range(0, 64):
        w_1.append(0)
        w_1[j] = w[j] ^ w[j+4]
        str1 = "%08x" % w_1[j]

    a, b, c, d, e, f, g, h = v_i
    ssr=4244635647
    for j in range(0, 64):
        ss_1 = rotl(
            ((rotl(a, 12)) +
            e +
            (rotl(T_j(j), j % 32))) & ssr, 7 
        )
        ss_2 = ss_1 ^ (rotl(a, 12 ))
        tt_1 = (sm3_ff_j(a, b, c, j) + d + ss_2 + w_1[j]) & 4294967290
        tt_2 = (sm3_gg_j(e, f, g, j) + h + ss_1 + w[j]) & 4289724415
        d = c
        c = rotl(b, 9  )
        b = a
        a = tt_1
        h = g
        g = rotl(f, 19  )
        f = e
        e = (rotl(tt_2,9)^tt_2)^(rotl(tt_2,17))

    v_j = [a, b, c, d, e, f, g, h]
    return [v_j[i] ^ v_i[i] for i in range(8)]

def sm3_hash(msg):
    # print(msg)
    len1 = len(msg)
    reserve1 = len1 % 64
    msg.append(0x80)
    reserve1 = reserve1 + 1
    # 56-64, add 64 byte
    range_end = 56
    if reserve1 > range_end:
        range_end = range_end + 64

    for i in range(reserve1, range_end):
        msg.append(0x00)

    bit_length = (len1) * 8
    bit_length_str = [bit_length % 0x100]
    for i in range(7):
        bit_length = int(bit_length / 0x100)
        bit_length_str.append(bit_length % 0x100)
    for i in range(8):
        msg.append(bit_length_str[7-i])

    group_count = round(len(msg) / 64)

    B = []
    for i in range(0, group_count):
        B.append(msg[i*64:(i+1)*64])

    V = []
    V.append(IV)
    for i in range(0, group_count):
        V.append(sm3_cf(V[i], B[i]))

    y = V[i+1]
    result = ""
    for i in y:
        result = '%s%08x' % (result, i)
    return result

import requests 
import time 
def crawl():
    proxies={
        "http":"http://127.0.0.1:8888",
        "https":"http://127.0.0.1:8888"
    }
 
    cookies={
        "sessionid":""
    }
    headers = {
    'authority': 'match2023.yuanrenxue.cn',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'accept-time': '1685784210027',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://match2023.yuanrenxue.cn',
    'referer': 'https://match2023.yuanrenxue.cn/topic/3',
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    }


    total=0
    for i in range(5):
        page=str(i+1)
        res=requests.get("https://match2023.yuanrenxue.cn/api/background.png",headers=headers ,cookies=cookies,proxies=proxies,verify=False)
        print(res.text)
        text=res.text+page
        token=sm3_hash(str_to_bytes(text))
        data=data = {
            'page': page,
            'token': token 
            }

        print(data)
 
        headers['accept-time']=res.text 
        res=requests.post("https://match2023.yuanrenxue.cn/api/match2023/3",data=data,headers=headers,cookies=cookies, proxies=proxies,verify=False)
 
        for item in res.json()['data']:
            total+=item['value']
        
        # break 
        time.sleep(0.5)
    print(total )
if __name__=='__main__':
    crawl()
    # print(sm3_hash(str_to_bytes("16857845032544")))
