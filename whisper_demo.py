import os
import openai

def readAudio(audio_path,save_path):
    
    audio_file = open(audio_path, "rb")
    transcript = openai.Audio.transcribe(
        model="whisper-1",
        file=audio_file,
        response_format="text",
        language="en"
    )
    with open(save_path,"w") as file:
        file.write(transcript)
    
    print("[ * ] Finished ReadAudio...")