import pandas as pd
import os
"""
data = {
            '播客名称': podcastname_list,
            '简介': intro_list,
            '标签': tagcsv,
            '评分': ls_list,
            '排名': top_list,
            '剧集名': episode_titles,
            '剧集介绍': ep_intros,
            'audio链接': audio_hrefs
        }
file_path = "xx/xx/xx.csv"
================================================================
func:
    write_to_csv 
        - return file_path
    rename 
        - return df

"""


def write_to_csv(data, file_path):
    df = pd.DataFrame(data)
    if os.path.isfile(file_path) and os.stat(file_path).st_size > 0:
        df.to_csv(file_path, mode='a', index=False, header=False)
        print("f[ * ] 成功追加内容到{file_path}")
    else:
        # 将DataFrame写入CSV文件
        df.to_csv(file_path, index=False)
        print("f[ * ] 成功写入内容到{file_path}")
    return file_path


def rename(file_path):
    # 读取 CSV 文件，跳过第一行
    df = pd.read_csv(file_path)

    # 获取需要修改的列名
    column_name = '剧集名'
    # 获取列数据的长度
    length = len(df[column_name])
    # 修改列数据
    df[column_name] = [f"{str(length-i)}_{value}" for i,
                       value in enumerate(df[column_name])]
    # # 保存修改后的数据到新的 CSV 文件
    # df.to_csv('/Users/jadeunicorn/Jade/Work/Python/Projects/Others/results/numbered.csv', index=False)
    return df
