import  pandas as pd
def rename(path):
    # 读取 CSV 文件，跳过第一行
    df = pd.read_csv(path)
    
    # 获取需要修改的列名
    column_name = '剧集名'
    # 获取列数据的长度
    length = len(df[column_name])
    # 修改列数据
    df[column_name] = [f"{str(length-i)}_{value}" for i, value in enumerate(df[column_name])]
    # # 保存修改后的数据到新的 CSV 文件
    # df.to_csv('/Users/jadeunicorn/Jade/Work/Python/Projects/Others/results/numbered.csv', index=False)
    return df