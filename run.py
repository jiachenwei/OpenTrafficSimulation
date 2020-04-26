from example import *


def task(dir_path: str):
    os.system("start python m_threads.py -1 '%s'" % dir_path)
    os.system("start python m_threads.py -2 '%s'" % dir_path)
    os.system("start python m_threads.py -3 '%s'" % dir_path)
    os.system("start python m_threads.py -4 '%s'" % dir_path)


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
    os.system("""python analysis.py -a "%s" """ % path)
    pass
