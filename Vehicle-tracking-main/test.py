from datetime import datetime, timedelta

# 输入文件路径
input_file = 'C:\\Users\\wu\\Desktop\\czq\\103detection_results1.txt'
# 输出文件路径
output_file = 'C:\\Users\\wu\\Desktop\\czq\\103_1.txt'

# 初始时间戳
initial_time = datetime(2024, 5, 1, 12, 56, 47)
# 时间间隔为10秒
time_increment = timedelta(seconds=10)

# 读取原始数据文件
with open(input_file, 'r') as file:
    lines = file.readlines()

# 创建输出文件并写入带时间戳的数据
with open(output_file, 'w') as file:
    current_time = initial_time
    for i in range(0, len(lines), 3):  # 每组是两行，但我们按三行处理，避免有额外的空行
        # 确保我们不会越界
        if i + 1 < len(lines):
            # 获取当前时间戳的字符串表示
            timestamp_str = current_time.strftime('%Y-%m-%d %H:%M:%S')

            # 写入时间戳
            file.write(f'Timestamp: {timestamp_str}\n')
            # 写入帧信息和车辆计数信息
            file.write(lines[i])  # 写入"Frame X Results"行
            file.write(lines[i + 1])  # 写入"Vehicle Count"行
            # 跳过可能存在的空行
            if i + 2 < len(lines) and lines[i + 2].strip() == "":
                file.write("\n")
            # 时间增加10秒
            current_time += time_increment
print("已成功为每一帧添加时间戳并保存到新的文件中。")