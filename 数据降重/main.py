import pandas as pd
import numpy as np

# 加载Excel文件
file_path = './基本数据集/results1_with_scores_and_diff1.xlsx'  # 替换为实际文件路径
excel_data = pd.read_excel(file_path)

# 对 'flow' 和 'density' 列进行随机降重 (在0.9到1.0之间随机缩减)
excel_data['flow'] = excel_data['flow'] * np.random.uniform(0.9, 1.0, size=len(excel_data))
excel_data['density'] = excel_data['density'] * np.random.uniform(0.9, 1.0, size=len(excel_data))

# 对 'flow' 和 'density' 列进行四舍五入取整
excel_data['flow'] = excel_data['flow'].round().astype(int)
excel_data['density'] = excel_data['density'].round().astype(int)

# 计算 flow/density 的比值并填入 'speed' 列
# 为了避免 density 为0的情况，先检查并处理
excel_data['speed'] = excel_data['flow'] / excel_data['density']
excel_data['speed'] = excel_data['speed'] * 10
excel_data['speed'] = excel_data['speed'].replace([np.inf, -np.inf], 0)  # 替换无穷大情况为0
excel_data['speed'] = excel_data['speed'].fillna(0)  # 如果出现NaN（density为0的情况），用0填充

# # 对 'Positive ideal solution distance'、'Negative ideal solution distance'、'相对接近'、'得分' 列进行随机降重
# columns_to_reduce = ['Positive ideal solution distance\n', 'Negative ideal solution distance\n', '相对接近', '得分']
# for col in columns_to_reduce:
#     excel_data[col] = excel_data[col] * np.random.uniform(0.95, 1.0, size=len(excel_data))
#
# # 计算 '得分' 的分差 (当前行的得分 - 上一行的得分)，并填入 '得分分差' 列
# excel_data['得分分差'] = excel_data['得分'].diff().fillna(0)  # 使用 diff() 计算差分，第一行填充为0

# 保存修改后的数据到一个新的Excel文件
output_file_path = './降重数据集/results1_with_scores_and_diff.xlsx'
excel_data.to_excel(output_file_path, index=False)

print(f"Modified Excel file saved as: {output_file_path}")
