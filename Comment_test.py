import requests
import pprint
import json
import math
import sys
import re
import jieba
from wordcloud import WordCloud, ImageColorGenerator

def get_replies(VideoId, pages_number): # 传入两个参数分别是视频的ID和评论的页数
        video_url = 'https://api.bilibili.com/x/v2/reply' #设置请求地址
        video_url_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        }
        # 按照页数循环
        for numbers in range(pages_number):
            try:
        	    # 设置GET请求参数
                video_url_params = {
                    'jsonp': 'jsonp',
                    'pn': numbers+1,  # 页数从0开始的所以要+1
                    'type': '1',
                    'oid': VideoId,  # 视频id
                    'sort': '0',
                }
                # 获得评论列表
                repliesall = requests.get(video_url, params=video_url_params,
                                   headers=video_url_headers).json()['data']['replies'] # 这里直接取出评论列表
                for replies in repliesall:
                    # 循环获得次视频下面的评论
                    neirong = replies['content']['message']
                    # 返回评论内容
                    return neirong
            except:
                print('==================无法获取==================ID：' + VideoId)

def savetxts(commenttext):
        try:
            # 文件目录设置
            with open(r'd:\wb.txt', 'a', encoding='utf-8') as f:
                f.write(commenttext + '\n')
        except:
            print('--------------------这篇评论无法写入-------------------' + commenttext)

def GetVideoList(UP_main_ID,Page): # 这里需要传入UP主的ID和页数
    # 设置网址
    Get_list_Url = 'http://space.bilibili.com/ajax/member/getSubmitVideos'
    Get_list_params = {
        'mid': UP_main_ID,  # 设置up主ID
        'pagesize': '30',
        'tid': '0',
        'page': Page, # 第几页
        'keyword': '',
        'order': 'pubdate',
    }
    Get_list_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    }
    # 返回视频数据
    GetVideoList = requests.get(
        Get_list_Url, params=Get_list_params, headers=Get_list_headers).json()['data']['vlist']
    for ListID in GetVideoList:
        # 获取视频视频评论页数
        PageCount = pages_number(ListID['aid']) # 调用取评论页数的方法
        print('正在获取的视频ID：' + str(ListID['aid'],) + '总页数:' + str(PageCount)) # 打印一个提示信息
        # 调用获得评论方法
        get_replies(ListID['aid'], PageCount)
    # 返回
    return '获取评论完成。'

# 这个函数获得视频评论的页数，返回int格式，视频评论总页数
def pages_number(VideoId):
    video_url = 'https://api.bilibili.com/x/v2/reply'
    video_url_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    }

    video_url_params = {
        'jsonp': 'jsonp',
        'pn': '1',  # 页数
        'type': '1',
        'oid': VideoId,  # 视频id
        'sort': '0',
    }
    # 获得该视频的一些参数
    replies = requests.get(video_url, params=video_url_params,
                           headers=video_url_headers).json()
    # 获得总评论数
    pages_number = replies['data']['page']['count']
    # 获得并返回页数，每页有20条评论，所以返回总页数除20并且向上取整
    return math.ceil(pages_number / 20)

UpId = input('请输入UP主的IP：')
Uppage = input('请输入页数：')
GetVideoList(UpId,Uppage)
