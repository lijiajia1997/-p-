#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 21:49:03 2021

@author: adrbmdns
"""

import requests
import json
from lxml import etree
import time
import xlwt
import re
 
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'cookie': "your cookie"
}
 
# 只需要把用户名，用户id，视频页数放到下面就行
target_users = [{'user_name': 'GNZ48-吴羽霏应援会', 'target_user_id': '231229661', 'pages_num': 17}]  # 要爬取的用户的id和视频的页数
for user in target_users:
    user_id = user['target_user_id']
    user_name = user['user_name']
    pages_num = user['pages_num']
    excel = xlwt.Workbook(encoding='utf-8')
    sheet = excel.add_sheet('sheet1')
    sheet.write(0, 0, '视频名称')
    sheet.write(0, 1, '发布时间')
    sheet.write(0, 2, '视频时长')
    sheet.write(0, 3, '投币数量')
    sheet.write(0, 4, '点赞数量')
    sheet.write(0, 5, '分享数量')
    sheet.write(0, 6, '评论数量')
    sheet.write(0, 7, '弹幕数量')
    sheet.write(0, 8, '播放量')
    sheet.write(0, 9, '收藏数量')
    sheet.write(0, 10, 'BV号')
    sheet.write(0, 11, '视频地址')
    sheet.write(0, 12, '视频aid')
    count = 1
    for page in range(1, pages_num + 1):
        try:
            print("正在爬取第" + str(page) + "页数据\n")
            user_main_page_link = "https://api.bilibili.com/x/space/arc/search?mid=" + user_id + "&ps=30&tid=0&pn=" + str(
                page) + "&keyword=&order=pubdate&jsonp=jsonp"
            user_response = requests.get(user_main_page_link, headers=headers)
            user_json = json.loads(user_response.text)
            user_datas = user_json['data']
            ls = user_datas['list']
            vlist = ls['vlist']
            for t in vlist:
                title = t['title']  # 标题
                length = t['length']  # 视频时长
                bvid = t['bvid']  # 视频id
                comment = t['comment']  # 评论数量
                view_num = t['play']
                video_url = 'https://www.bilibili.com/video/' + bvid  # 具体视频连接
                aid = t['aid']
                time.sleep(1)
 
                video_response = requests.get(video_url, 'html.parser', headers=headers).content
                video_text = requests.get(video_url)
                selector = etree.HTML(video_response)
                coin_span = selector.xpath("//span[@class='coin']")
                coin_num = coin_span[0].xpath("text()")[0].strip(' ').strip('\n').strip(' ')  # 硬币数量
                dm_span = selector.xpath("//span[@class='dm']")
                dm_num = dm_span[0].xpath("text()")[0].strip(' ').strip('\n')  # 弹幕数量
                like_span = selector.xpath("//span[@class='like']")
                like_num = like_span[0].xpath("text()")[0].strip(' ').strip('\n')  # 喜欢数量
                share_span = selector.xpath("//span[@class='share']")
                share_num = share_span[0].xpath("text()")[0].strip(' ').strip('\n')  # 分享数量
                collect_span = selector.xpath("//span[@class='collect']")
                collect_num = collect_span[0].xpath("text()")[0].strip(' ').strip('\n')  # 收藏数量
                publish_time = re.findall(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})", video_text.text)[
                    2]  # 发布时间
                sheet.write(count, 0, title)
                sheet.write(count, 1, publish_time)
                sheet.write(count, 2, length)
                sheet.write(count, 3, coin_num)
                sheet.write(count, 4, like_num)
                sheet.write(count, 5, share_num)
                sheet.write(count, 6, comment)
                sheet.write(count, 7, dm_num)
                sheet.write(count, 8, view_num)
                sheet.write(count, 9, collect_num)
                sheet.write(count, 10, bvid)
                sheet.write(count, 11, video_url)
                sheet.write(count, 12, aid)
                col = 13
                count += 1
                print("已经爬取第" + str(count) + "条\n")
            time.sleep(3)
        except:
            file_name = user_name + ".xls"
            excel.save(file_name)
    file_name = user_name + ".xls"
    excel.save(file_name)