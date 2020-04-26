from example import *

TDS = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]

for _ in TDS:
    y = std_task(_, "output/test/")
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