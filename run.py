from example import *


def task(dir_path: str):
    TDS = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
    for _ in TDS:
        y = std_task(_, dir_path)
        while True:
            try:
                ti, td, pe, ty, ret = next(y)
                print("Time:%s  Traffic Density:%.2f  Permeability:%.2f"
                      % (ti, td, pe), ret)
                pass
            except StopIteration:
                break
            finally:
                pass
            pass
        pass
    pass


if __name__ == '__main__':
    path = "./output/data_%s/" % time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    task(path)
    os.system("""python analysis.py "%s" """ % path)
    pass