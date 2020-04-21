import cv2
import numpy as np
from copy import deepcopy
from numba import jit

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 


class Visualization(object):
    __vehicle = np.array([])
    __vehicle_size = np.array([], dtype=np.int)
    __vehicle_img_size = np.array([], dtype=np.int)
    __vehicle_img_centre = np.array([], dtype=np.int)

    __bg = np.array([])
    __bg_size = np.array([], dtype=np.int)
    __bg_img_size = np.array([], dtype=np.int)
    __bg_img_centre = np.array([], dtype=np.int)

    __thickness = np.array([], dtype=np.int)
    __r = int()

    __nv_color = (1, 1, 1)
    __iv_color = (1, 0, 1)
    __bg_color = (0.2, 0.2, 0.2)

    __title = ""

    def __init__(self, car_size=(15, 6), car_img_size=(64, 64, 3), bg_size=(640, 640), loop_radius=256,
                 width=16, title="The Elephant Racing\n\n->[ENTER TO PLAY]  \n[Setting]\n[Help?]"):

        self.__vehicle_size = np.array(car_size, dtype=np.int)

        cig = (48, 48, 3)
        if car_img_size[0] <= 48:
            self.__vehicle_img_size = np.array(cig, dtype=np.int)
            self.__vehicle_img_centre = np.array(np.array(cig[0:2]) / 2, dtype=np.int)
        else:
            self.__vehicle_img_size = np.array(car_img_size, dtype=np.int)
            self.__vehicle_img_centre = np.array(np.array(car_img_size[0:2]) / 2, dtype=np.int)
            pass

        self.__bg_size = np.array(bg_size, dtype=np.int)
        self.__bg_img_size = np.array([bg_size[0], bg_size[1], 3], dtype=np.int)
        self.__bg_img_centre = np.array(np.array(bg_size) / 2, dtype=np.int)

        self.__r = loop_radius
        self.__thickness = width

        self.__vehicle = np.zeros(self.__vehicle_img_size)
        self.__bg = np.zeros(self.__bg_img_size)

        self.__title = title

        self.__init_graph(self.__bg_color, self.__title)
        pass

    # @jit
    def __draw_car(self, theta: np.array([]), vehicle_type=np.array([])):
        have_color = len(vehicle_type) != 0
        img = deepcopy(self.__bg)
        mask = np.zeros(self.__bg_img_size)
        for i in range(0, len(theta)):
            t = theta[i]
            h = int(320 - np.cos(np.pi * theta[i] / 180) * self.__r)
            w = int(320 + np.sin(np.pi * theta[i] / 180) * self.__r)
            a = 360 - t

            vehicle = deepcopy(self.__vehicle)
            r_car = cv2.getRotationMatrix2D(tuple(self.__vehicle_img_centre), a, 1)
            vehicle = cv2.warpAffine(vehicle, r_car, tuple(self.__vehicle_img_size[0:2]))

            h0 = h - self.__vehicle_img_centre[0]
            h1 = h + self.__vehicle_img_centre[0]
            w0 = w - self.__vehicle_img_centre[1]
            w1 = w + self.__vehicle_img_centre[1]

            if have_color:
                if vehicle_type[i] == 0:
                    pass
                elif vehicle_type[i] == 1:
                    vehicle[:, :, 0] = vehicle[:, :, 0] * self.__iv_color[0]
                    vehicle[:, :, 1] = vehicle[:, :, 1] * self.__iv_color[1]
                    vehicle[:, :, 2] = vehicle[:, :, 2] * self.__iv_color[2]
            else:
                pass

            mask[h0:h1, w0:w1, :] = mask[h0:h1, w0:w1, :] + vehicle[:, :, :]
            pass

        temp = np.sign(np.sum(mask, 2))
        temp = np.abs(temp - 1)

        img[:, :, 0] = img[:, :, 0] * temp
        img[:, :, 1] = img[:, :, 1] * temp
        img[:, :, 2] = img[:, :, 2] * temp
        img = img + mask
        return img

    # @jit
    def __draw_tags(self, img, theta: np.array([])):
        img = deepcopy(img)
        mask = np.zeros(self.__bg_img_size)
        tag = np.zeros(self.__vehicle.shape)
        cv2.rectangle(tag, (0, 0), (18, 18), (1, 1, 1), -1)
        cv2.rectangle(tag, (0, 0), (18, 18), (1, 0, 0), 1)
        for j in range(0, len(theta)):
            tag_ = deepcopy(tag)
            t = theta[j]
            h = int(320 - np.cos(np.pi * theta[j] / 180) * self.__r)
            w = int(320 + np.sin(np.pi * theta[j] / 180) * self.__r)
            a = 360 - t
            
            re = (cv2.getTextSize(str(j+1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1))
            org = np.array([9-re[0][0]/2, 9+re[0][1]/2], dtype=np.int)

            cv2.putText(tag_, str(j+1), tuple(org), cv2.FONT_HERSHEY_PLAIN, 1, (1, 0, 0), 1, cv2.LINE_AA)
            tg = tag.sum(2) == 0

            h0 = h - self.__vehicle_img_centre[0]
            h1 = h + self.__vehicle_img_centre[0]
            w0 = w - self.__vehicle_img_centre[1]
            w1 = w + self.__vehicle_img_centre[1]

            mask[h0:h1, w0:w1, 0] = mask[h0:h1, w0:w1, 0] * tg
            mask[h0:h1, w0:w1, 1] = mask[h0:h1, w0:w1, 1] * tg
            mask[h0:h1, w0:w1, 2] = mask[h0:h1, w0:w1, 2] * tg
            mask[h0:h1, w0:w1, :] = mask[h0:h1, w0:w1, :] + tag_[:, :, :]
            pass

        temp = np.sign(np.sum(mask, 2))
        temp = np.abs(temp - 1)

        img[:, :, 0] = img[:, :, 0] * temp
        img[:, :, 1] = img[:, :, 1] * temp
        img[:, :, 2] = img[:, :, 2] * temp
        img = img + mask
        return img

    def __draw_stat(self):
        pass

    def __draw_shell(self):
        pass

    # @jit
    def __init_graph(self, bg_color, title):
        cv2.circle(self.__bg, tuple(self.__bg_img_centre), self.__r, bg_color, self.__thickness, cv2.LINE_AA)
        cv2.circle(self.__bg, tuple(self.__bg_img_centre), self.__r, (0.5, 0.5, 0.5), int(self.__thickness/25), cv2.LINE_8)
        self.__bg = self.__beautification(self.__bg)

        p0 = tuple(np.array(self.__vehicle_img_centre[0:2] - self.__vehicle_size / 2, dtype=np.int))
        p1 = tuple(np.array(self.__vehicle_img_centre[0:2] + self.__vehicle_size / 2, dtype=np.int))
        cv2.rectangle(self.__vehicle, p0, p1, self.__nv_color, -1, cv2.LINE_AA)

        pts = np.array([
            tuple([
                self.__vehicle_img_centre[0] + self.__vehicle_size[0] / 2,
                self.__vehicle_img_centre[1] - self.__vehicle_size[1] / 2
            ]),
            tuple([
                self.__vehicle_img_centre[0] + self.__vehicle_size[0] / 2 + self.__vehicle_size[1] / 3,
                self.__vehicle_img_centre[1]
            ]),
            tuple([
                self.__vehicle_img_centre[0] + self.__vehicle_size[0] / 2,
                self.__vehicle_img_centre[1] + self.__vehicle_size[1] / 2
            ])
        ], dtype=np.int)
        cv2.fillConvexPoly(self.__vehicle, pts, (1, 0, 0), cv2.LINE_AA)
        self.__put_title(title)
        pass

    # @jit
    def __beautification(self, img: np.array([])):
        img0 = deepcopy(img)
        lawn = cv2.imread("material/lawn.jpg")
        lawn = cv2.resize(lawn, tuple(self.__bg_img_size[0:2]))
        mask = img0.sum(2)
        mask = mask <= 0
        mask = np.array(mask, dtype=np.float)
        for i in range(3):
            img0[:, :, i] = lawn[:, :, i] * mask / 255 + img0[:, :, i]
            pass
        return img0

    # @jit
    def __put_title(self, title: str):
        line_spacing = 2
        font_scale = 0.9
        thickness = 1
        tts = title.split('\n')
        size = []
        for t in tts:
            text_size = np.array(cv2.getTextSize(t, cv2.FONT_HERSHEY_DUPLEX, font_scale, thickness))
            text_size[0] = np.array(text_size[0])
            text_size[0][1] = text_size[0][1] + text_size[1]
            size.append(tuple(text_size[0]))
            pass
        meta_high = size[0][1]
        total_centre_high = int((len(tts) - 1) * meta_high * line_spacing)
        for i in range(0, len(tts)):
            cv2.putText(self.__bg, tts[i],
                        tuple(np.array(self.__bg_img_centre
                                       - np.array([0, total_centre_high/2-i*meta_high*line_spacing])
                                       - np.array([size[i][0]/2, 0]),
                                       dtype=np.int)),
                        cv2.FONT_HERSHEY_DUPLEX, font_scale, (1, 1, 0), thickness, lineType=cv2.LINE_AA)
            pass
        pass

    # @jit
    def refresh(self, theta: np.array([]), vehicle_type=np.array([])):
        img = self.__draw_car(theta, vehicle_type)
        img = self.__draw_tags(img, theta)
        return img

    pass


class LaneVis(object):
    pass


if __name__ == '__main__':
    import time

    th = np.array(range(0, 360, 18))
    cv2.namedWindow("Test", cv2.WINDOW_KEEPRATIO)
    vis = Visualization()
    st = 0
    et = 0
    dt = 0
    wt = 1
    for i in range(0, 60000):
        st = time.time()
        img = vis.refresh(th)
        th = th + 1
        cv2.imshow("Test", img)
        et = time.time()
        dt = (et - st) * 1000
        wt = int(66 - (et - st) * 1000)
        print(wt)

        if wt < 1:
            wt = 1
        else:
            pass

        if cv2.waitKey(wt) == 27:
            break
    cv2.destroyAllWindows()
