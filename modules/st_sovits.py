import  streamlit as st
import subprocess
def sovits():
    st.header("☊ So-VITS")
    st.write("## 💡 安装依赖:")
    st.code("""
        # 克隆github仓库
        git clone https://github.com/svc-develop-team/so-vits-svc -b 4.0
        cd ./so-vits-svc
        pip uninstall -y torchdata torchtext
        pip install --upgrade pip setuptools numpy numba
        pip install pyworld praat-parselmouth fairseq tensorboardX torchcrepe librosa==0.9.1
        pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 torchaudio==0.13.1+cu117 --extra-index-url https://download.pytorch.org/whl/cu117
        # 在Windows上，你可以从 aria2 的官方网站下载预编译的二进制文件，并手动安装。
        brew install aria2
        aria2c --console-log-level=error -c -x 16 -k 1M -s 16 https://ibm.ent.box.com/shared/static/z1wgl1stco8ffooyatzdwsqn2psd9lrr -o checkpoint_best_legacy_500.pt -d /content/so-vits-svc/hubert
    """,language='bash')
    st.write("## 预配置:")
    st.markdown("""
        1. model(G_x.pt)h 放在 so-vits-svc/logs/44k/
        2. config(config.json) 放在 so-vits-svc/configs/
        3. 待处理音频放在 so-vits-svc/raw/
    """)
    with st.form("参数设置"):
        c1,c2 = st.columns(2)
        with c1:
            st.write("## 合成音频(推理)")
            st.caption("需要将音频上传到so-vits-svc/raw 文件夹下, 然后设置模型路径、配置文件路径、合成的音频名称")
            model_path = st.text_input("model_path","logs/44k/sunyz/G_80000.pth")
            config_path = st.text_input("config_path","configs/config_sun.json")
            clean_names = st.text_input("clean_names","wohuideng.wav")
            spk_list = st.text_input("spk_list","sunyz")
            trans = st.slider("trans",-8,+8)
        with c2:
            st.write("## 聚类音色泄漏控制")
            st.caption("0为完全不使用聚类，1为只使用聚类，通常设置0.5即可")
            cluster_infer_ratio = st.select_slider("cluster_infer_ratio",["0","0.5","1"])
            slice_db = st.slider("slice_db",-100,+100)
            wav_format = st.selectbox("wav_format",["wav"])
            wav_output = st.text_input("wav_output",f"/content/so-vits-svc/results/{clean_names}_{trans}key_{spk_list}.{wav_format}")
        
        if st.form_submit_button("Synthesis"):
            command = f'python /content/so-vits-svc/inference_main.py -m {model_path} -c {config_path} -n "{clean_names}" -t {trans} -s {spk_list}  -cr {cluster_infer_ratio} -sd {slice_db} -wf {wav_format}'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
                