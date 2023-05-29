import time
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from utils.save2csv import write_to_csv

"""
================================================================
Podcaster 爬虫:
1. selenium_chrome: 初始化
2. page: 单播客url爬取
    - 自动加载全部页面
    - 获取所有历史剧集
        - 播客名称
        - 简介
        - 标签
        - 评分 + 排名
            - 剧集名
            - 剧集介绍
            - audio链接
================================================================
chrome = Chrome(args)
chrome.selenium_chrome()
driver = chrome.driver                  driver
chrome.page()
podcast_name = chrome.podcast_name      播客名称
csv_save_path = chrome.csv_save_path    保存的csv文件路径
"""


class Chrome:
    def __init__(self, args):
        self.args = args
        """
        self.args
        self.driver         driver
        self.podcast_name   播客名称
        self.csv_save_path  保存的csv文件路径
        """

    def selenium_chrome(self):
        # 创建一个Chrome选项对象
        chrome_options = Options()
        service = Service(executable_path='./chromedriver/chromedriver')
        if self.args.headless:
            chrome_options.add_argument("--headless")
        if self.args.noimg:
            # 禁止加载图片
            prefs = {"profile.managed_default_content_settings.images": 2}
            chrome_options.add_experimental_option("prefs", prefs)

        # 初始化webdriver
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # 自定义的cookie
        cookies = [
            {'name': '_gid', 'value': 'GA1.2.270288550.1684565151'},
            {'name': '_gcl_au', 'value': '1.1.1066160910.1684565347'},
            {'name': '_fbp', 'value': 'fb.1.1684565346978.1220227898'},
            {'name': '_gat_gtag_UA_83220730_1', 'value': '1'},
            {'name': 'messages', 'value': 'W1siX19qc29uX21lc3NhZ2UiLDAsMjUsIlN1Y2Nlc3NmdWxseSBzaWduZWQgaW4gYXMgdW5pY29ybmphZGUuIiwiIl1d:1q0HkQ:sAVKuA5_974-c959hxmmmiP0tY8MRltT1NSiUbR32xY'},
            {'name': 'csrftoken', 'value': 'pXuDrbesq6cYAFI8qQS32EGU4ynysMne'},
            {'name': 'sessionid', 'value': 'j0dpdt6ulg56grcok5d2814a6jcvq0mo'},
            {'name': '_ga', 'value': 'GA1.1.1521668813.1684565151'},
            {'name': '_ga_T0PZE2Z7L4', 'value': 'GS1.1.1684569976.2.1.1684570531.48.0.0'}
        ]
        print("[ * ] ChromeDriver配置初始化成功")
        # 打开网页
        driver.get(self.args.url)
        print("[ * ] 打开Url成功")
        # 添加cookie
        for cookie in cookies:
            driver.add_cookie(cookie)

        # 刷新页面以应用cookie
        driver.refresh()
        print("[ * ] Cookie设置成功")
        time.sleep(5)
        self.driver = driver

    def page(self, driver=None, savepath=None):
        if driver is None and savepath is None:
            driver = self.driver
            savepath = self.args.output_path
        time.sleep(5)
        podcastname_list, intro_list, tagcsv, ls_list, top_list, episode_titles, ep_intros, audio_hrefs = [
            [] for _ in range(8)]

        """播客名"""
        podcast_name = driver.find_element(
            By.XPATH, "//div[contains(@class,'ln-row')]//div[@class='w-full']/h1/a").get_attribute('title')

        print("podcast_name:"+podcast_name)
        """简介"""
        intro = driver.find_element(
            By.XPATH, "//div[contains(@class,'ln-text-p')]").text
        # print("intro:"+intro)
        """标签"""
        tags = driver.find_elements(
            By.XPATH, "//div[starts-with(@class,'mr-2 rtl')]/a")
        tag_list = [tag.text for tag in tags]
        tag = ', '.join(tag_list)
        # print("tag_list:"+str(tag_list))
        """评分 - 排名"""
        score = driver.find_elements(
            By.XPATH, "//div[@id='listen-score']//div[contains(@class,'number')]")
        ls = re.findall(r'\d+', score[0].text)
        top = re.findall(r'(?:\d+(?:\.\d+)?|\.\d+)%', score[1].text)
        load = driver.find_elements(
            By.XPATH, "//button[contains(text(),'more')]")
        # print("LS:"+ls[0]+"    TOP:"+top[0])
        page = 1
        while True:
            try:
                load = driver.find_element(
                    By.XPATH, "//button[contains(text(),'more')]")
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center', inline: 'nearest', behavior: 'auto'});", load)
                driver.execute_script("arguments[0].click();", load)
                print("\033[F\033[K", end="")
                print(f"[ + ] 当前爬取页面进度: Page {page} ...")
                page = page + 1
                time.sleep(0.6)
                try:
                    end = driver.find_element(
                        By.XPATH, "//div[contains(text(),'have seen all episodes of this podcast')]")
                    print("[ * ] 发现终止标记,剧集已全部加载完成")
                    break
                except:
                    continue

            except NoSuchElementException:
                print("[ * ] 剧集已全部加载完成")
                break
            except Exception as e:
                print("[ x ] 发生异常:", e)
                break

        def get_details(ep, i):
            """剧集名"""
            episode = ep.find_element(
                By.XPATH, ".//div[contains(@class,'w-full')]//a")
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'start', inline: 'nearest'});", episode)
            episode_title = episode.get_attribute('title')
            print(f"{i}> {episode_title}")
            """剧集介绍"""
            ep_intro = ep.find_element(
                By.XPATH, ".//div[contains(@class,'line-clamp')]")
            ep_intro = ep_intro.text
            time.sleep(0.2)
            """audio链接"""
            ep_more = ep.find_element(By.XPATH, ".//a[@aria-label='MORE']")
            # ep_more = ep.find_element(By.XPATH, "./div/div[3]/div/div[3]/div[7]/a")
            driver.execute_script("arguments[0].click();", ep_more)

            # audio_href = ep.find_element(By.XPATH, "./div/div[3]/div/div[3]/div[7]/div/div/div[2]/a[1]").get_attribute('href')
            audio_href = ep.find_element(
                By.XPATH, ".//a[@title='Download audio file']").get_attribute('href')
            driver.execute_script("arguments[0].click();", ep_more)
            # print("ep_title: "+episode_title+"ep_intro:"+ep_intro)
            episode_titles.append(episode_title)
            ep_intros.append(ep_intro)
            audio_hrefs.append(audio_href)
        print("[ + ] 开始爬取剧集详细信息...")
        i = 1
        """默认剧集"""
        # print("[ + ] 开始默认剧集爬取...")
        each_eps = driver.find_elements(By.XPATH, "//div[@class='pt-4']")
        for ep in each_eps:
            try:
                get_details(ep, i)
                i = i + 1
            except:
                continue
        """分页剧集"""
        time.sleep(1)
        # print("[ + ] 开始分集爬取...")
        exp_eps = driver.find_elements(
            By.XPATH, "//div[@id='episodes-pagination']/div/div[contains(@class,'gap-4')]")
        for exp in exp_eps:
            try:
                get_details(exp, i)
                i = i + 1
            except:
                continue
        podcastname_list = [podcast_name if index ==
                            0 else None for index in range(len(episode_titles))]
        intro_list = [intro if index ==
                      0 else None for index in range(len(episode_titles))]
        tagcsv = [tag if index ==
                  0 else None for index in range(len(episode_titles))]
        ls_list = [ls[0] if index ==
                   0 else None for index in range(len(episode_titles))]
        top_list = [top[0] if index ==
                    0 else None for index in range(len(episode_titles))]

        data = {
            '播客名称': podcastname_list,
            '简介': intro_list,
            '标签': tagcsv,
            '评分': ls_list,
            '排名': top_list,
            '剧集名': episode_titles,
            '剧集介绍': ep_intros,
            'audio链接': audio_hrefs
        }
        parts = podcast_name.split(":", 1)
        save_name = parts[0].replace(" ", "")
        pattern = r"\W"  # 匹配所有非字母数字字符
        save_name = re.sub(pattern, "_", save_name)
        global csv_path
        csv_path = f"{savepath}{save_name}.csv"
        write_to_csv(data, csv_path)
        print(
            f"[ * ] Save 《{podcast_name}》 To CSV Successfully.\nPath: {os.getcwd()}{csv_path.lstrip('.')}")
        self.podcast_name = podcast_name
        self.csv_save_path = f"{os.getcwd()}{csv_path.lstrip('.')}"