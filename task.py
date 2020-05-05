import os
import sys

from matplotlib import pyplot as plt
from progressbar import *

from example import *
from usr_example import *


def std_task_scene(proportion: dict, traffic_density: float, dir_path: str):
    road_length = 1000 * CAR_NUM / traffic_density

    start_tag = time.time()

    permeability = 1 - list(proportion.values())[0]

    cars = Fleet(CAR_NUM, "R", proportion, road_length, "L")
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
    data[data > MAX_SPEED] = MAX_SPEED
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
    pass


def std_task(proportions: list, traffic_densities: list, dir_path: str):
    for td in traffic_densities:
        for p in proportions:
            task = std_task_scene(p, td, dir_path)
            while True:
                try:
                    ti, td, pe, ty, ret = next(task)
                    print("Time:%s  Traffic Density:%.2f  Permeability:%.2f"
                          % (ti, td, pe))
                    print(ret)
                except StopIteration:
                    break
                finally:
                    pass
                pass
            pass
        pass
    pass


if __name__ == '__main__':
    y = std_task_scene({HDC: 0.7, IDC_CACC: 0.3}, 20, 'output/test3/')
    while True:
        try:
            ti, td, pe, ty, ret = next(y)
            print("Time:%s  Traffic Density:%.2f  Permeability:%.2f"
                  % (ti, td, pe))
            print(ret)
        except StopIteration:
            break
        finally:
            pass
        pass
    pass
