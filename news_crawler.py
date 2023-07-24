import json
import re
import os
import chardet
import requests
import pickle
from bs4 import BeautifulSoup
from tqdm import tqdm

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
def date_trans(date):
    date_list = re.split("[年月日]", date)[1:]
    date_list_1 = ["0" + d if len(d) == 1 else d for d in date_list]
    return "".join(date_list_1)

def get_news_url_lst(mapi_url):
    """通过读取mapi来获取新闻视频url"""
    news_url_lst = []
    rqg = requests.get(mapi_url, headers=headers, timeout=10.0) 
    rqg.encoding = chardet.detect(rqg.content)["encoding"]
    html = rqg.content.decode("utf-8")
    soup = BeautifulSoup(html) 
    api_contents = json.loads(soup.text)
    for item in api_contents:
        news_url = item['content_urls']['www']
        news_url_lst.append(news_url)
    news_url_lst = list(set(news_url_lst))
    return news_url_lst

def get_date_video_url(news_url_lst):
    """获取视频url"""
    date_video_url = {}
    for item in tqdm(news_url_lst):
        rqg = requests.get(item, headers=headers, timeout=3.0)  # .content
        rqg.encoding = chardet.detect(rqg.content)["encoding"]
        html = rqg.content.decode("utf-8")
        soup = BeautifulSoup(html, "lxml")  # 生成BeautifulSoup对象
        try:
            # news_date = soup.find_all(id="m_newsTitle")[0].contents[0].replace("葫芦岛新闻", "")
            # news_date = soup.find_all(class_="titSpan")[0].contents[0].replace("阳泉新闻", "")
            news_date = soup.find_all(class_="titSpan")[0].contents[0].replace("县区新闻联播", "")
            news_date = date_trans(news_date)
            # video_url = (str(soup.find_all(type="text/javascript")[2]).split("video=['")[1].split("->video/mp4']")[0])
            video_url = str(soup.find_all(id="m3u8")[0]['value'])
            date_video_url[news_date] = video_url
        except:
            print(item)
    return date_video_url

def export_date_video_url(date_video_url, output):

    """把视频url信息导出"""
    with open(output, "wb") as f:
        pickle.dump(date_video_url, f)

# 阳泉新闻 -------------------------------------------------------------------------------
mapi_url = "https://mapi.yqrtv.com/api/v1/contents.php?&count=500&offset=0&column_id=110&with_child=1"
news_url_lst = get_news_url_lst(mapi_url)
date_video_url = get_date_video_url(news_url_lst)
export_date_video_url(date_video_url, "pkl/news_yangquan.pkl")
print('视频url列表获取完成，已存储到本地！')

# 阳泉县区新闻 -------------------------------------------------------------------------------
mapi_url = "https://mapi.yqrtv.com/api/v1/contents.php?&count=500&offset=0&column_id=112&with_child=1"
news_url_lst = get_news_url_lst(mapi_url)
date_video_url = get_date_video_url(news_url_lst)
export_date_video_url(date_video_url, "pkl/news_yangquan_xianqv.pkl")
print('视频url列表获取完成，已存储到本地！')

# 葫芦岛新闻 -------------------------------------------------------------------------------
## 通过request遍历新闻列表获取新闻url
for i in range(51):
    url = "http://www.hldbtv.com/ProgramsData/Channel_24/Index_{data}.aspx".format(data=str(i + 1))
    rqg = requests.get(url, headers=headers, timeout=10.0)  # .content
    rqg.encoding = chardet.detect(rqg.content)["encoding"]
    html = rqg.content.decode("utf-8")
    soup = BeautifulSoup(html, "lxml")  # 生成BeautifulSoup对象
    for item in soup.find_all(target="_blank"):
        if "日葫芦岛新闻" in item.contents[0]:
            news_url_lst.append("http://www.hldbtv.com" + item["href"])