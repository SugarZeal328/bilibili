import requests
from lxml import etree
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

class Bili_UP_Homepage():
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})  # 禁止图片加载，加快速度
        self.bro = webdriver.Chrome(options=chrome_options)
        self.head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        self.mid=input("请输入UP主mid：")
        self.start_page=input("请输入起始页数：")
        self.end_page=input("请输入结束页数：")

    def main(self):
        self.data_list = []
        self.urls = [] #视频url列表
        self.oids = []
        self.comments = []
        #遍历params列表中的params参数，给Get_UP_Video_url使用，获取视频url
        for params in self.Params_list():

            self.Get_UP_Video_url(params)
        #遍历视频url列表给Get_Video_Data使用获取数据
        for url in self.urls:

            self.Get_Video_Data(url)
        self.bro.quit()
        #将所有数据整合输出文件
        for a, b, c in zip(self.data_list, self.oids, self.comments):
            a["oid"] = b
            a["comment"] = c
        pd.DataFrame(self.data_list).to_csv('.\\浙江省图书馆.csv')

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
            self.urls.append("https://www.bilibili.com/video/" + i["bvid"])
            self.oids.append(i["aid"])
            self.comments.append(i["comment"])

    #根据视频url获取视频数据
    def Get_Video_Data(self,url):
        print(url)
        dic = {}
        self.bro.get(url)
        self.bro.execute_script('window.scrollTo(0, document.body.scrollHeight)')  # 向下拉动一屏

        self.bro.execute_script('window.scrollTo(0, document.body.scrollHeight)')  # 向下拉动一屏

        self.bro.execute_script('window.scrollTo(0, document.body.scrollHeight)')  # 向下拉动一屏

        html = etree.HTML(self.bro.page_source)
        try:
            dic["title"] = html.xpath('//div[@id="viewbox_report"]/h1/@title')[0]
        except:
            dic["title"] = ""
        try:
            dic["view"] = html.xpath('//span[@class="view"]/text()')[0]
        except:
            dic["view"] = ""
        try:
            dic["dm"] = html.xpath('//span[@class="dm"]/text()')[0]
        except:
            dic["dm"] = ""
        try:
            dic["rank"] = html.xpath('//span[@class="rank"]/text()')[0]
        except:
            dic["rank"] = ""
        try:
            dic["time"] = html.xpath('//div[@id="viewbox_report"]/div/span[3]/text()')[0]
        except:
            dic["time"] = ""
        try:
            dic["describes"] = html.xpath('//div[@class="info open"]/text()')[0]
        except:
            dic["describes"] = ""
        try:
            dic["like"] = html.xpath('//span[@class="like"]//text()')[0]
        except:
            dic["like"] = ""
        try:
            dic["coin"] = html.xpath('//span[@class="coin"]//text()')[0]
        except:
            dic["coin"] = ""
        try:
            dic["collect"] = html.xpath('//span[@class="collect"]//text()')[0]
        except:
            dic["collect"] = ""
        try:
            dic["share"] = html.xpath('//span[@class="share"]//text()')[0]
        except:
            dic["share"] = ""
        try:
            dic["page"] = html.xpath('//*[@id="comment"]/div/div[2]/div/div[4]/a[last()-1]/text()')[0]
        except:
            dic["page"] = "1"
        self.data_list.append(dic)


if __name__ == "__main__":
    Spider=Bili_UP_Homepage()
    Spider.main()