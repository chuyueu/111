import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt


# 插值函数
def new_fuel_interpolation(aoa, FTD_fuel, DATA_tab):
    """
    :param aoa: 遥测攻角
    :param FTD_fuel: 遥测油量
    :param DATA_tab: 插值表
    :return:
    """
    temp = [aoa,
            FTD_fuel,
            np.interp(FTD_fuel, DATA_tab['状态油量[kg]'][::-1], DATA_tab['重心X[m]'][::-1]),
            np.interp(FTD_fuel, DATA_tab['状态油量[kg]'][::-1], DATA_tab['重心Y[m]'][::-1]),
            np.interp(FTD_fuel, DATA_tab['状态油量[kg]'][::-1], DATA_tab['重心Z[m]'][::-1]),
            np.interp(FTD_fuel, DATA_tab['状态油量[kg]'][::-1], DATA_tab['IXX[kg*m2]'][::-1]),
            np.interp(FTD_fuel, DATA_tab['状态油量[kg]'][::-1], DATA_tab['IYY[kg*m2]'][::-1]),
            np.interp(FTD_fuel, DATA_tab['状态油量[kg]'][::-1], DATA_tab['IZZ[kg*m2]'][::-1]),
            np.interp(FTD_fuel, DATA_tab['状态油量[kg]'][::-1], DATA_tab['IXY[kg*m2]'][::-1]),
            np.interp(FTD_fuel, DATA_tab['状态油量[kg]'][::-1], DATA_tab['IXZ[kg*m2]'][::-1]),
            np.interp(FTD_fuel, DATA_tab['状态油量[kg]'][::-1], DATA_tab['IYZ[kg*m2]'][::-1])]
    df = np.array(temp).T
    # df = pd.DataFrame(df, columns=['X_CG[m]', 'Y_CG[m]', 'Z_CG[m]',
    #                                'I_XX[kg*m2]', 'I_YY[kg*m2]', 'I_ZZ[kg*m2]',
    #                                'I_XY[kg*m2]', 'I_XZ[kg*m2]', 'I_YZ[kg*m2]'])
    return df
    # # 导出新的插值表
    # df.to_excel('C:\\Users\\A.FYYX-2021DGSRZC\\Desktop\\new_fuel_interpolate1.xls')  # 带index
    # df.to_excel('C:\\Users\\A.FYYX-2021DGSRZC\\Desktop\\new_fuel_interpolate2.xls', index=False)  # 不带index


# 读取数据
def get_data(filename, sheetname):
    """
    :param filename: xls文件名
    :param sheetname: 工作表名称
    :return: 中心油箱 左油箱 右油箱
    """
    data = pd.read_excel(filename, sheet_name=sheetname)
    data_center_fuel_tank = data.iloc[0:101, 2:12]
    data_left_fuel_tank = data.iloc[102:203, 2:12]
    data_right_fuel_tank = data.iloc[204:305, 2:12]
    return data_center_fuel_tank, data_left_fuel_tank, data_right_fuel_tank


def get_aoa(temp_aoa):
    aoa = 0.0
    if temp_aoa < 0.0:
        aoa = 0.0
    elif temp_aoa > 9.0:
        aoa = 9.0
    else:
        aoa = temp_aoa
    return aoa


# 以中央油箱为例
# 按AOA插值
# ===========================================================
# 根据AOA选择要使用的工作表(包含三个油箱的数据) data为tuple类型
filename = 'fuel property.xls'
new_table_5 = np.array([0] * 11)  # α weight 3*CG 6*I 共11列
new_table = np.array([0] * 11)  # α weight 3*CG 6*I 共11列
data_0 = get_data(filename, sheetname='0')
data_3 = get_data(filename, sheetname='3')
data_5 = get_data(filename, sheetname='5')
data_7 = get_data(filename, sheetname='7')
data_9 = get_data(filename, sheetname='9')
time_start = time.time()
AOA = get_aoa(1.2)  # 例:想要得到 AOA = 4 时的插值表
test_fuel = 12121.2
AOA_low = 0.0  # 初始AOA左限
AOA_high = 0.0  # 初始AOA右限
if (AOA > 0.0) & (AOA < 3.0):
    AOA_low = 0.0
    AOA_high = 3.0
    data1 = data_0
    data2 = data_3
elif (AOA > 3.0) & (AOA < 5.0):
    AOA_low = 3.0
    AOA_high = 5.0
    data1 = data_3
    data2 = data_5
elif (AOA > 5.0) & (AOA < 7.0):
    AOA_low = 5.0
    AOA_high = 7.0
    data1 = data_5
    data2 = data_7
else:
    AOA_low = 7.0
    AOA_high = 9.0
    data1 = data_7
    data2 = data_9
fuel_df_AOA_low_center = data1[0]  # AOA = low
fuel_df_AOA_high_center = data2[0]  # AOA = high
fuel_df_AOA_low_left = data1[1]  # AOA = low
fuel_df_AOA_high_left = data2[1]  # AOA = high
fuel_df_AOA_low_right = data1[2]  # AOA = low
fuel_df_AOA_high_right = data2[2]  # AOA = high
# 用2个表进行插值，得到指定攻角的插值表
new_table_2 = np.array([0] * 11)
fuel_weight = data_0[0]['状态油量[kg]']
for i in range(len(data1[0])):
    temp = np.array([AOA,
                     fuel_weight[i],
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_center['重心X[m]'][i], fuel_df_AOA_high_center['重心X[m]'][i]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_center['重心Y[m]'][i], fuel_df_AOA_high_center['重心Y[m]'][i]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_center['重心Z[m]'][i], fuel_df_AOA_high_center['重心Z[m]'][i]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_center['IXX[kg*m2]'][i], fuel_df_AOA_high_center['IXX[kg*m2]'][i]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_center['IYY[kg*m2]'][i], fuel_df_AOA_high_center['IYY[kg*m2]'][i]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_center['IZZ[kg*m2]'][i], fuel_df_AOA_high_center['IZZ[kg*m2]'][i]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_center['IXY[kg*m2]'][i], fuel_df_AOA_high_center['IXY[kg*m2]'][i]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_center['IXZ[kg*m2]'][i], fuel_df_AOA_high_center['IXZ[kg*m2]'][i]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_center['IYZ[kg*m2]'][i], fuel_df_AOA_high_center['IYZ[kg*m2]'][i]]),
                     ])
    new_table_2 = np.row_stack((new_table_2, temp))
new_table_2 = new_table_2[1:len(new_table_2)+1, :]
df_2_center = pd.DataFrame(new_table_2, columns=['AOA[°]', '状态油量[kg]',
                                                 '重心X[m]', '重心Y[m]', '重心Z[m]',
                                                 'IXX[kg*m2]', 'IYY[kg*m2]', 'IZZ[kg*m2]',
                                                 'IXY[kg*m2]', 'IXZ[kg*m2]', 'IYZ[kg*m2]'])
temp_table = new_fuel_interpolation(AOA, test_fuel, df_2_center)
new_table = np.row_stack((new_table, temp_table))
new_table = new_table[1:len(new_table_5) + 1, :]
new_center = pd.DataFrame(new_table, columns=['AOA[°]', '状态油量[kg]',
                                             '重心X[m]', '重心Y[m]', '重心Z[m]',
                                             'IXX[kg*m2]', 'IYY[kg*m2]', 'IZZ[kg*m2]',
                                             'IXY[kg*m2]', 'IXZ[kg*m2]', 'IYZ[kg*m2]'])
new_center.to_excel('C:\\Users\\A.FYYX-2021DGSRZC\\Desktop\\AOA_first.xls')  # 带index

for i in range(len(data1[0])):
    temp = np.array([AOA,
                     fuel_weight[i],
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_left['重心X[m]'][i+102], fuel_df_AOA_high_left['重心X[m]'][i+102]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_left['重心Y[m]'][i+102], fuel_df_AOA_high_left['重心Y[m]'][i+102]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_left['重心Z[m]'][i+102], fuel_df_AOA_high_left['重心Z[m]'][i+102]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_left['IXX[kg*m2]'][i+102], fuel_df_AOA_high_left['IXX[kg*m2]'][i+102]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_left['IYY[kg*m2]'][i+102], fuel_df_AOA_high_left['IYY[kg*m2]'][i+102]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_left['IZZ[kg*m2]'][i+102], fuel_df_AOA_high_left['IZZ[kg*m2]'][i+102]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_left['IXY[kg*m2]'][i+102], fuel_df_AOA_high_left['IXY[kg*m2]'][i+102]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_left['IXZ[kg*m2]'][i+102], fuel_df_AOA_high_left['IXZ[kg*m2]'][i+102]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_left['IYZ[kg*m2]'][i+102], fuel_df_AOA_high_left['IYZ[kg*m2]'][i+102]]),
                     ])
    new_table_2 = np.row_stack((new_table_2, temp))
new_table_2 = new_table_2[1:len(new_table_2)+1, :]
# time_start = time.time()
df_2_left = pd.DataFrame(new_table_2, columns=['AOA[°]', '状态油量[kg]',
                                                 '重心X[m]', '重心Y[m]', '重心Z[m]',
                                                 'IXX[kg*m2]', 'IYY[kg*m2]', 'IZZ[kg*m2]',
                                                 'IXY[kg*m2]', 'IXZ[kg*m2]', 'IYZ[kg*m2]'])
temp_table = new_fuel_interpolation(AOA, test_fuel, df_2_left)
new_table = np.row_stack((new_table, temp_table))
new_table = new_table[1:len(new_table_5) + 1, :]
new_table_left = pd.DataFrame(new_table, columns=['AOA[°]', '状态油量[kg]',
                                                 '重心X[m]', '重心Y[m]', '重心Z[m]',
                                                 'IXX[kg*m2]', 'IYY[kg*m2]', 'IZZ[kg*m2]',
                                                 'IXY[kg*m2]', 'IXZ[kg*m2]', 'IYZ[kg*m2]'])

for i in range(len(data1[0])):
    temp = np.array([AOA,
                     fuel_weight[i],
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_right['重心X[m]'][i+204], fuel_df_AOA_high_right['重心X[m]'][i+204]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_right['重心Y[m]'][i+204], fuel_df_AOA_high_right['重心Y[m]'][i+204]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_right['重心Z[m]'][i+204], fuel_df_AOA_high_right['重心Z[m]'][i+204]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_right['IXX[kg*m2]'][i+204], fuel_df_AOA_high_right['IXX[kg*m2]'][i+204]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_right['IYY[kg*m2]'][i+204], fuel_df_AOA_high_right['IYY[kg*m2]'][i+204]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_right['IZZ[kg*m2]'][i+204], fuel_df_AOA_high_right['IZZ[kg*m2]'][i+204]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_right['IXY[kg*m2]'][i+204], fuel_df_AOA_high_right['IXY[kg*m2]'][i+204]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_right['IXZ[kg*m2]'][i+204], fuel_df_AOA_high_right['IXZ[kg*m2]'][i+204]]),
                     np.interp(AOA, [AOA_low, AOA_high], [fuel_df_AOA_low_right['IYZ[kg*m2]'][i+204], fuel_df_AOA_high_right['IYZ[kg*m2]'][i+204]]),
                     ])
    new_table_2 = np.row_stack((new_table_2, temp))
new_table_2 = new_table_2[1:len(new_table_2)+1, :]
# time_start = time.time()
df_2_right = pd.DataFrame(new_table_2, columns=['AOA[°]', '状态油量[kg]',
                                                 '重心X[m]', '重心Y[m]', '重心Z[m]',
                                                 'IXX[kg*m2]', 'IYY[kg*m2]', 'IZZ[kg*m2]',
                                                 'IXY[kg*m2]', 'IXZ[kg*m2]', 'IYZ[kg*m2]'])
temp_table = new_fuel_interpolation(AOA, test_fuel, df_2_right)
new_table = np.row_stack((new_table, temp_table))
new_table = new_table[1:len(new_table_5) + 1, :]
new_table_right = pd.DataFrame(new_table, columns=['AOA[°]', '状态油量[kg]',
                                                 '重心X[m]', '重心Y[m]', '重心Z[m]',
                                                 'IXX[kg*m2]', 'IYY[kg*m2]', 'IZZ[kg*m2]',
                                                 'IXY[kg*m2]', 'IXZ[kg*m2]', 'IYZ[kg*m2]'])
time_end = time.time()
# print('time cost', time_end-time_start, 's')

# 以 AOA=9° center_fuel_tank 测试

# def interpolate(data_fuel_tank):
#     empty = 0
#     full = 12719
#     n = 1  # 插值精确度
#     kind = 'cubic'  # 插值类型
#     new_fuel_weight = np.linspace(full, empty, full * n + 1)
#
#     # 抽取数据
#     data_fuel_tank_weight = data_fuel_tank['状态油量[kg]']
#     data_fuel_tank_X_CG = data_fuel_tank['重心X[m]']
#     data_fuel_tank_Y_CG = data_fuel_tank['重心Y[m]']
#     data_fuel_tank_Z_CG = data_fuel_tank['重心Z[m]']
#     data_fuel_tank_I_XX = data_fuel_tank['IXX[kg*m2]']
#     data_fuel_tank_I_YY = data_fuel_tank['IYY[kg*m2]']
#     data_fuel_tank_I_ZZ = data_fuel_tank['IZZ[kg*m2]']
#     data_fuel_tank_I_XY = data_fuel_tank['IXY[kg*m2]']
#     data_fuel_tank_I_XZ = data_fuel_tank['IXZ[kg*m2]']
#     data_fuel_tank_I_YZ = data_fuel_tank['IYZ[kg*m2]']
#
#     # 对I_XX进行插值
#     fig = plt.figure()
#     ax1 = fig.add_subplot(331)
#     ax1.plot(data_fuel_tank_weight, data_fuel_tank_I_XX, '-r', label='Origin')
#     f = interpolate.interp1d(data_fuel_tank_weight, data_fuel_tank_I_XX, kind=kind)
#     I_XX_Cubic_interpolation = f(new_fuel_weight)
#     ax1.plot(new_fuel_weight, I_XX_Cubic_interpolation, label=str(kind))
#     plt.legend(loc='best')
#     plt.title('I_XX')
#
#     # 对I_YY进行插值
#     ax2 = fig.add_subplot(332)
#     ax2.plot(data_fuel_tank_weight, data_fuel_tank_I_YY, '-r', label='Origin')
#     f = interpolate.interp1d(data_fuel_tank_weight, data_fuel_tank_I_YY, kind=kind)
#     I_YY_Cubic_interpolation = f(new_fuel_weight)
#     ax2.plot(new_fuel_weight, I_YY_Cubic_interpolation, label=str(kind))
#     plt.legend(loc='best')
#     plt.title('I_YY')
#
#     # 对I_ZZ进行插值
#     ax3 = fig.add_subplot(333)
#     ax3.plot(data_fuel_tank_weight, data_fuel_tank_I_ZZ, '-r', label='Origin')
#     f = interpolate.interp1d(data_fuel_tank_weight, data_fuel_tank_I_ZZ, kind=kind)
#     I_ZZ_Cubic_interpolation = f(new_fuel_weight)
#     ax3.plot(new_fuel_weight, I_ZZ_Cubic_interpolation, label=str(kind))
#     plt.legend(loc='best')
#     plt.title('I_ZZ')
#
#     # 对I_XY进行插值
#     ax4 = fig.add_subplot(334)
#     ax4.plot(data_fuel_tank_weight, data_fuel_tank_I_XY, '-r', label='Origin')
#     f = interpolate.interp1d(data_fuel_tank_weight, data_fuel_tank_I_XY, kind=kind)
#     I_XY_Cubic_interpolation = f(new_fuel_weight)
#     ax4.plot(new_fuel_weight, I_XY_Cubic_interpolation, label=str(kind))
#     plt.legend(loc='best')
#     plt.title('I_XY')
#
#     # 对I_XZ进行插值
#     ax5 = fig.add_subplot(335)
#     ax5.plot(data_fuel_tank_weight, data_fuel_tank_I_XZ, '-r', label='Origin')
#     f = interpolate.interp1d(data_fuel_tank_weight, data_fuel_tank_I_XZ, kind=kind)
#     I_XZ_Cubic_interpolation = f(new_fuel_weight)
#     ax5.plot(new_fuel_weight, I_XZ_Cubic_interpolation, label=str(kind))
#     plt.legend(loc='best')
#     plt.title('I_XZ')
#
#     # 对I_YZ进行插值
#     ax6 = fig.add_subplot(336)
#     ax6.plot(data_fuel_tank_weight, data_fuel_tank_I_YZ, '-r', label='Origin')
#     f = interpolate.interp1d(data_fuel_tank_weight, data_fuel_tank_I_YZ, kind=kind)
#     I_YZ_Cubic_interpolation = f(new_fuel_weight)
#     ax6.plot(new_fuel_weight, I_YZ_Cubic_interpolation, label=str(kind))
#     plt.legend(loc='best')
#     plt.title('I_YZ')
#
#     # 对X_CG进行插值
#     ax7 = fig.add_subplot(337)
#     ax7.plot(data_fuel_tank_weight, data_fuel_tank_X_CG, '-r', label='Origin')
#     f = interpolate.interp1d(data_fuel_tank_weight, data_fuel_tank_X_CG, kind=kind)
#     X_CG_Cubic_interpolation = f(new_fuel_weight)
#     ax7.plot(new_fuel_weight, X_CG_Cubic_interpolation, label=str(kind))
#     plt.legend(loc='best')
#     plt.title('X_CG')
#
#     # 对Y_CG进行插值
#     ax8 = fig.add_subplot(338)
#     ax8.plot(data_fuel_tank_weight, data_fuel_tank_Y_CG, '-r', label='Origin')
#     f = interpolate.interp1d(data_fuel_tank_weight, data_fuel_tank_Y_CG, kind=kind)
#     Y_CG_Cubic_interpolation = f(new_fuel_weight)
#     ax8.plot(new_fuel_weight, Y_CG_Cubic_interpolation, label=str(kind))
#     plt.legend(loc='best')
#     plt.title('Y_CG')
#
#     # 对Z_CG进行插值
#     ax9 = fig.add_subplot(339)
#     ax9.plot(data_fuel_tank_weight, data_fuel_tank_Z_CG, '-r', label='Origin')
#     f = interpolate.interp1d(data_fuel_tank_weight, data_fuel_tank_Z_CG, kind=kind)
#     Z_CG_Cubic_interpolation = f(new_fuel_weight)
#     ax9.plot(new_fuel_weight, Z_CG_Cubic_interpolation, label=str(kind))
#     plt.legend(loc='best')
#     plt.title('Z_CG')
#     plt.show()
#     # 拼接形成新的插值表
#     interpolation = np.c_[new_fuel_weight,
#                           X_CG_Cubic_interpolation,
#                           Y_CG_Cubic_interpolation,
#                           Z_CG_Cubic_interpolation,
#                           I_XX_Cubic_interpolation,
#                           I_YY_Cubic_interpolation,
#                           I_ZZ_Cubic_interpolation,
#                           I_XY_Cubic_interpolation,
#                           I_XZ_Cubic_interpolation,
#                           I_YZ_Cubic_interpolation]
#     return np.matrix(interpolation).T
