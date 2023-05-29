import requests
import re
import os
import pandas as pd
from utils import save2csv
from tqdm import tqdm
"""
    self.csvpath            - 保存的csv文件路径 
    self.podcast_name
    self.urls               - audios链接列表
    self.savedir            - relative audios directory
    self.full_audios_dir    - absolute audios directory
"""


class DownloadAudio:
    def __init__(self, csvpath):
        self.csvpath = csvpath

    def read_csv_url(self):
        csvpath = self.csvpath
        df = save2csv.rename(csvpath)
        # 读取CSV文件，假设链接列的名称为"链接"
        # df = pd.read_csv(csvpath)
        podcast = df["播客名称"][0]
        parts = podcast.split(":", 1)
        podcast_name = parts[0].replace(" ", "")
        pattern = r"\W"  # 匹配所有非字母数字字符
        podcast_name = re.sub(pattern, "_", podcast_name)
        self.podcast_name = podcast_name
        audio_dir = f"./results/audios/{podcast_name}/"
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)
        ep_names = df["剧集名"]
        urls = df['audio链接']

        self.ep_names = ep_names
        self.urls = urls
        self.savedir = audio_dir
        # return ep_names,urls,audio_dir

    def get_redirect(self):
        ep_names = self.ep_names
        urls = self.urls
        savedir = self.savedir
        self.full_audios_dir = f"{os.getcwd()}{savedir.lstrip('.')}"
        try:
            # config.set('Temporary', 'audio_path',
            #            f"{os.getcwd()}{savedir.lstrip('.')}")
            # # 将修改后的配置写回配置文件
            # with open('config.ini', 'w') as configfile:
            #     config.write(configfile)
            # 遍历链接
            for ep_name, url in tqdm(zip(ep_names, urls)):
                resp = requests.get(url, allow_redirects=True)
                final_url = resp.url
                print("[ * ] Audio链接: "+final_url)
                audio_data = resp.content
                name_parts = ep_name.split(":", 1)
                epname = name_parts[0].replace(" ", "")
                pattern = r"\W"  # 匹配所有非字母数字字符
                podcast_name = re.sub(pattern, "_", epname)
                path = f"{savedir}{epname}.mp3"
                try:
                    with open(path, 'wb') as f:
                        f.write(audio_data)
                    # print("[ * ] Audio下载成功.Path: "+path)
                except:
                    # print("[ ! ] Audio下载失败.Path: "+path)
                    continue
            print("[ * ] Audio 完成下载. Path: "+savedir)
        except requests.exceptions.RequestException as e:
            print(f"请求出错: {e}\n")
