# -*- coding: utf-8 -*-
import requests
import json
import urllib
import gzip
import io
import os
import http.cookiejar
import re
import random
import time
import csv
import codecs
import demjson

#代理部分
proxies = {
  "http":"http://127.0.0.1:1080",
  "https":"https://127.0.0.1:1080"
}
s = requests.session()
s.proxies = proxies
s.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
}
#代理和基础连接部分结束

def getMessage(keyword):
  search = keyword
  website = "http://www.instagram.com"
  q = urllib.parse.quote(search)    #网址转码
  url1 = website + "/explore/tags/" + q + "/?__a=1" #搜索标签部分的地址，返回的是一个JSON数据
  requests.adapters.DEFAULT_RETRIES = 5 #设定重试次数
  html = s.get(url1)    #获取页面数据,返回一个状态代码；比如200
  ans = json.loads(html.text)   #获取返回的json数据
  pgn = 0   #页面序号？

getMessage("beauty")