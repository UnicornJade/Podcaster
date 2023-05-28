import streamlit as st
import subprocess, os,redirect_audio,configparser
config = configparser.ConfigParser()
config.read('config.ini')

def crawler():
    st.write("# 🪲 Crawler")
    st.write("## Step 1: 选择模式")
    mode = st.radio("**👇 爬虫Mode选择**", ('指定播客Url爬取', '按标签爬取', '按关键词搜索'))
    if mode == '指定播客Url爬取':
        result = ""
        success = False
        error = False
        st.write("## Step 2: Run 🦄")
        st.caption("播客Url:")
        url = st.text_input('💡 输入播客Url', 'https://...')
        st.caption("**脚本参数设置:**")
        c1,c2 = st.columns(2)
        check_headless = c1.checkbox("无头浏览器模式",value=True)
        check_noimg = c2.checkbox("图片阻塞模式",value=True)
        start = st.button("Start")
        if url and start:
            headless = ''
            noimg = ''
            if check_headless:
                headless = '--headless'
            if check_noimg:
                noimg = '--noimg'
            try:
                command = f'python3.11 run.py -U {url} {headless} {noimg}'
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                success = True
            except subprocess.CalledProcessError as e:
                # 输出错误信息和回显信息
                st.error(f"命令执行失败！返回码：{e.returncode}")
                st.exception(e)
                error = e
            if success:
                if result:
                    st.success("☻ 命令执行成功！")
                    with st.expander("🐞$ Outputs"):
                        st.markdown(
                            f'<div class="result-block">'
                            f'Response ☈:'
                            f'<pre><code>{result.stdout}</code></pre>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
            elif error:
                st.error(f"命令执行失败！返回码：{error.returncode}")
                with st.expander("🐞$ Outputs"):
                    st.exception(error)
        st.write("## Step 3: Download MP3:")
        st.caption("选择csv文件")
        csv = st.text_input('',value=config["Temporary"]["PODCAST_CSV_PATH"])
        download = st.button("Download Episodes")
        if csv and download:
            ep_names,urls,audio_dir = redirect_audio.read_csv_url(csv)
            # 创建一个状态指示器
            with st.spinner("Processing audio redirects..."):
                # 调用函数，等待完成
                redirect_audio.get_redirect(ep_names,urls,audio_dir)
            # 完成后显示成功信息
            st.success(f"Audio Download processed successfully!\nPath: {config['Temporary']['audio_path']}")
    elif mode == '按标签爬取':
        st.write("按标签爬取.")
    elif mode == '按关键词搜索':
        st.write("按关键词搜索.")
