import openai,os
from whisper_demo import readAudio
from openai_translate import translate
openai.api_key = os.getenv("OPENAI_API_KEY")

audio_path = "/Users/jadeunicorn/Downloads/test.mp3"
text_save_path = "./results/audio2txt/test.txt"

print("[ + ] 开始转录audio...")
readAudio(audio_path,text_save_path)
print("[ + ] 开始翻译字幕...")
translate(text_save_path,"zh")