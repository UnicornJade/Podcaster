import os
import torch
import torchaudio
from tqdm import tqdm


class VAD:
    """
    ================================================================
    /只用输入源音频路径
    1. 语音活跃检测
    2. 获取所有语音判断音频
    3. 合并音频至10s左右
    ================================================================
    vad = VAD('test.mp3')
    vad.vad()
    vad.combine()
    """
    folder_path = ''
    slicer_dir = ''

    def __init__(self, audiopath, model, utils, podcast_name):
        self.audiopath = audiopath  # vad待处理的音频文件路径
        self.model = model
        self.utils = utils
        self.podcast_name = podcast_name

    def vad(self):
        audiopath = self.audiopath
        model = self.model
        utils = self.utils
        podcast_name = self.podcast_name
        # import faulthandler; faulthandler.enable()
        SAMPLING_RATE = 16000*3
        torch.set_num_threads(1)

        # download example
        # torch.hub.download_url_to_file('https://models.silero.ai/vad_models/en.wav', 'en_example.wav')

        # USE_ONNX = False  # change this to True if you want to test onnx model
        # if USE_ONNX:
        #     os.system("pip install -q onnxruntime")

        # model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
        #                               model='silero_vad',
        #                               force_reload=True,
        #                               onnx=USE_ONNX)

        (get_speech_timestamps,
         save_audio,
         read_audio,
         VADIterator,
         collect_chunks) = utils

        wav = read_audio(audiopath, sampling_rate=SAMPLING_RATE)
        # print("已读取音频: "+audiopath)
        # get speech timestamps from full audio file
        speech_timestamps = get_speech_timestamps(
            wav, model, sampling_rate=SAMPLING_RATE)
        # pprint(speech_timestamps)
        # save_audio('only_speech.wav',
        #            collect_chunks(speech_timestamps, wav),
        #            sampling_rate=SAMPLING_RATE
        # )
        # 读取音频文件

        # wav, sr = torchaudio.load('your_audio_file.wav')

        # # 按每十分钟进行切分
        # segment_duration = sec  # 切分的时长，单位：秒，即十分钟
        # segment_samples = int(segment_duration * SAMPLING_RATE)  # 切分的采样点数量
        #
        # num_segments = math.ceil(len(wav) / segment_samples)  # 切分后的段数
        #
        # segments = []  # 用于存储切分的段
        #
        # for i in range(num_segments):
        #     start_samples = i * segment_samples
        #     end_samples = min((i + 1) * segment_samples, len(wav))
        #     audio_segment = wav[start_samples:end_samples]
        #     segments.append(audio_segment)

        slicer_dir = os.path.splitext(os.path.basename(audiopath))[0]
        if not os.path.exists(f"./results/slicer/{podcast_name}/{slicer_dir}"):
            os.makedirs(f"./results/slicer/{podcast_name}/{slicer_dir}")
        self.folder_path = f"./results/slicer/{podcast_name}/{slicer_dir}"
        self.slicer_dir = slicer_dir
        # 保存所有段到文件
        for i, segment in tqdm(enumerate(speech_timestamps)):
            start_time = segment['start']
            end_time = segment['end']
            audio_segment = wav[start_time:end_time]
            torchaudio.save(
                f'./results/slicer/{podcast_name}/{slicer_dir}/{os.path.splitext(os.path.basename(audiopath))[0]}_{i}.mp3', audio_segment.unsqueeze(0), SAMPLING_RATE)

        # print("Finished")
        """# 定义最大时长为10秒
        max_duration = sec

        # 初始化计时器和当前段音频
        current_duration = 0
        current_audio = []

        # 遍历每个语音活跃时间戳
        for i, segment in enumerate(speech_timestamps):
            start_time = segment['start']
            end_time = segment['end']
            duration = end_time - start_time

            # 如果当前段音频加上当前时间戳的时长超过最大时长，则保存当前段音频并重置计时器和当前段音频
            if current_duration + duration > max_duration*SAMPLING_RATE:
                if current_audio:
                    # 保存当前段音频
                    torchaudio.save(f'./results/slicer/{slicer_dir}/{os.path.splitext(os.path.basename(audiopath))[0]}_{i}.mp3', current_audio, SAMPLING_RATE)
                    # 重置计时器和当前段音频
                    current_duration = 0
                    current_audio = []

            # 将当前时间戳的音频段添加到当前段音频
            current_audio.append(wav[start_time:end_time])
            # 更新计时器
            current_duration += duration

        # 保存最后一段音频
        if current_audio:
            torchaudio.save(f'./results/slicer/{slicer_dir}/{os.path.splitext(os.path.basename(audiopath))[0]}_{i+1}.mp3',current_audio, SAMPLING_RATE)

        # print("Finished")"""

    def combine(self, folder_path=None, slicer_dir=None):
        podcast_name = self.podcast_name

        if folder_path is None or slicer_dir is None:
            folder_path = self.folder_path
            slicer_dir = self.slicer_dir
        """
        # 读取音频文件
        waveform, sample_rate = torchaudio.load("test.mp3")
        # 获取音频时长（单位：秒）
        duration = waveform.size(1) / sample_rate
        print(f"音频时长：{duration} 秒")
        """
        max_sec = 1000
        audios = []
        t = 0
        i = 0
        # 遍历文件夹下的所有文件
        for file_name in tqdm(os.listdir(folder_path)):
            # 构造音频文件的完整路径
            file_path = os.path.join(folder_path, file_name)

            # 检查文件是否为音频文件
            if file_name.endswith((".wav", ".mp3", ".flac")):
                try:
                    # 读取音频文件
                    waveform, sample_rate = torchaudio.load(file_path)

                    # 计算音频时长（单位：秒）
                    duration = waveform.size(1) / sample_rate
                    if t > max_sec:
                        audio_combined = torch.cat(audios, dim=1)
                        if not os.path.exists(f"./results/slicer/out/{podcast_name}/{slicer_dir}"):
                            os.makedirs(
                                f"./results/slicer/out/{podcast_name}/{slicer_dir}")
                        torchaudio.save(
                            f'./results/slicer/out/{podcast_name}/{slicer_dir}/{slicer_dir}_{i}.mp3', audio_combined, sample_rate)
                        i += 1
                        audios = []
                        t = 0
                    if duration <= max_sec:
                        audios.append(waveform)
                        t += duration
                    else:
                        if len(audios) > 0:
                            audio_combined = torch.cat(audios, dim=1)
                            if not os.path.exists(f"./results/slicer/out/{podcast_name}/{slicer_dir}"):
                                os.makedirs(
                                    f"./results/slicer/out/{podcast_name}/{slicer_dir}")
                            torchaudio.save(
                                f'./results/slicer/out/{podcast_name}/{slicer_dir}/{slicer_dir}_{i}.mp3', audio_combined, sample_rate)
                            i += 1
                            audios = []
                            t = 0
                        if not os.path.exists(f"./results/slicer/out/{podcast_name}/{slicer_dir}"):
                            os.makedirs(
                                f"./results/slicer/out/{podcast_name}/{slicer_dir}")
                        torchaudio.save(
                            f'./results/slicer/out/{podcast_name}/{slicer_dir}/{slicer_dir}_{i}.mp3', waveform, sample_rate)
                except Exception as e:
                    print(f"读取音频文件出错: {file_name}")
                    print(f"错误信息: {str(e)}")
                    print()
        print(f"[ * ] {os.path.basename(folder_path)}.mp3 预处理成功")

        # print("[ * ] 音频后处理完成")
