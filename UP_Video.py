from selenium import webdriver
from multiprocessing.dummy import Pool
from time import sleep
import requests

class Bili_UP_Video_Download():

    def main(self):
        self.head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        self.mid=input("请输入UP主mid：")
        self.start_page=input("请输入起始页数：")
        self.end_page=input("请输入结束页数：")
        self.Video_urls=[]
        pool = Pool(3)
        pool.map(self.Get_UP_Video_url,self.Params_list()) #获取视频url
        print("-"*30+"共获取%d条视频url"%(len(self.Video_urls))+"-"*30)
        option = webdriver.ChromeOptions()
        option.add_argument("--user-data-dir=" + r"C:/Users/13772/AppData/Local/Google/Chrome/User Data/")  # 启用带插件的浏览器
        self.bro = webdriver.Chrome(options=option)
        for url in self.Video_urls:
            self.bro.get(url)
            sleep(6)
            self.Video_list()

    # 生成params参数列表
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

    #判断是否存在视频列表即多个视频，如果存在以此点击下载，否则只下载当前视频
    def Video_list(self):
        try:
            if self.bro.find_element_by_xpath('//*[@id="multi_page"]/div[1]/div[1]/h3').text == "视频选集":
                li_list = self.bro.find_elements_by_xpath('//ul[@class="list-box"]/li')
                for i in range(len(li_list)):
                    li_list[i].click()
                    self.bro.refresh() #刷新页面
                    sleep(3)
                    self.Download_video()
                    li_list = self.bro.find_elements_by_xpath('//ul[@class="list-box"]/li')
        except:
            self.Download_video()
            pass

    #下载视频函数，点击助手和下载按钮
    def Download_video(self):
        try:
            # 点击哔哩哔哩助手
            sleep(2)
            self.bro.find_element_by_id('bilibiliHelper2HandleButton').click()
        except Exception as e:
            print("点击哔哩哔哩助手出现异常：", end="\n")
            print(e)
            pass
        try:
            # 点击下载格式
            sleep(2)
            self.bro.find_element_by_xpath('//div[@class="sc-jUEnpm cCSKON"]/div[1]').click()
            sleep(2)
        except Exception as e:
            print("点击下载格式出现异常：", end="\n")
            print(e)
            pass

if __name__ == "__main__":
    Spider=Bili_UP_Video_Download()
    Spider.main()