import cv2
import os

# 输入视频文件路径
video_path = 'D:\\数学建模\\32.31.250.103\\1.mp4'

# 输出帧的保存文件夹
output_folder = 'frames'

# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 打开视频文件
cap = cv2.VideoCapture(video_path)

# 检查视频是否打开成功
if not cap.isOpened():
    print("无法打开视频文件")
    exit()

frame_count = 0

# 逐帧读取视频
while True:
    ret, frame = cap.read()  # ret是布尔值，frame是当前帧
    if not ret:
        break  # 如果读取失败（视频结束），退出循环

    # 保存每一帧为图像文件，格式为'frame_0.png', 'frame_1.png', ...
    frame_filename = os.path.join(output_folder, f'frame_{frame_count}.png')
    cv2.imwrite(frame_filename, frame)

    print(f"保存帧: {frame_filename}")
    frame_count += 1

# 释放视频捕获对象
cap.release()
print(f"总共保存了 {frame_count} 帧")
