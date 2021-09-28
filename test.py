import pandas as pd
import numpy as np
from test_2sheet import new_fuel_interpolation, get_data, get_aoa
import time


def judge_aoa(AOA, tank_data):
    """
    :param AOA: 遥测的攻角
    :param tank_data: 某个油箱在 AOA = 0,3,5,7,9时的质量特性
    :return: 某个油箱的两个已知攻角插值表
    """
    if (AOA > 0.0) & (AOA < 3.0):
        AOA_low = 0.0
        AOA_high = 3.0
        data1 = tank_data[0]
        data2 = tank_data[1]
    elif (AOA > 3.0) & (AOA < 5.0):
        AOA_low = 3.0
        AOA_high = 5.0
        data1 = tank_data[1]
        data2 = tank_data[2]
    elif (AOA > 5.0) & (AOA < 7.0):
        AOA_low = 5.0
        AOA_high = 7.0
        data1 = tank_data[2]
        data2 = tank_data[3]
    else:
        AOA_low = 7.0
        AOA_high = 9.0
        data1 = tank_data[3]
        data2 = tank_data[4]
    return data1, data2, AOA_low, AOA_high


# 读插值表
file_name = filename = 'fuel property.xls'
data_9_center = get_data(filename, sheetname='9')[0]
data_7_center = get_data(filename, sheetname='7')[0]
data_5_center = get_data(filename, sheetname='5')[0]
data_3_center = get_data(filename, sheetname='3')[0]
data_0_center = get_data(filename, sheetname='0')[0]
data_center = [data_0_center, data_3_center, data_5_center, data_7_center, data_9_center]
# 左油箱
data_9_left = get_data(filename, sheetname='9')[1]
data_7_left = get_data(filename, sheetname='7')[1]
data_5_left = get_data(filename, sheetname='5')[1]
data_3_left = get_data(filename, sheetname='3')[1]
data_0_left = get_data(filename, sheetname='0')[1]
data_left = [data_0_left, data_3_left, data_5_left, data_7_left, data_9_left]
# 右油箱
data_9_right = get_data(filename, sheetname='9')[2]
data_7_right = get_data(filename, sheetname='7')[2]
data_5_right = get_data(filename, sheetname='5')[2]
data_3_right = get_data(filename, sheetname='3')[2]
data_0_right = get_data(filename, sheetname='0')[2]
data_right = [data_0_right, data_3_right, data_5_right, data_7_right, data_9_right]
# 插值计算
time_start = time.time()
AOA_weight_interp = np.array([0]*11)
aoa = 1.2
fuel = 12121.2
aoa = get_aoa(aoa)
data_C = judge_aoa(aoa, data_center)
data_L = judge_aoa(aoa, data_left)
data_R = judge_aoa(aoa, data_right)


def AOA_weight_interp(aoa, fuel, data):
    weight_interp_low = new_fuel_interpolation(aoa, fuel, data[0])
    weight_interp_high = new_fuel_interpolation(aoa, fuel, data[1])
    interpolate = np.array([aoa,
                            fuel,
                            np.interp(aoa, [data[2], data[3]], [weight_interp_low[2], weight_interp_high[2]]),
                            np.interp(aoa, [data[2], data[3]], [weight_interp_low[3], weight_interp_high[3]]),
                            np.interp(aoa, [data[2], data[3]], [weight_interp_low[4], weight_interp_high[4]]),
                            np.interp(aoa, [data[2], data[3]], [weight_interp_low[5], weight_interp_high[5]]),
                            np.interp(aoa, [data[2], data[3]], [weight_interp_low[6], weight_interp_high[6]]),
                            np.interp(aoa, [data[2], data[3]], [weight_interp_low[7], weight_interp_high[7]]),
                            np.interp(aoa, [data[2], data[3]], [weight_interp_low[8], weight_interp_high[8]]),
                            np.interp(aoa, [data[2], data[3]], [weight_interp_low[9], weight_interp_high[9]]),
                            np.interp(aoa, [data[2], data[3]], [weight_interp_low[10], weight_interp_high[10]])
                            ])
    df = interpolate.reshape(1, 11)
    df = pd.DataFrame(df, columns=['aoa', 'fuel', 'xcg', 'ycg', 'zcg', 'ixx', 'iyy', 'izz', 'ixy', 'ixz', 'iyz'])
    return df
    # df.to_excel('C:\\Users\\A.FYYX-2021DGSRZC\\Desktop\\weight_first.xls')  # 带index


center_tank = AOA_weight_interp(aoa, fuel, data_C)
left_tank = AOA_weight_interp(aoa, fuel, data_L)
right_tank = AOA_weight_interp(aoa, fuel, data_R)
# 转换坐标系
# time_mid = time.time()


def transfer(data):
    data_Ixx = data['ixx'] + data['fuel'] * (data['ycg']**2 + data['zcg']**2)
    data_Iyy = data['iyy'] + data['fuel'] * (data['xcg']**2 + data['zcg']**2)
    data_Izz = data['izz'] + data['fuel'] * (data['xcg']**2 + data['ycg']**2)
    data_Ixy = data['ixy'] + data['fuel'] * data['xcg'] * data['ycg']
    data_Ixz = data['ixz'] + data['fuel'] * data['xcg'] * data['zcg']
    data_Iyz = data['iyz'] + data['fuel'] * data['ycg'] * data['zcg']
    return data_Ixx, data_Iyy, data_Izz, data_Ixy, data_Ixz, data_Iyz


a = transfer(left_tank)
b = transfer(center_tank)
c = transfer(right_tank)
time_end = time.time()
print('time cost', time_end-time_start, 's')
