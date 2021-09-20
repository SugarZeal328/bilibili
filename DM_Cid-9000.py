import csv

def response(flow):
    try:
        if "https://api.bilibili.com/x/v2/dm/web/seg.so?type=1" in flow.request.url:
            print("*_*"*100)
            dic={}
            dic["cid"]=flow.request.url.split("&oid=")[-1].split("&pid=")[0]
            dic["oid"]=flow.request.url.split("&pid=")[-1].split("&")[0]
            with open('cid.csv', 'a') as f:
                w = csv.writer(f)
                w.writerow(dic.values())
    except:
        pass