import copy
import time
from typing import List, Dict

import pandas as pd

from std_interface import *


class Car(CarInfo):
    """
    基础车类
    """

    def __init__(self, car_name: str, car_type: int, following_model: FollowingModel, expecting_headway: float,
                 limiting_acceleration: [float, float], limiting_speed: [float, float], stopping_distance: float,
                 observation_error: float, operation_error: float, response_time_delay: float,
                 car_color: [float, float, float], car_size: [float, float]):
        """
        构造函数
        初始化所有静态数据
        :param car_type: 车辆类型，str类型
        :param following_model: 跟驰模型，引用跟驰模型接口的实例类
        :param expecting_headway: 期望车头时距，float类型，单位s
        :param limiting_acceleration: 加速度范围，list类型，例如[最大减速度，最大加速度]，例如[-6，2]，单位m/s**2
        :param limiting_speed: 速度范围，list类型，例如[最小速度，最大速度]，例如[0，25]，单位m/s
        :param stopping_distance: 停车间距，float类型，跟驰车车头与前车车尾间距，单位m
        :param observation_error: 观测误差，float类型，范围[0,1]
        :param operation_error: 操作误差，float类型，范围[0,1]
        :param response_time_delay: 反应延迟，float类型，指一秒中的有效响应比例，范围[0,1]
        :param car_color: 车辆颜色，list类型，例如[0.5, 0.5, 0.5],rbg颜色，颜色范围[0,1]
        :param car_size: 车辆尺寸，list类型，例如[长度，宽度]，参考捷达尺寸[4.5,1.7]，单位m
        """
        super().__init__()
        self.name = car_name
        self.id = hash(time.time())
        time.sleep(0.001)
        self.car_type = car_type
        self.following_model = following_model
        self.init_location = float()
        self.init_speed = float()
        self.init_acceleration = float()
        self.expecting_headway = expecting_headway
        self.car_size = car_size  # [length, width]
        self.limiting_acceleration = limiting_acceleration
        self.limiting_speed = limiting_speed
        self.stopping_distance = stopping_distance
        self.observation_error = observation_error
        self.operation_error = operation_error
        self.response_time_delay = response_time_delay
        self.car_color = car_color

        self.real_mileage = 0
        self.real_location = self.init_location
        self.real_speed = self.init_speed
        self.real_acceleration = float()

        self.real_headway = float()
        self.real_spacing = float()
        self.real_speed_difference = float()
        self.real_acceleration_difference = float()

        self.preceding_car = self
        self.following_car = self

        self.is_linked = False
        self.is_initialized = False

        self.road_length = float()

        self.time = 0
        self._time = self.time
        self.real_position = 0
        self._real_position = 0

        self._real_mileage = 0
        self._real_location = self.init_location
        self._real_speed = self.init_speed
        self._real_acceleration = float()

        self._real_headway = float()
        self._real_spacing = float()
        self._real_speed_difference = float()
        self._real_acceleration_difference = float()
        self._response_time_delay = np.random.random() * self.response_time_delay

    def __call__(self):
        self.id = hash(time.time())
        time.sleep(0.001)

    def __repr__(self):
        return self.name

    def get_info(self):
        ret = CarInfo()
        ret.name = self.name
        ret.id = self.id
        ret.car_type = self.car_type
        ret.following_model = self.following_model
        ret.init_location = self.init_location
        ret.init_speed = self.init_speed
        ret.init_acceleration = self.init_acceleration
        ret.expecting_headway = self.expecting_headway
        ret.car_size = self.car_size
        ret.limiting_acceleration = self.limiting_acceleration
        ret.limiting_speed = self.limiting_speed
        ret.stopping_distance = self.stopping_distance
        ret.observation_error = self.observation_error
        ret.operation_error = self.operation_error
        ret.response_time_delay = self.response_time_delay
        ret.car_color = self.car_color

        ret.real_mileage = self.real_mileage
        ret.real_location = self.real_location
        ret.real_speed = self.real_speed
        ret.real_acceleration = self.real_acceleration

        ret.real_headway = self.real_headway
        ret.real_spacing = self.real_spacing
        ret.real_speed_difference = self.real_speed_difference
        ret.real_acceleration_difference = self.real_acceleration_difference

        ret.preceding_car = self.preceding_car
        ret.following_car = self.following_car

        ret.road_length = self.road_length

        ret.time = self.time
        ret.real_position = self.real_position
        return ret

    def initialize(self, loc: float, speed: float, acceleration: float, road_length: float):
        """
        动态变量初始化函数
        :param road_length:
        :param loc: 位置，float类型，单位m
        :param speed: 速度，float类型，单位m/s
        :param acceleration: 加速度，float类型，单位m/s**2
        :return:
        """
        self.init_location = loc
        self.real_location = loc
        self.real_position = loc
        self.init_speed = speed
        self.real_speed = speed
        self.init_acceleration = acceleration
        self.real_acceleration = acceleration
        self.road_length = road_length
        self.is_initialized = True
        pass

    def count_difference(self, location_correction: float):
        """
        差值计算
        :param location_correction: 位置修正，float类型，解决首车与尾车的位置计算偏差
        :return:
        """
        self.real_speed_difference = (
                self.preceding_car.real_speed
                - self.real_speed
        )
        self.real_acceleration_difference = (
                self.preceding_car.real_acceleration
                - self.real_acceleration
        )
        self.real_spacing = (
                self.preceding_car.real_location
                - self.preceding_car.car_size[0]
                - self.real_location
                + location_correction
        )

        def count_real_headway(dx: float, dv: float) -> float:
            re = float()
            if dv == 0:
                re = float("inf") * dx
            elif dv != 0:
                re = -dx / dv
                if re < 0:
                    re = float("inf")
                    pass

                if dx < 0:
                    re = -float("inf")
                    pass

            else:
                pass
            return re

        self.real_headway = count_real_headway(
            self.real_spacing,
            self.real_speed_difference
        )
        pass

    def link(self, following_car, preceding_car):
        """
        链接函数，链接跟驰车与前车
        :param following_car:
        :param preceding_car: 前车实例
        :return:
        """
        self.following_car = following_car
        self.preceding_car = preceding_car
        self.is_linked = True

    def update(self, step: float):
        """
        更新动态数据，此方法仅作为更新准备，并不会赋值
        :param step: 步长,float类型
        :return: 无
        """
        if self._response_time_delay > 0:
            self._response_time_delay -= 0.001
            _a = self._real_acceleration
        else:
            self._response_time_delay = self.response_time_delay
            _a = self.following_model(self)
            _a = self._check_acceleration(_a) * np.random.normal(1, self.operation_error)
            pass

        _a = self._check_acceleration(_a)
        _v = self.real_speed + step * _a
        _v = self._check_speed(_v)

        loc = self.real_location
        if _a == 0:
            dloc = _v * step
        else:
            dloc = (_v ** 2 - self.real_speed ** 2) / (2 * _a)
        loc = dloc + loc

        self._real_acceleration = _a
        self._real_speed = _v
        self._real_location = loc
        self._real_mileage += dloc

        self._time += step
        self._real_position = loc % self.road_length
        pass

    def apply(self):
        """
        更新赋值，此方法使用前应使用update做更新准备
        :return:
        """
        self.time = self._time
        self.real_acceleration = self._real_acceleration
        self.real_speed = self._real_speed
        self.real_location = self._real_location
        self.real_mileage = self._real_mileage
        self.real_position = self._real_position
        pass

    def switch_following_model(self, following_model: FollowingModel):
        self.following_model = following_model

    def get_difference(self):
        return np.array([self.real_spacing, self.real_speed_difference, self.real_acceleration_difference])

    def _check_acceleration(self, acceleration: float) -> float:
        if (self.real_speed <= self.limiting_speed[0] and acceleration < 0) \
                or \
                (self.real_speed >= self.limiting_speed[1] and acceleration > 0):
            acceleration = 0
            pass
        else:
            if acceleration < self.limiting_acceleration[0]:
                acceleration = self.limiting_acceleration[0]
            elif acceleration > self.limiting_acceleration[1]:
                acceleration = self.limiting_acceleration[1]
            else:
                pass
        return acceleration

    def _check_speed(self, speed: float) -> float:
        if speed < self.limiting_speed[0]:
            speed = self.limiting_speed[0]
        elif speed > self.limiting_speed[1]:
            speed = self.limiting_speed[1]
        else:
            pass
        return speed


class FVDModel(FollowingModel):
    def __init__(self):
        pass

    def _run(self, following_car: Car) -> float:
        b = 28
        alpha = 0.16
        beta = 1.1
        _lambda = 0.5
        optimal_speed = (
                0.5 * following_car.limiting_speed[1]
                * (np.tanh(following_car.real_spacing / b - beta) - np.tanh(-beta))
        )
        _a = (
                alpha * (optimal_speed - following_car.real_speed)
                + _lambda * following_car.real_speed_difference
        )
        # print(optimal_speed, _a)
        return _a

    pass


class GippsModel(FollowingModel):
    def _run(self, following_car: Car) -> float:
        e = ((following_car.limiting_acceleration[0] * following_car.response_time_delay) ** 2
             - following_car.limiting_acceleration[0]
             * (2 * (following_car.real_spacing
                     * np.random.normal(1, following_car.observation_error)
                     - following_car.stopping_distance)
                # - following_car.expecting_headway
                # * following_car.limiting_speed[1])
                - following_car.real_speed * following_car.response_time_delay
                - (following_car.preceding_car.real_speed
                   * np.random.normal(1, following_car.observation_error)) ** 2
                / following_car.preceding_car.limiting_acceleration[0]))
        if e < 0:
            e = 0
            pass
        v1 = (following_car.real_speed
              + 2.5
              * following_car.limiting_acceleration[1]
              * (1 - following_car.real_speed / following_car.limiting_speed[1])
              * (0.0025 + following_car.real_speed / following_car.limiting_speed[1]) ** 0.5)
        v2 = (following_car.limiting_acceleration[0] * following_car.response_time_delay + e ** 0.5)
        v = min(v1, v2)
        _a = (v - following_car.real_speed) / following_car.response_time_delay
        return _a

    pass


class IDMModel(FollowingModel):
    def __init__(self, beta=4):
        self.beta = beta

    def _run(self, following_car: Car) -> float:

        exp_spacing = (
                following_car.stopping_distance
                + following_car.real_speed
                * following_car.expecting_headway
                + following_car.real_speed
                * following_car.real_speed_difference * 0.5
                / abs(following_car.limiting_acceleration[1]
                      * following_car.limiting_acceleration[0]) ** 0.5
        )
        _a = float()
        if following_car.real_spacing > 0:
            _a = (
                    abs(following_car.limiting_acceleration[1])
                    * (1
                       - abs(following_car.real_speed
                             / following_car.limiting_speed[1]) ** self.beta
                       - abs(exp_spacing
                             / following_car.real_spacing
                             * np.random.normal(1, following_car.observation_error)) ** 2
                       )
            )
        elif following_car.real_spacing <= 0:
            _a = -float('inf')
        return _a

    pass


class PATHModelACC(FollowingModel):
    def __init__(self, k1=0.23, k2=0.07):
        self.k1 = k1
        self.k2 = k2

    def _run(self, following_car: Car) -> float:
        e = (
                following_car.real_spacing
                * np.random.normal(1, following_car.observation_error)
                - following_car.stopping_distance
                - following_car.expecting_headway
                * following_car.real_speed
        )
        _a = (self.k1 * e
              + self.k2
              * following_car.real_speed_difference
              * np.random.normal(1, following_car.observation_error))
        return _a

    pass


class PATHModelCACC(FollowingModel):
    def __init__(self, k1=1.1, k2=0.23, k3=0.07):
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3

    def _run(self, following_car: Car) -> float:
        e = (
                following_car.real_spacing
                * np.random.normal(1, following_car.observation_error)
                - following_car.stopping_distance
                - following_car.expecting_headway
                * following_car.real_speed
        )
        _a = (self.k1
              * following_car.preceding_car.real_acceleration
              * np.random.normal(1, following_car.observation_error)
              + self.k2 * e
              + self.k3
              * following_car.real_speed_difference
              * np.random.normal(1, following_car.observation_error))
        return _a

    pass


class IDMWithGipps(FollowingModel):
    def __init__(self, beta=4):
        self.beta = beta
        self.idm = IDMModel(beta)
        self.gipps = GippsModel()

    def _run(self, following_car) -> float:
        re = 0
        a1 = self.idm(following_car)
        a2 = self.gipps(following_car)
        t = np.min((0, a1, a2))
        if t == 0:
            re = a1
        elif t != 0:
            re = t
        else:
            pass
        return re


class PATHModelACCWithGipps(FollowingModel):
    def __init__(self, k1=0.23, k2=0.07):
        self.k1 = k1
        self.k2 = k2
        self.path_acc = PATHModelACC(k1, k2)
        self.gipps = GippsModel()

    def _run(self, following_car) -> float:
        re = 0
        a1 = self.path_acc(following_car)
        a2 = self.gipps(following_car)
        t = np.min((0, a1, a2))
        if t == 0:
            re = a1
        elif t != 0:
            re = t
        else:
            pass
        return re


class PATHModelCACCWithGipps(FollowingModel):
    def __init__(self, k1=1.1, k2=0.23, k3=0.07):
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3
        self.path_cacc = PATHModelCACC(k1, k2, k3)
        self.gipps = GippsModel()

    def _run(self, following_car) -> float:
        re = 0
        a1 = self.path_cacc(following_car)
        a2 = self.gipps(following_car)
        t = np.min((0, a1, a2))
        if t == 0:
            re = a1
        elif t != 0:
            re = t
        else:
            pass
        return re


class IntelligentDrivingCarModel(FollowingModel):
    dict_mode = {0: 'head', 1: 'body', 2: 'tail'}

    def __init__(self, model: FollowingModel, alpha: float = 0.5, beta: float = 1, gamma: float = 1, name='IDC',
                 max_search_index=5):
        self.model = model
        self.name = name
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.max_search_index = max_search_index
        pass

    def _run(self, following_car: Car) -> float:

        _following_car = following_car.get_info()
        a = 0

        cars = []
        tmp_car = following_car
        for i in range(self.max_search_index + 1):
            cars.append(tmp_car)
            tmp_car = tmp_car.preceding_car
            pass

        head = []
        body = []
        tail = []

        tag = 2
        for c in cars[:-1]:
            if tag == 2 and type(c.preceding_car.following_model) == type(self):
                t = c.get_difference()
                tail.append(t + np.sum(tail, 0))
                continue
            elif tag == 2 and type(c.preceding_car.following_model) != type(self):
                tag = 1
                t = c.get_difference()
                body.append(t + np.sum(tail, 0))
                continue
            elif tag == 1 and type(c.preceding_car.following_model) != type(self):
                t = c.get_difference()
                body.append(t + np.sum(tail, 0) + np.sum(body, 0))
                continue
            elif tag == 1 and type(c.preceding_car.following_model) == type(self):
                tag = 0
                t = c.get_difference()
                head.append(t + np.sum(tail, 0) + np.sum(body, 0))
                continue
            else:
                pass
            pass

        if len(body) == 0 or len(head) == 0:
            a = self.model(_following_car)
            pass
        elif type(_following_car.following_car.following_model) is not type(self):
            # head
            if len(tail) != 0:
                vector_pre_car = tail[0]
            else:
                vector_pre_car = body[0]
            vector_mean_body = np.mean(body, 0)
            vector_head = head[0]
            dx = np.max((
                vector_pre_car[0]
                + self.gamma
                * np.min((0, vector_pre_car[1], vector_mean_body[1], vector_head[1]))
                , 0
            ))
            dv = vector_pre_car[1] + self.gamma * np.min(
                (0, vector_pre_car[2], vector_mean_body[2], vector_head[2])
            )
            da = np.min((vector_pre_car[2], vector_mean_body[2], vector_head[2]))
            _following_car.real_spacing = dx
            _following_car.real_speed_difference = dv
            _following_car.real_acceleration_difference = da
            a = self.model(_following_car)
            pass
        elif type(_following_car.following_car.following_model) is type(self):
            # tail
            if len(tail) != 0:
                vector_pre_car = tail[0]
            else:
                vector_pre_car = body[0]
            vector_mean_body = np.mean(body, 0)
            vector_head = head[0]
            t = _following_car.expecting_headway
            t = t - self.alpha * t * np.tanh(self.beta * (np.max((vector_pre_car[1],
                                                                 vector_mean_body[1],
                                                                 vector_head[1]))
                                                          + self.gamma
                                                          * np.max((vector_pre_car[2],
                                                                   vector_mean_body[2],
                                                                   vector_head[2]))))
            _following_car.expecting_headway = t
            a = self.model(_following_car)
            pass
        else:
            print("ERROR")
            exit()
        return a


SET_INIT_LOC_TYPE = {"L", "U", "R"}

SET_INIT_CARS_TYPE = {"U", "R"}


class Fleet:
    def __init__(self,
                 car_num: int,
                 init_type_car: str,
                 proportion: Dict,
                 road_length: float,
                 init_type_loc: str):
        self.car_num = car_num
        self.init_type_car = init_type_car
        self.proportion = proportion
        self.road_length = road_length
        self.init_type_loc = init_type_loc
        self.cars = self._init_cars()
        self._make_cars_link()
        self._init_loc()
        self._index = np.linspace(1, self.car_num, self.car_num)

    def update(self, step):
        for c in self.cars:
            c.update(step)
            pass

        for c in self.cars:
            c.apply()
            pass

        for c in self.cars[:-1]:
            c.count_difference(location_correction=0)
            pass

        self.cars[-1].count_difference(location_correction=self.road_length)
        pass

    def _init_cars(self) -> List[Car]:
        proportion_keys = list(self.proportion.keys())
        proportion_values = list(self.proportion.values())
        re = []
        if self.init_type_car is "U":
            pass
        elif self.init_type_car is "R":
            list_rand_num = []
            num_and_car = []
            list_num = list(
                np.array(np.array(proportion_values)
                         * self.car_num
                         / np.sum(proportion_values),
                         dtype=int)
            )
            for ln in list_num:
                list_rand_num.append(list(np.random.rand(ln)))
                pass
            for lrn, c in zip(list_rand_num, proportion_keys):
                for u in lrn:
                    num_and_car.append([u, copy.deepcopy(c)])
                    pass
                pass
            num_and_car = np.array(num_and_car)
            index = np.argsort(num_and_car[:, 0])
            for _i in index:
                re.append(num_and_car[_i, 1])
        else:
            pass

        for r in re:
            r()

        return re

    def _make_cars_link(self):
        index = len(self.cars)
        for x in range(index - 1):
            self.cars[x].link(self.cars[x - 1], self.cars[x + 1])
            pass
        self.cars[-1].link(self.cars[-2], self.cars[0])
        pass

    def _init_loc(self) -> None:
        if self.init_type_loc is "L":
            num = len(self.cars)
            self.cars[0].initialize(0, 0, 0, self.road_length)
            for _i in range(1, num):
                self.cars[_i].initialize(
                    self.cars[_i - 1].init_location
                    + self.cars[_i - 1].stopping_distance
                    + self.cars[_i].car_size[0],
                    0,
                    0,
                    self.road_length
                )
                pass
            pass
        elif self.init_type_loc is "U":
            num = len(self.cars)
            loc = np.linspace(0, self.road_length, num)
            for cl, car in zip(loc, self.cars):
                car.initialize(cl, 0, 0, self.road_length)
                pass
            pass
        elif self.init_type_loc is "R":
            pass
        else:
            pass

        for c in self.cars[:-1]:
            c.count_difference(location_correction=0)
            pass
        self.cars[-1].count_difference(location_correction=self.road_length)
        pass

    def get_cars_location(self) -> List:
        re = []
        for c in self.cars:
            re.append(c.real_location)
            pass
        return re

    def get_cars_speed(self) -> List:
        re = []
        for c in self.cars:
            re.append(c.real_speed)
            pass
        return re

    def get_cars_acceleration(self) -> List:
        re = []
        for c in self.cars:
            re.append(c.real_acceleration)
            pass
        return re

    def get_cars_headway(self) -> List:
        re = []
        for c in self.cars:
            re.append(c.real_headway)
            pass
        return re

    def get_cars_spacing(self) -> List:
        re = []
        for c in self.cars:
            re.append(c.real_spacing)
            pass
        return re

    def get_cars_type(self) -> List:
        re = []
        for c in self.cars:
            re.append(c.car_type)
            pass
        return re

    def get_data(self) -> pd.DataFrame:
        re = []
        rows = np.linspace(1, self.car_num, self.car_num, dtype=np.int)
        cols = ['sub_index', 'time', 'type', 'pos', 'v', 'a', 'dl', 'dv', 'da', 'hw']
        for c in self.cars:
            tmp = [c.time, c.car_type, c.real_position, c.real_speed, c.real_acceleration, c.real_spacing,
                   c.real_speed_difference, c.real_acceleration_difference, c.real_headway]
            re.append(tmp)
            pass
        re = np.c_[np.array([self._index]).T, re]
        re = pd.DataFrame(re, index=rows, columns=cols, dtype='double')
        re.index.name = 'index'
        return re

    def get_data_by_list(self) -> List:
        re = []
        for c in self.cars:
            tmp = [c.time, c.id, c.car_type, c.real_position, c.real_speed, c.real_acceleration, c.real_spacing,
                   c.real_speed_difference, c.real_acceleration_difference, c.real_headway]
            re.append(tmp)
            pass
        re = np.c_[np.array([self._index]).T, re]
        return re
