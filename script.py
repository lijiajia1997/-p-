#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 23:01:55 2021

@author: adrbmdns
"""

import requests
import json
import pandas as pd
import time

# please change file name and directory
data01 = pd.read_excel('GNZ48-吴羽霏应援会.xls')

#dataframe to list
aid = data01[['视频aid']]
aid = aid.values.tolist()
aid01 = []
for i in aid:
    for aaa in i:
        bbb = int(aaa)
        aid01.append(bbb)
        
#get p names
aid_names = []
for i in aid01:
    print("正在爬取视频" + str(i) + "分p名称\n")
    url = "https://api.bilibili.com/x/player/pagelist?aid=" + str(i) + "&jsonp=jsonp"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63'}
    video_data = requests.get(url=url, headers=headers)
    v_cid_info = json.loads(video_data.text)
    p_length = len(v_cid_info['data'])
    video_name = []
    video_name.append(str(i))
    for u in range(p_length):
        name00 = v_cid_info['data'][u]['part']
        video_name.append(name00)
    aid_names.append(video_name)
    time.sleep(3)

df01 = pd.DataFrame(aid_names)
df01.to_excel('视频分p名.xls')

    
    
    
    
    
    
    