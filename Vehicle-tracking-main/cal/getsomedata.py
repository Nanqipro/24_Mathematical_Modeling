import pandas as pd

df = pd.read_csv(r"C:\Users\wu\Desktop\czq\103merged_traffic_data.csv")

# 假设时间间隔为10秒钟
time_interval_seconds = 10
road_length_meters = 20  # 车道长度为15米

# 计算流量 (单位时间内通过的车辆数)
df['flow_rate'] = df['vehicle_count'] / time_interval_seconds

# 计算密度 (每公里内的车辆数)
df['density'] = (df['vehicle_count'] / road_length_meters) * 1000

# 计算速度 (流量与密度的比率)
df['speed'] = df['flow_rate'] / df['density']

# 显示结果
print(df)
