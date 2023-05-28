import argparse,sys,os,subprocess
import podcaster_main
import redirect_audio
global_podcastname = ""
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
    
    options:
        -h, --help         show this help message and exit
    
        """
        print(unicorn)
        sys.exit(0)
    parser = argparse.ArgumentParser(
        prog="Podcaster",
        description="Podcaster is a web crawler tool designed specifically for the podcast resources on www.listennotes.com. It allows comprehensive scraping of podcast information, including all episodes with their descriptions, tags, sources, cover ratings, rankings, audio files, and more. It offers customization options for the target URL, the number of podcasts to crawl, and other parameters.",
        epilog='--By Unicorn.'
    )
    # 参数设置
    parser.add_argument('-U','--url',dest='url', help="输入要爬取的url")
    parser.add_argument('-C','--count',default="1",dest='count', help="选择爬取页数,默认为1")
    parser.add_argument('-O','--output',default="./results/",dest='output_path', help="选择输出到文件夹,默认保存到'./results/'下")
    parser.add_argument('--driver',default="./chromedriver/chromedriver",dest='driver_path', help="设置selenium依赖的chromedriver,默认使用'./chromedriver/chromedriver'")
    parser.add_argument("--headless", action="store_true", help="启用无头浏览器模式,后台静默运行")
    parser.add_argument("--noimg", action="store_true", help="启用图片阻塞模式,不加载图片资源")
    """==============================================================================="""
    parser.add_argument("-A","--audio", action="store_true", help="下载对应音频文件")
    parser.add_argument("--csvpath", help="音频所在csv")
    parser.add_argument("--audio_output", help="下载音频文件路径")
    parser.add_argument("--whisper", action="store_true", help="转录音频为文字,并智能处理、翻译为中文独白口播稿")
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
            subprocess.check_output(['pip', 'show', requirement], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            print(f"[ + ] 正在安装依赖项: {requirement} ...")
            subprocess.check_call(['pip', 'install', requirement])

    print("[ * ] All dependencies are checked and installed.")

def main(args):
    podcaster_main.start_scraping(args)
    
    if args.audio:
        if args.csvpath:
            ep_names,urls,audio_dir = redirect_audio.read_csv_url(args.csvpath)
            redirect_audio.get_redirect(ep_names,urls,audio_dir)
        else:
            print("[ ! ] 请输入音频链接所在csv文件路径：--csvpath [xxx.csv]")
            sys.exit(1)
        
    
if __name__ == '__main__':
    args = argparse_init()
    check_dependencies()
    main(args)
    # print(args)