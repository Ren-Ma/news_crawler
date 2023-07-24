import pickle
import os
from tqdm import tqdm
import time

start_time = time.time()
# with open('/data/renma/news_crawler/pkl/news_yangquan.pkl','rb') as f:
with open('/data/renma/news_crawler/pkl/news_yangquan_xianqv.pkl','rb') as f:
    date_video_url = pickle.load(f)

for date,link in tqdm(date_video_url.items()):
#    os.system("ffmpeg -i %s -c copy -bsf:a aac_adtstoasc %s.mp4"%(link,'/data/renma/news_crawler/video/yangquan_news_video/'+date)) 
    os.system("ffmpeg -i %s -c copy -bsf:a aac_adtstoasc %s.mp4"%(link,'/data/renma/news_crawler/video/yangquan_xianqv_news_video/'+date)) 

end_time = time.time()
duration = end_time - start_time
print('视频下载完成！共用时：', duration/60, '分')