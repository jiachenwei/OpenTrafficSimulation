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
                            PATH_CACC=PATHModelCACC(),
                            IDM_WITH_GIPPS=IDMWithGipps(),
                            PATH_ACC_WITH_GIPPS=PATHModelACCWithGipps(),
                            PATH_CACC_WITH_GIPPS=PATHModelCACCWithGipps(),
                            IDCM_ACC=IntelligentDrivingCarModel(PATHModelACCWithGipps()),
                            IDCM_CACC=IntelligentDrivingCarModel(PATHModelCACCWithGipps()))

DICT_CAR_TYPE = {
    "TEST": 00,
    "HDC": 10,
    "SDC": 20,
    "IDC": 30
}

HDC = Car(car_name='HDC',
          car_type=DICT_CAR_TYPE["HDC"],
          following_model=DICT_FOLLOWING_MODEL["IDM_WITH_GIPPS"],
          car_size=CAR_SIZE,
          expecting_headway=3,
          limiting_acceleration=LIMITING_ACCELERATION,
          limiting_speed=LIMITING_SPEED,
          stopping_distance=1,
          observation_error=0.05,
          operation_error=0.05,
          response_time_delay=0.67,
          car_color=(1, 0, 0))

SDC_CACC = Car(car_name='SDC',
               car_type=DICT_CAR_TYPE["SDC"],
               following_model=DICT_FOLLOWING_MODEL["PATH_CACC_WITH_GIPPS"],
               car_size=CAR_SIZE,
               expecting_headway=2,
               limiting_acceleration=LIMITING_ACCELERATION,
               limiting_speed=LIMITING_SPEED,
               stopping_distance=1,
               observation_error=0.005,
               operation_error=0.005,
               response_time_delay=0.02,
               car_color=(1, 0, 0))

SDC_ACC = Car(car_name='SDC',
              car_type=DICT_CAR_TYPE["SDC"],
              following_model=DICT_FOLLOWING_MODEL["PATH_ACC_WITH_GIPPS"],
              car_size=CAR_SIZE,
              expecting_headway=3,
              limiting_acceleration=LIMITING_ACCELERATION,
              limiting_speed=LIMITING_SPEED,
              stopping_distance=1,
              observation_error=0.005,
              operation_error=0.005,
              response_time_delay=0.02,
              car_color=(1, 0, 0))

# IDC
IDC_CACC = Car(car_name='IDC',
               car_type=DICT_CAR_TYPE["IDC"],
               following_model=DICT_FOLLOWING_MODEL["IDCM_CACC"],
               car_size=CAR_SIZE,
               expecting_headway=2,
               limiting_acceleration=LIMITING_ACCELERATION,
               limiting_speed=LIMITING_SPEED,
               stopping_distance=1,
               observation_error=0.005,
               operation_error=0.005,
               response_time_delay=0.02,
               car_color=(1, 0, 0))

IDC_ACC = Car(car_name='IDC',
              car_type=DICT_CAR_TYPE["IDC"],
              following_model=DICT_FOLLOWING_MODEL["IDCM_ACC"],
              car_size=CAR_SIZE,
              expecting_headway=3,
              limiting_acceleration=LIMITING_ACCELERATION,
              limiting_speed=LIMITING_SPEED,
              stopping_distance=1,
              observation_error=0.005,
              operation_error=0.005,
              response_time_delay=0.02,
              car_color=(1, 0, 0))

# 精度0.02 不可更改
std_hdc_sdc_acc_proportions = [{HDC: 1.00, SDC_ACC: 0.00},
                               {HDC: 0.90, SDC_ACC: 0.10},
                               {HDC: 0.80, SDC_ACC: 0.20},
                               {HDC: 0.70, SDC_ACC: 0.30},
                               {HDC: 0.60, SDC_ACC: 0.40},
                               {HDC: 0.50, SDC_ACC: 0.50},
                               {HDC: 0.40, SDC_ACC: 0.60},
                               {HDC: 0.30, SDC_ACC: 0.70},
                               {HDC: 0.20, SDC_ACC: 0.80},
                               {HDC: 0.10, SDC_ACC: 0.90},
                               {HDC: 0.00, SDC_ACC: 1.00}]

std_hdc_sdc_cacc_proportions = [{HDC: 1.00, SDC_CACC: 0.00},
                                {HDC: 0.90, SDC_CACC: 0.10},
                                {HDC: 0.80, SDC_CACC: 0.20},
                                {HDC: 0.70, SDC_CACC: 0.30},
                                {HDC: 0.60, SDC_CACC: 0.40},
                                {HDC: 0.50, SDC_CACC: 0.50},
                                {HDC: 0.40, SDC_CACC: 0.60},
                                {HDC: 0.30, SDC_CACC: 0.70},
                                {HDC: 0.20, SDC_CACC: 0.80},
                                {HDC: 0.10, SDC_CACC: 0.90},
                                {HDC: 0.00, SDC_CACC: 1.00}]

std_hdc_idc_acc_proportions = [{HDC: 1.00, IDC_ACC: 0.00},
                               {HDC: 0.90, IDC_ACC: 0.10},
                               {HDC: 0.80, IDC_ACC: 0.20},
                               {HDC: 0.70, IDC_ACC: 0.30},
                               {HDC: 0.60, IDC_ACC: 0.40},
                               {HDC: 0.50, IDC_ACC: 0.50},
                               {HDC: 0.40, IDC_ACC: 0.60},
                               {HDC: 0.30, IDC_ACC: 0.70},
                               {HDC: 0.20, IDC_ACC: 0.80},
                               {HDC: 0.10, IDC_ACC: 0.90},
                               {HDC: 0.00, IDC_ACC: 1.00}]

std_hdc_idc_cacc_proportions = [{HDC: 1.00, IDC_CACC: 0.00},
                                {HDC: 0.90, IDC_CACC: 0.10},
                                {HDC: 0.80, IDC_CACC: 0.20},
                                {HDC: 0.70, IDC_CACC: 0.30},
                                {HDC: 0.60, IDC_CACC: 0.40},
                                {HDC: 0.50, IDC_CACC: 0.50},
                                {HDC: 0.40, IDC_CACC: 0.60},
                                {HDC: 0.30, IDC_CACC: 0.70},
                                {HDC: 0.20, IDC_CACC: 0.80},
                                {HDC: 0.10, IDC_CACC: 0.90},
                                {HDC: 0.00, IDC_CACC: 1.00}]

std_traffic_densities = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]

proportions = std_hdc_idc_acc_proportions
traffic_densities = std_traffic_densities
