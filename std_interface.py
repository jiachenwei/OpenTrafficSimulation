import abc
import numpy as np


class FollowingModel(metaclass=abc.ABCMeta):
    """
    跟驰模型接口类
    """

    def __call__(self, following_car):
        return self._run(following_car)

    @abc.abstractmethod
    def _run(self, following_car) -> float:
        """
        跟驰模型接口类虚函数，必须重载。
        跟驰模型计算入口
        在此方法中，可以调用CarInfo中所有变量
        :param following_car: 跟驰车实例类，类型为Car
        :return: 返回加速度，浮点类型，单位m/s**2
        """

    pass


class CarInfo(metaclass=abc.ABCMeta):
    def __init__(self):
        self.name = str()  # 车辆名称
        self.id = None  # 车辆ID，内置生成，不可赋值
        self.car_type = None  # int类型，车辆类型，00、10、20、30内置占用，选择其他数字
        self.following_model = FollowingModel  # 跟驰模型
        self.init_location = float()  # 初始位置，自动生成，不可赋值
        self.init_speed = float()  # 初始速度，自动生成，不可赋值
        self.init_acceleration = float()  # 初始加速度，自动生成，不可赋值
        self.expecting_headway = float()  # 期望车头时距，单位s
        self.car_size = [float(), float()]  # 车辆尺寸[length, width]，单位m
        self.limiting_acceleration = [float(), float()]  # 限制加速度[减速度（负值），加速度]，单位m/s
        self.limiting_speed = [float(), float()]  # 限制速度[最小速度，最大速度]，单位m/s**2
        self.stopping_distance = float()  # 停车间距/安全间距，单位m
        self.observation_error = float()  # 观测误差
        self.operation_error = float()  # 操作误差
        self.response_time_delay = float()  # 响应延迟
        self.car_color = [float(), float(), float()]  # 车辆颜色OpenCVRGB色彩[]

        self.real_mileage = 0  # 真实里程，单位m
        self.real_location = self.init_location  # 真实位置，单位m
        self.real_speed = self.init_speed  # 真实速度，单位m/s
        self.real_acceleration = float()  # 真实加速度，单位m/s**2

        self.real_headway = float()  # 真实车头时距，单位s
        self.real_spacing = float()  # 真实车头车尾间隔，单位m
        self.real_speed_difference = float()  # 真实速度差，单位m/s
        self.real_acceleration_difference = float()  # 真实加速度差，单位m/s**2

        self.preceding_car = self  # 指定前车，若无特殊需要，自动生成
        self.following_car = self  # 指定后车，若无特殊需要，自动生成

        self.road_length = float()  # 道路长度，单位m，应该制定车流密度，与仿真车辆数，则自动生成道路长度

        self.time = 0  # 模拟时间，自动生成，不可赋值
        self.real_position = 0  # 真实道路位置，单位m


# 如何输入自己的跟驰模型，例如
class MyFollowingModel(FollowingModel):  # 首先需要继承FollowingModel接口
    def __init__(self, b: float = 28, alpha: float = 0.16, beta: float = 1.1, _lambda: float = 0.5):
        """
        构造函数，如果需要在实例化时传参，则可以借助此方法。
        注意：此方法非虚函数，不需要一定重载。
        b: float = 28的意思是变量，b默认类型float，默认值为28
        此外外部参数必须变为类内部参数。
        """
        self.b = b
        self.alpha = alpha
        self.beta = beta
        self._lambda = _lambda
        pass

    def _run(self, following_car: CarInfo) -> float:
        """
        重载
        :param following_car:
        :return:
        """
        optimal_speed = (
                0.5 * following_car.limiting_speed[1]
                * (np.tanh(following_car.real_spacing / self.b - self.beta) - np.tanh(-self.beta))
        )
        _a = (
                self.alpha * (optimal_speed - following_car.real_speed)
                + self._lambda * following_car.real_speed_difference
        )
        return _a  # 返回计算的加速度

    pass
