import pandas as pd
import os
def write_to_csv(data,file_path):
        df = pd.DataFrame(data)
        if os.path.isfile(file_path) and os.stat(file_path).st_size > 0:
                df.to_csv(file_path, mode='a', index=False, header=False)
        else:
                # 将DataFrame写入CSV文件
                df.to_csv(file_path, index=False)
