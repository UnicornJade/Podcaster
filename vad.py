import os,math
SAMPLING_RATE = 44100
import torch,torchaudio
torch.set_num_threads(1)

# download example
# torch.hub.download_url_to_file('https://models.silero.ai/vad_models/en.wav', 'en_example.wav')

USE_ONNX = False # change this to True if you want to test onnx model
if USE_ONNX:
    os.system("pip install -q onnxruntime")

model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_vad',
                              force_reload=True,
                              onnx=USE_ONNX)

(get_speech_timestamps,
        save_audio,
        read_audio,
        VADIterator,
        collect_chunks) = utils
        
wav = read_audio('test.mp3', sampling_rate=SAMPLING_RATE)
print("已读取音频")
# get speech timestamps from full audio file
speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=SAMPLING_RATE)
print(speech_timestamps)
# save_audio('only_speech.wav',
#            collect_chunks(speech_timestamps, wav),
#            sampling_rate=SAMPLING_RATE
# )
# 读取音频文件

# wav, sr = torchaudio.load('your_audio_file.wav')

# 按每十分钟进行切分
segment_duration = 600  # 切分的时长，单位：秒，即十分钟
segment_samples = int(segment_duration * SAMPLING_RATE)  # 切分的采样点数量

num_segments = math.ceil(len(wav) / segment_samples)  # 切分后的段数

segments = []  # 用于存储切分的段

for i in range(num_segments):
    start_samples = i * segment_samples
    end_samples = min((i + 1) * segment_samples, len(wav))
    audio_segment = wav[start_samples:end_samples]
    segments.append(audio_segment)

# 保存所有段到文件
for i, segment in enumerate(segments):
    torchaudio.save(f'segment_{i}.wav', segment, SAMPLING_RATE)
print("Finished")

# wav, sr = torchaudio.load('/Users/jadeunicorn/Downloads/test.mp3')