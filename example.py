import os
import sys
from time import time

import matplotlib.pyplot as plt
from progressbar import *

from moos import *

STEP = 0.001  # ms

SIMULATION_TIME = 600  # sec
SAMPLING_TIME = 300  # sec
SAMPLING_INTERVAL = 100  # ms

MAX_SPEED = 120
LIMITING_SPEED = [0, MAX_SPEED / 3.6]
LIMITING_ACCELERATION = [-2, 1]
CAR_SIZE = [4.5, 1.7]
CYCLE_INDEX = int(SIMULATION_TIME / STEP)

CAR_NUM = 50

DICT_FOLLOWING_MODEL = dict(FVD=FVDModel(),
                            GIPPS=GippsModel(),
                            IDM=IDMModel(),
                            PATH_ACC=PATHModelACC(),
                            PATH_CACC=PATHModelCACC())

DICT_CAR_TYPE = {
    "TEST": 00,
    "HDC": 10,
    "SDC": 20,
    "IDC": 30
}


def std_task(traffic_density: float, dir_path: str):
    road_length = 1000 * CAR_NUM / traffic_density

    HDC = Car(car_name='HDC',
              car_type=DICT_CAR_TYPE["HDC"],
              following_model=DICT_FOLLOWING_MODEL["IDM"],
              car_size=CAR_SIZE,
              expecting_headway=3,
              limiting_acceleration=LIMITING_ACCELERATION,
              limiting_speed=LIMITING_SPEED,
              stopping_distance=1,
              observation_error=0.05,
              operation_error=0.05,
              response_time_delay=0.67,
              car_color=(1, 0, 0),
              road_length=road_length)

    SDC = Car(car_name='SDC',
              car_type=DICT_CAR_TYPE["SDC"],
              following_model=DICT_FOLLOWING_MODEL["PATH_CACC"],
              car_size=CAR_SIZE,
              expecting_headway=2,
              limiting_acceleration=LIMITING_ACCELERATION,
              limiting_speed=LIMITING_SPEED,
              stopping_distance=1,
              observation_error=0.005,
              operation_error=0.005,
              response_time_delay=0.02,
              car_color=(1, 0, 0),
              road_length=road_length)

    # 精度0.02 不可更改
    proportions = [{HDC: 1.00, SDC: 0.00},
                   {HDC: 0.90, SDC: 0.10},
                   {HDC: 0.80, SDC: 0.20},
                   {HDC: 0.70, SDC: 0.30},
                   {HDC: 0.60, SDC: 0.40},
                   {HDC: 0.50, SDC: 0.50},
                   {HDC: 0.40, SDC: 0.60},
                   {HDC: 0.30, SDC: 0.70},
                   {HDC: 0.20, SDC: 0.80},
                   {HDC: 0.10, SDC: 0.90},
                   {HDC: 0.00, SDC: 1.00}]

    for p in proportions:
        start_tag = time.time()

        permeability = p[SDC]

        cars = Fleet(CAR_NUM, "R", p, road_length, "L")
        dump = []
        end_tag = time.time()
        yield (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
               traffic_density,
               permeability,
               'message',
               "1.初始化完成.用时%.2fsec." % (end_tag - start_tag))

        yield (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
               traffic_density,
               permeability,
               'message',
               "2.仿真开始.运行目标:+%.2fsec." % (STEP * CYCLE_INDEX))
        start_tag = time.time()
        bar = ProgressBar()
        dump.append(cars.get_data_by_list())
        for _ in bar(range(int(CYCLE_INDEX / SAMPLING_INTERVAL))):
            for j in range(SAMPLING_INTERVAL):
                cars.update(STEP)
                pass
            dump.append(cars.get_data_by_list())
            pass

        end_tag = time.time()

        yield (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
               traffic_density,
               permeability,
               'message',
               ("3.仿真完成.运行目标+%.2fsec,用时:%.2fsec,数据内存使用:%.2fKB."
                % (CYCLE_INDEX * STEP, end_tag - start_tag, sys.getsizeof(dump) / 1024)))

        start_tag = time.time()

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            pass

        file_name = ('TD_%.2f_PE_%.2f' % (traffic_density, permeability))
        cols = ['sub_index', 'time', 'id', 'type', 'pos', 'v', 'a', 'dl', 'dv', 'da', 'hw']
        dump = np.vstack(dump)
        dump = pd.DataFrame(dump, columns=cols, dtype='double')
        dump.index.name = 'index'
        dump.to_csv(dir_path + 'data_' + file_name + '.csv', sep=',')
        # np.save(file_name, dump)

        data = np.array(dump['v'][dump['time'] > SAMPLING_TIME]) * 3.6
        mean = np.mean(data)
        x = np.linspace(0, MAX_SPEED, int(MAX_SPEED / 10) + 1)
        y, _ = np.histogram(data, bins=x)
        y = y / y.sum()
        x = x[:-1] + 5
        plt.figure(figsize=(5, 3), dpi=100)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.bar(x, y)
        plt.plot(x, y, ls="-", c="black", label='速度-频率曲线')
        plt.axvline(x=mean, ls="-", c="red", label='平均速度')
        plt.title('速度-频率曲线(TD=%.2f,PE=%.2f)'
                  % (traffic_density, permeability))
        plt.xlabel('速度')
        plt.ylabel('频率')
        plt.xticks(np.linspace(0, MAX_SPEED, int(MAX_SPEED / 10) + 1))
        plt.yticks(np.linspace(0, 1, 5))
        plt.ylim(0, 1)
        plt.xlim(0, MAX_SPEED)
        plt.legend()
        plt.tight_layout()
        plt.savefig(dir_path + file_name + '.jpg')
        plt.close()

        end_tag = time.time()

        yield (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
               traffic_density,
               permeability,
               'message',
               ("4.数据持久化完成.生成数据文件%s.csv(%.2fMB),用时:%.2fsec."
                % (file_name,
                   os.path.getsize(dir_path + 'data_' + file_name + '.csv') / (1024 ** 2),
                   end_tag - start_tag)))

        yield (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
               traffic_density,
               permeability,
               'data',
               dump)