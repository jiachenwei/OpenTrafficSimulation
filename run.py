from example import *
from usr_example import *
import os


def task(dir_path: str, cpu_core_num: int = 4):
    if cpu_core_num == 1:
        os.system("start python m_threads.py -1 %s" % dir_path)
    elif cpu_core_num == 2:
        os.system("start python m_threads.py -21 %s" % dir_path)
        os.system("start python m_threads.py -22 %s" % dir_path)
    elif cpu_core_num == 4:
        os.system("start python m_threads.py -41 %s" % dir_path)
        os.system("start python m_threads.py -42 %s" % dir_path)
        os.system("start python m_threads.py -43 %s" % dir_path)
        os.system("start python m_threads.py -44 %s" % dir_path)


if __name__ == '__main__':
    if not os.path.exists("./output/"):
        os.makedirs("./output/")
        pass

    path = "./output/data_%s" % time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    tmp_path = path
    count = 1

    while os.path.exists(tmp_path):
        tmp_path = path + '_' + str(count)
        count += 1
        pass

    path = tmp_path + '/'
    os.makedirs(path)
    task(path)
    pass
