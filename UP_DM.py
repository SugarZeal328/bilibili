from selenium import webdriver
from selenium.webdriver import ChromeOptions
import requests
from multiprocessing.dummy import Pool
from time import sleep
import pandas as pd
from lxml import etree
import os

class Bili_UP_DM():
    def __init__(self):
        option = ChromeOptions()
        option.add_experimental_option('prefs',{'profile.managed_default_content_settings.images': 2})  # 禁止图片加载，加快速度
        option.add_argument('--proxy-server=http://127.0.0.1:9000')
        option.add_argument('--headless')
        option.add_argument('--disable-gpu')
        self.bro = webdriver.Chrome(options=option)
        self.head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        self.mid=input("请输入UP主mid：")
        self.start_page=input("请输入起始页数：")
        self.end_page=input("请输入结束页数：")

    def main(self):
        self.Video_urls=[]
        pool = Pool(3)
        pool.map(self.Get_UP_Video_url,self.Params_list()) #获取视频url
        for url in self.Get_UP_DM_url():
            self.Get_UP_DM_Data(url)

    #生成params参数列表
    def Params_list(self):
        params_list=[]
        for i in range(int(self.start_page),int(self.end_page)+1):
            params = {
                "mid": int(self.mid),
                "ps": 30,
                "tid": 0,
                "pn":i,
                "keyword":"",
                "order": "pubdate",
                "json":"json"
            }
            params_list.append(params)
        return params_list

    #接受params列表中的params访问数据获得UP主所有视频url
    def Get_UP_Video_url(self,params):
        js = requests.get("https://api.bilibili.com/x/space/arc/search?",headers=self.head,params=params).json()
        for i in js["data"]["list"]["vlist"]:
            self.Video_urls.append("https://www.bilibili.com/video/" + i["bvid"])

    def Get_UP_DM_url(self):
        #遍历每一个视频url进行模拟点击弹幕按钮，实现后台mitmdump抓包 获得弹幕数据接口所需要的cid
        for url in self.Video_urls:
            self.bro.get(url)
            self.bro.maximize_window()  # 最大化浏览器
            sleep(14)
            element1 = self.bro.find_element_by_xpath('//div[@class="bui-collapse-arrow"]/span[1]')
            self.bro.execute_script("arguments[0].click();", element1)
            sleep(4)
        self.bro.quit()
        print("-"*30+"mitmdump抓包已经结束"+"-"*30)
        #抓包结束读入数据，开始拼接弹幕url
        names = ["cid", "oid"]
        df = pd.read_csv("cid.csv", names=names)
        df = df.drop_duplicates() #去重
        df = df.reset_index(drop=True)
        pd.DataFrame(df).to_csv('.\\cid.csv')
        DM_url = ["https://comment.bilibili.com/%s.xml" % (i) for i in df.cid]
        print("-" * 15 + "共拼接%d条弹幕接口"%(len(DM_url)) + "-" * 15)
        return DM_url

    def Get_UP_DM_Data(self,url):
        print("-" * 30 + "正在获取弹幕数据" + "-" * 30)
        if not os.path.exists("UP_DM"):
            os.mkdir("UP_DM")
        #开始访问真实的弹幕数据接口并保存数据
        r = requests.get(url, headers=self.head)
        r.encoding = 'utf8'
        html = etree.HTML(r.text.encode('utf-8'))
        d_list = html.xpath("//d")
        for d in d_list:
            dm = d.xpath("./text()")[0]
            name = url.split("com/")[-1].replace(".xml", "")
            #所有所有弹幕存为一个txt，命名为UP_DM
            with open("UP_DM.txt","a",encoding="utf-8") as f:
                f.write(dm)
                f.write('\n')
            #一个视频弹幕存为一个txt 全部放在文件夹里
            with open("./UP_DM/%s.txt" % (name), "a", encoding="utf-8") as f:
                f.write(dm)
                f.write('\n')

if __name__ == "__main__":
    Spider=Bili_UP_DM()
    Spider.main()