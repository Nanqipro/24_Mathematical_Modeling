import pandas as pd

# 假设原始数据保存在一个文件中
input_file = 'C:\\Users\\wu\\Desktop\\czq\\108_2.txt'

# 用于存储最终结果的字典
traffic_data = {'timestamps': [], 'vehicle_count': []}

# 读取原始数据文件
with open(input_file, 'r') as file:
    lines = file.readlines()

# 遍历文件内容并提取时间戳和车辆计数
for i in range(0, len(lines), 4):  # 每三行是一组数据
    timestamp_line = lines[i]
    vehicle_count_line = lines[i+2]

    # 提取时间戳
    if "Timestamp:" in timestamp_line:
        timestamp = timestamp_line.split('Timestamp:')[1].strip()
    else:
        print(f"错误: 行 {i+1} 不是有效的时间戳格式: {timestamp_line}")
        continue  # 跳过这一行

    # 提取车辆计数
    if "Vehicle Count:" in vehicle_count_line:
        vehicle_count = int(vehicle_count_line.split('Vehicle Count:')[1].strip())
    else:
        print(f"错误: 行 {i+3} 不是有效的车辆计数格式: {vehicle_count_line}")
        continue  # 跳过这一行

    # 将时间戳和车辆计数存储到字典中
    traffic_data['timestamps'].append(timestamp)
    traffic_data['vehicle_count'].append(vehicle_count)

# 将字典转换为DataFrame
df = pd.DataFrame(traffic_data)

# 定义输出CSV文件路径
output_csv_file = '108traffic_data2.csv'

# 将 DataFrame 写入 CSV 文件
df.to_csv(output_csv_file, index=False)

print(f"数据已成功写入 {output_csv_file}")
