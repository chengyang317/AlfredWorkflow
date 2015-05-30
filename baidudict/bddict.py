# coding=utf-8
__author__ = 'Philip'


import sys
import hashlib
import time
import math
import base64
import urllib2
import urllib
import re
import json
import alfredxml

client_id = '1xML4eLvqG8runr4uHcDPU6f'

def is_cn_char(i):
    return 0x4e00<=ord(i)<0x9fa6

def bdDict(From,To,Q):
    resp = urllib2.urlopen("http://openapi.baidu.com/public/2.0/translate/dict/simple?client_id=%s&q=%s&from=%s&to=%s"%(client_id,Q,From,To)).read()
    js = json.loads(resp,encoding = 'utf-8')
    return js

# alfred 的入口函数.
def query(query):
# 对query 作防御
    if(len(query)==0):
        rowList = [{'uid':'1',
                    'arg':'',
                    'autocomplete':'',
                    'icon':'icon.png',
                    'subtitle':'Please Input',
                    'title':'Please Input'}]
        element = alfredxml.genAlfredXML(rowList)
        print(element) #输出结果，其中arg值最为下一个query
        return
# 判断是否为中文字符，若是 汉译英 若否 英译汉
    if(is_cn_char(unicode(query,"utf-8")[0])):
        resp = bdDict("zh","en",query)
    else:
        resp = bdDict("en","zh",query)
    if(resp[u'errno'] == 0):  # 通过bdDict() 函数 ，调用百度词典HTTP接口.
        if(len(resp[u'data'])==0):
            return
        rowList = []
        subtitle = ''
        k = resp['data']['symbols'][0] # 解析JSON.
        uid = 1
        for i in k.keys():
            if(i.startswith("ph_")):
                subtitle +=i[3:]+'['+ resp['data']['symbols'][0][i] + ']'
        # 解析JSON, 生成rowList
        rowList.append({
                'uid':uid,
                'arg':query,
                'autocomplete':query,
                'icon':'icon.png',
                'subtitle':subtitle.encode("utf-8"),
                'title':'发音'})
        uid +=1


        for i in resp['data']['symbols'][0]['parts']:
            if(len(i['part'])>0):
                subtitle = reduce(lambda x,y:x+","+y, i['part'])
            else:
                subtitle = ''
            title = reduce(lambda x,y:x+","+y, i['means'])
            rowList.append({
                'uid':uid,
                'arg':query,
                'autocomplete':query,
                'icon':'icon.png',
                'subtitle':subtitle.encode("utf-8"),
                'title':title.encode("utf-8")})
            uid +=1


    else:
        print("err")
        pass
    #print(rowList)
    # 生成XML文件.
    print(alfredxml.genAlfredXML(rowList))