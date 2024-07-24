import requests
import json
import time
import random
from dotenv import load_dotenv  
import os  
  
# 加载.env文件  
load_dotenv()

class AutoTyper():
    def __init__(self, authorization, channel_id, text,  inner_interval=10):
        self.channel_id = channel_id
        self.authorization = authorization
        self.inner_interval = inner_interval
        self.text = text

        self.count = 0

    def chat(self, auth, content):
        self.inner_sleep()
        # 伪装头
        header = {
            "Authorization": auth,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
        }
        # 整理发送的内容、生成nonce
        msg = {
            "content": content,
            "nonce": "82329451214{}33232234".format(random.randrange(0, 1000)),  # 923802142370693120 923802484009336832
            "tts": False
        }
        # 拼接频道地址
        url = 'https://discord.com/api/v9/channels/{}/messages'.format(self.channel_id)
        res = requests.post(url=url, headers=header, data=json.dumps(msg))
        print(res.content)

    def inner_sleep(self, t1=10, t2=60):
        time.sleep(self.inner_interval + random.randint(t1, t2))

    def batch_chat(self):
        print("task number:{}, time:{}".format(self.count, time.asctime(time.localtime(time.time()))))
        self.chat(self.authorization, self.text)
        self.count += 1


if __name__ == "__main__":
    channel_id =  os.getenv("CHANNEL_ID")   
    text = os.getenv("TEXT")  
    authorization = os.getenv("AUTHORIZATION") 
    autotyper = AutoTyper(authorization, channel_id, text)
    # 设定时间戳文件的路径  
    timestamp_file = 'last_run_timestamp.txt'  
  
    # 尝试读取上次运行的时间戳  
    last_run_timestamp = 0  
    try:  
        with open(timestamp_file, 'r') as f:  
            last_run_timestamp = float(f.read().strip())  
    except FileNotFoundError:  
        # 如果文件不存在，认为上次运行时间已经很久了  
        print("上次运行时间记录文件不存在，视为允许运行。")  
    while True:  
        current_timestamp = time.time()  
        time_difference = current_timestamp - last_run_timestamp  
      
        if time_difference > 7200:  # 7200秒 = 2小时  
            print(f"距离上次运行时间已超过两小时（{time_difference}秒），开始执行脚本。")  
            break  # 退出循环，开始执行脚本的其余部分  
        else:  
            print(f"距离上次运行时间未超过两小时（{time_difference}秒），等待中...")  
            time.sleep(60)  # 等待一分钟后再次检查     
    autotyper.batch_chat()
    
    # 更新时间戳文件 
    with open(timestamp_file, 'w') as f:  
        f.write(str(current_timestamp))
