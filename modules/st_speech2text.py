import streamlit as st
import openai,os,subprocess
from whisper_demo import readAudio
from openai_translate import translate
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
openai.api_key = config["API"]["openai_api_key"]

def speech2text():
    st.header("👂🏻 Speech To Text")
    st.write("## Step 1: Initial Setup :")
    mode = st.selectbox("",["Select File","Select Dir"])
    if mode == "Select File":
        st.caption("MP3 File")
        audio = st.text_input('💡 输入Auido Path', '/Users/.../xxx.mp3')
    elif mode == "Select Dir":
        st.caption("MP3 Files Dir")
        audio_dir = st.text_input('💡 输入Auido Dir', '/Users/xxx/')
        audio = f"{audio_dir}*.mp3"
    st.caption("Output Text File Name")
    name = st.text_input('💡 输入口播稿名称', 'xxx.txt')
    
    if st.button("Start"):
        text_save_path = f"./results/audio2txt/{name}"
        translated_path = f"./results/audio2txt/translated/{text_save_path.split('/')[-1]}"
        config.set('Temporary', 'txt_original_path', f"{os.getcwd()}{text_save_path.lstrip('.')}")
        config.set('Temporary', 'txt_translated_path', f"{os.getcwd()}{translated_path.lstrip('.')}")
        # 将修改后的配置写回配置文件
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        print("[ + ] 开始转录audio...")
        with st.spinner("Reading Audio ..."):
            readAudio(audio,text_save_path)
            st.success("Read Audio To English Succseefully")
        print("[ + ] 开始翻译字幕...")
        with st.spinner("Translating Audio ..."):
            translate(text_save_path,"zh")
            st.success("Translate Audio To Chinese Succseefully")
            st.code(f"Original Path: {config['Temporary']['txt_original_path']}")
            st.code(f"Translated Path: {config['Temporary']['txt_translated_path']}")
        original = f"open {config['Temporary']['txt_original_path']}"
        translated = f"open {config['Temporary']['txt_original_path']}"
        if st.button("打开转录稿"):
            os.startfile(original)
        if st.button("打开翻译稿"):
            os.startfile(translated)

        
        