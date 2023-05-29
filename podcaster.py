import argparse
import sys
import os
import glob
import subprocess
from utils import selenium
from utils import csv2audio
from utils import vad


def argparse_init():
    if len(sys.argv) == 1:
        unicorn = r"""
    =========================================================
     ____              _                    _               
    |  _ \   ___    __| |  ___   __ _  ___ | |_   ___  _ __ 
    | |_) | / _ \  / _` | / __| / _` |/ __|| __| / _ \| '__|
    |  __/ | (_) || (_| || (__ | (_| |\__ \| |_ |  __/| |   
    |_|     \___/  \__,_| \___| \__,_||___/ \__| \___||_|   
        
                                               --by Unicorn.
    =========================================================
    description:
    Podcaster is a web crawler tool designed specifically for
    the podcast resources on www.listennotes.com. It allows
    comprehensive scraping of podcast information, including
    all episodes with their descriptions, tags, sources,
    cover ratings, rankings, audio files, and more. It offers
    customization options for the target URL, the number of
    podcasts to crawl,and other parameters.
    
    Example:
        python podcaster.py --U [url] --headless --noimg -A --whisper --tts --sovits

    options:
        -h, --help            show this help message and exit
        -U URL, --url URL     输入要爬取的url
        -O OUTPUT_PATH, --output OUTPUT_PATH
                                选择输出到文件夹,默认保存到'./results/'下
        --driver DRIVER_PATH  设置selenium依赖的chromedriver,默认使用'./chromedriver/chromedriver'
        --headless            启用无头浏览器模式,后台静默运行
        --noimg               启用图片阻塞模式,不加载图片资源
        -A, --audio           下载对应音频文件
        --csvpath CSVPATH     音频所在csv
        --audio_output AUDIO_OUTPUT
                                下载音频文件路径
        --whisper             转录音频为文字,并智能处理、翻译为中文独白口播稿
        --tts                 TTS文字转音频
        --sovits              So-vits音色合成处理

                                                                    --By Unicorn.
        """
        print(unicorn)
        sys.exit(0)
    parser = argparse.ArgumentParser(
        prog="Podcaster",
        description="Podcaster is a web crawler tool designed specifically for the podcast resources on www.listennotes.com. It allows comprehensive scraping of podcast information, including all episodes with their descriptions, tags, sources, cover ratings, rankings, audio files, and more. It offers customization options for the target URL, the number of podcasts to crawl, and other parameters.",
        epilog='--By Unicorn.'
    )
    # 参数设置
    parser.add_argument('-U', '--url', dest='url', help="输入要爬取的url")
    # parser.add_argument('-O', '--output', default="./results/",
    #                     dest='output_path', help="选择输出到文件夹,默认保存到'./results/'下")
    # parser.add_argument('--driver', default="./chromedriver/chromedriver", dest='driver_path',
    #                     help="设置selenium依赖的chromedriver,默认使用'./chromedriver/chromedriver'")
    parser.add_argument("--headless", action="store_true",
                        help="启用无头浏览器模式,后台静默运行")
    parser.add_argument("--noimg", action="store_true",
                        help="启用图片阻塞模式,不加载图片资源")
    """==============================================================================="""
    parser.add_argument("-A", "--audio", action="store_true", help="下载对应音频文件")
    parser.add_argument("--csv", default=None, help="指定播客csv")

    parser.add_argument("--preprocess", action="store_true",  help="音频文件预处理")
    parser.add_argument("--threads", type=int,
                        default=None,  help="多线程音频文件预处理")
    parser.add_argument("--pre_dir", default=None, help="指定预处理音频文件所在文件夹")

    # parser.add_argument("--audio_output", help="下载音频文件路径")
    parser.add_argument("--whisper", action="store_true",
                        help="转录音频为文字,并智能处理、翻译为中文独白口播稿")
    parser.add_argument("--tts", action="store_true", help="TTS文字转音频")
    parser.add_argument("--sovits", action="store_true", help="So-vits音色合成处理")

    # 解析参数
    args = parser.parse_args()
    return args


def check_dependencies():
    print("[ + ] Checking the dependencies required by the program...")
    # 检查是否存在 requirements.txt 文件
    requirements_file = './requirements.txt'
    if not os.path.isfile(requirements_file):
        print("[ ! ]未找到 requirements.txt 文件，请确保文件存在。")
        sys.exit(1)

    # 读取 requirements.txt 文件中的依赖项
    with open(requirements_file, 'r') as file:
        requirements = file.read().splitlines()

    # 检查并安装依赖项
    for requirement in requirements:
        try:
            subprocess.check_output(
                ['pip', 'show', requirement], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            print(f"[ + ] 正在安装依赖项: {requirement} ...")
            subprocess.check_call(['pip', 'install', requirement])

    print("[ * ] All dependencies are checked and installed.")


def main(args):
    # 执行系统命令
    # command = "python "
    # process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # # 读取命令执行结果并输出到当前终端
    # for line in process.stdout:
    #     print(line.decode().strip())

    # # 等待命令执行完成
    # process.wait()
    if args.url:
        chrome = selenium.Chrome(args)
        chrome.selenium_chrome()
        # driver = chrome.driver
        chrome.page()
        podcast_name = chrome.podcast_name
        csv_save_path = chrome.csv_save_path
        print(">>> CSVs 保存在: "+csv_save_path+" <<<")

    if args.audio:
        if args.csv is None:
            csv_path = csv_save_path
        else:
            csv_path = args.csv
        download_audio = csv2audio.DownloadAudio(csv_path)
        download_audio.read_csv_url()
        download_audio.get_redirect()
        # podcast_name = download_audio.podcast_name
        print(">>> Audios 保存在: "+download_audio.full_audios_dir+" <<<")

    if args.preprocess:
        if args.pre_dir is None:
            pre_audio_dir = download_audio.full_audios_dir
        else:
            pre_audio_dir = args.pre_dir
        podcast_name = os.path.basename(pre_audio_dir.rstrip('/'))
        print("[ + ] VAD 模型加载...")
        import torch
        USE_ONNX = False  # change this to True if you want to test onnx model
        if USE_ONNX:
            os.system("pip install -q onnxruntime")
        model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                      model='silero_vad',
                                      force_reload=True,
                                      onnx=USE_ONNX)
        print(f"[ + ] 音频预处理...\n* 正在处理播客: {podcast_name}")
        if args.threads is not None:
            import concurrent.futures
            # import multiprocessing
            import threading
            max_workers = args.threads

            def process_file(file_path):
                v = vad.VAD(file_path, model, utils, podcast_name)
                v.vad()
                v.combine()
            mp3_files = glob.glob(f"{pre_audio_dir}*.mp3")

            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                executor.map(process_file, mp3_files)
            # with multiprocessing.Pool() as pool:
            #     pool.map(process_file, mp3_files)
        else:
            for file_path in glob.glob(f"{pre_audio_dir}*.mp3"):
                v = vad.VAD(file_path, model, utils, podcast_name)
                v.vad()
                v.combine()
        print(f"[ * ] 播客 {podcast_name} 音频预处理完成")


if __name__ == '__main__':
    args = argparse_init()
    check_dependencies()
    main(args)
    # print(args)
