import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import subprocess,os
from modules import st_crawler
from modules import st_speech2text
from modules import st_tts
from modules import st_sovits
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

st.set_page_config(
    page_icon="🦄",
    page_title="Podcaster",
    layout="wide",
    initial_sidebar_state="auto",
)
# # horizontal menu
# selected = option_menu(None, ["Home", "Crawler", "Tasks", 'Settings'], 
#                        icons=['house', 'browser-chrome', "list-task", 'gear'], 
#                        menu_icon="cast", default_index=0, orientation="horizontal")
st.markdown('<style>div.stButton > button {float: right;}</style>', unsafe_allow_html=True)
st.markdown(
    """
    <style>
    .result-block {
        max-height: 360px;
        overflow-y: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# as sidebar menu
with st.sidebar:
    selected = option_menu("Podcaster", ["Home", "Crawler",'Speech-to-Text','TTS','So-Vits','Settings'], 
                           icons=['house', 'browser-chrome','ear','volume-up','music-note','gear'], menu_icon="cast", default_index=1)

if selected == "Home":
    col1,col2 = st.columns(2)
    with col2:
        """> 作者: Your Name  
    创建日期: 2023-05-30  
    版权声明: 版权归作者所有"""

    with col1:
        title_style = '''
            font-size: 48px;
            color: #282a36;
            margin-right: 10px
        '''
        text_css = """background: linear-gradient(to right,#ff79c6, #ffff, #ff79c6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-right: 10px
            margin: 0px
        """
        # 使用 HTML 标签和 CSS 样式创建包含背景图片的区域
        st.markdown(
            f'''
            <div >
                <h1 style="text-align: left;{title_style};margin:0;">☞  🦄 Podcaster</h1>
                <p style="text-align: right;{text_css};margin:0;">Coded by unicorn</p>
            </div>
            ''',
            unsafe_allow_html=True
        )
elif selected == "Crawler":
    st_crawler.crawler()
    
elif selected == "Speech-to-Text":
    st_speech2text.speech2text()
elif selected == "TTS":
    st_tts.tts()
elif selected == "So-Vits":
    st_sovits.sovits()
elif selected == "Settings":
    "# 参数设置"
    with st.form("参数设置"):

        # Azure Speech
        st.caption("Azure Speech Settings:")
        speech_key_placeholder = 'fxxxxx...'
        service_regio_placeholder = 'eastus'
        if config['API']['SPEECH_KEY']:
            speech_key_placeholder = config['API']['SPEECH_KEY']
        if config['API']['SPEECH_REGION']:
            service_regio_placeholder = config['API']['SPEECH_REGION']
        speech_key = st.text_input('Azure Speech API Key', speech_key_placeholder)
        speech_region = st.text_input('Azure Speech Region', service_regio_placeholder)
        
        # Openai
        st.caption("OpenAI Settings:")
        openai_api_key_placeholder = 'st-xxxxx...'
        if config['API']['OPENAI_API_KEY']:
            speech_key_placeholder = config['API']['OPENAI_API_KEY']
        openai_api = st.text_input('OpenAI API Key',openai_api_key_placeholder)
        
        run_button = st.form_submit_button("Save")
        if run_button:
            try:
                # 修改配置文件中的参数
                config.set('API', 'SPEECH_KEY',speech_key )
                config.set('API', 'SPEECH_REGION',speech_region )
                config.set('API', 'OPENAI_API_KEY',openai_api )
                # 将修改后的配置写回配置文件
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                    
                st.success(f"""
                        SPEECH_KEY is set to: {config['API']['SPEECH_KEY']}\n
                        SPEECH_REGION is set to: {config['API']['SPEECH_REGION']}\n
                        OPENAI_API_KEY is set to: {config['API']['OPENAI_API_KEY']}
                    """)

                success = True
            except subprocess.CalledProcessError as e:
                # 输出错误信息和回显信息
                st.error(f"命令执行失败！返回码：{e.returncode}")
                st.exception(e)
                error = e