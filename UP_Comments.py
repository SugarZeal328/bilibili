import requests,os,csv
import pandas as pd
from multiprocessing.dummy import Pool
from time import sleep

class Bili_UP_Comment():
    def main(self):
        urls=self.Get_Comment_url() #url列表
        if not os.path.exists("UP_Comments"):
            os.mkdir("UP_Comments")
        pool = Pool(3)
        pool.map(self.Get_Comment_Data,urls) #获取数据

    #拼接评论url
    def Get_Comment_url(self):
        urls = []
        df = pd.read_csv("UP_Homepage.csv")
        for a, b in zip(df.oid[:], df.page[:]):
            for i in range(b):
                url = "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=%s&type=1&oid=%s&sort=2" % (i + 1, a)
                print(url)
                urls.append(url)
        print("-" * 30 + "共拼接" + str(len(urls)) + "个url" + "-" * 30)
        print(urls)
        return urls

    #根据拼接好的url访问页面获取数据
    def Get_Comment_Data(self,url):
        sleep(3)
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        data = requests.get(url, headers=head).json()
        if data['data']['replies']:
            for i in data['data']['replies']:
                dic = {}
                dic["name"] = i["member"]["uname"]
                dic["sex"] = i["member"]["sex"]
                dic["level"] = i["member"]["level_info"]["current_level"]
                dic["content"] = i["content"]["message"]
                dic["time"] = i["ctime"]
                dic["like"] = i["like"]
                dic["rcount"] = i["rcount"]
                dic["oid"] = url.split("oid=")[-1].replace("&sort=2", "")
                name=url.split("oid=")[-1].replace("&sort=2", "")
                with open('UP_Comments.csv', 'a', encoding="utf-8") as f:
                    w = csv.writer(f)
                    w.writerow(dic.values())
                with open("./UP_Comments/%s.csv" % (name), "a", encoding="utf-8") as f:
                    w = csv.writer(f)
                    w.writerow(dic.values())



if __name__ == "__main__":
    Spider=Bili_UP_Comment()
    Spider.main()