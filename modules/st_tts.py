from azure_tts import azure_tts
import streamlit as st

def tts():
    st.header("👂🏻 Azure Speech - TTS")
    st.write("## Step 1: Initial Setup :")
    st.caption("Texts File")
    text_path = st.text_input('💡 输入口播稿 Path', '/Users/.../xxx.txt')
    output_path = st.text_input('💡 设置输出 Path', '/Users/.../xxx.mp3')
    
    if st.button("Run"):
        with open(text_path, 'r') as file:
            content = file.read()
        with st.spinner("Texting To Speech ..."):
            azure_tts(content,output_path)
        st.success('Text To Speech Successfully')