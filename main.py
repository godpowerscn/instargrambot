# -*- coding: utf-8 -*-
from bson import ObjectId
import requests
import json
import urllib
import time
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
from pymongo import MongoClient
from structs import errorlog

#定义mongodb连接
conn = MongoClient('192.168.99.100',32768)
db = conn.mydb
#结束定义mongodb连接
#代理部分
proxies = {
  "http":"http://127.0.0.1:1080",
  "https":"https://127.0.0.1:1080"
}
s = requests.session()
s.proxies = proxies
s.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
}
#代理和基础连接部分结束

def getMessage(keyword,maxpage):
  search = keyword
  website = "http://www.instagram.com"
  q = urllib.parse.quote(search)    #网址转码
  url1 = website + "/explore/tags/" + q + "/?__a=1" #搜索标签部分的地址，返回的是一个JSON数据
  requests.adapters.DEFAULT_RETRIES = 5 #设定重试次数
  html = s.get(url1)    #获取页面数据,返回一个状态代码；比如200
  ans = json.loads(html.text)   #获取返回的json数据
  pgn = 0   #页面序号？
  pinglun_set = db.pinglun  #定义数据集评论
  errormessage_set = db.errormessage  #定义错误数据集
  edges = ans['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges']

  # for i in range(len(edges)):
  #   temp_dict = {}
  #   if len(edges[i]['node']['edge_media_to_caption']['edges']) == 0:
  #     continue
  #   huifu = edges[i]['node']['edge_media_to_caption']['edges'][0]['node']['text'] #图片的回复文本
  #   display_url = edges[i]['node']['display_url'] #图片的回复地址
  #   is_video = edges[i]['node']['is_video'] #是否是图片
  #   owner = edges[i]['node']['owner']['id']
  #   accessibility_caption =edges[i]['node']['accessibility_caption']  #这个显示的是英文,通过header设置改中文
  #   shotcode = edges[i]['node']['shortcode']  #短码
  #   typename = edges[i]['node']['__typename']  #类型名称


  b = ans['graphql']['hashtag']["edge_hashtag_to_media"]
  hnp = b['page_info']['has_next_page'] #是否有下一页
  hashn = b['page_info']['end_cursor']  #结束指针
  for page in range(0,int(maxpage)):
    #获取网页地址（返回json数据）
    url1 = website+"/graphql/query/?query_hash=298b92c8d7cad703f7565aa892ede943&variables=%7B%22tag_name%22%3A%22"+q+"%22%2C%22first%22%3A6%2C%22after%22%3A%22"+hashn+"%22%7D"
    html = s.get(url1, verify=False)
    try:
      ans = json.loads(html.text)
    except NameError as e:
      errorlog['_id'] = ObjectId()
      errorlog['url'] = url1
      errorlog['time'] = time.time()
      errorlog['WrongFile'] = e.__traceback__.tb_frame.f_globals['__file__']
      errorlog['WrongLine'] = e.__traceback__.tb_lineno
      errorlog['WrongMessage'] = e
      errormessage_set.insert(errorlog)

    try:
      edges = ans['data']['hashtag']['edge_hashtag_to_media']['edges']
    except:
       print("wrong")

    #开始写入
    for i in range (len(edges)):
      temp_dict = {}
      # print ((len(edges)))
      if len(edges[i]['node']['edge_media_to_caption']['edges']) == 0:
        continue
      d = edges[i]['node']['edge_media_to_caption']['edges'][0]['node']['text']
      shortcode = edges[i]['node']['shortcode']
      url2 = website+"/p/"+shortcode+"/?__a=1"
      getnt = s.get(url2, verify=False)
      try:
        getnt = json.loads(getnt.text)
      except:
        print("wrong")
      #print(url2)
      getnt['graphql']['shortcode_media']






getMessage("beauty",2)