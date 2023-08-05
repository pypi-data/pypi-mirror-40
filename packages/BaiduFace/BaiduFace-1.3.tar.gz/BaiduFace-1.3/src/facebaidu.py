import time
import threading
import cv2
import numpy as np
import pylab
from aip import AipFace


class FaceApi(object):
    APP_ID = '10746894'
    API_KEY = '640WiwB1rT1kDGDkkn96YuFq'
    SECRET_KEY = 'xApbFvh7Kq1uxVjLVsrGLGWOd9ob0gZE'
    x1, x2, y1, y2, rotation_angle, key_point, key_point72 = [], [], [], [], [], [], []

    def __init__(self, referral_method, number=1, APP_ID=None, API_KEY=None, SECRET_KEY=None):
        """
        初始化各变量
        :param referral_method: 识别到新的人脸后执行的方法
        :param number: 识别的人数,默认是1
        :param APP_ID:
        :param API_KEY:
        :param SECRET_KEY:
        """
        if not API_KEY is None:
            self.APP_ID = APP_ID
            self.API_KEY = API_KEY
            self.SECRET_KEY = SECRET_KEY
        self.__referral_method = referral_method
        self.__number = number
        self.__client = AipFace(self.APP_ID
                                , self.API_KEY, self.SECRET_KEY)  # 实例化AipFace
        self.__cap = cv2.VideoCapture(0)
        self.__stranger = True  # 是否新人
        self.__faces = list(range(3))
        self.__image_flow = 0
        self.options = {"max_face_num": self.__number,
                        "face_fields": "age,expression,faceshape,glasses,gender,beauty,race,landmark,qualities"}

    def get_face(self, client):
        """
        获取人脸信息
        :param client:
        """
        while True:
            try:
                if self.__image_flow != 0:
                    res = client.detect(self.__image_flow, self.options)
                    self.data = res
                    print(self.data)
                    # start=time.time()
                    self.__faces[0] = self.__faces[1]
                    self.__faces[1] = self.__faces[2]
                    self.__faces[2] = self.__image_flow

                    if 'result' in self.data.keys() and len(self.data['result']) > 0:
                        self.x1, self.x2, self.y1, self.y2, self.rotation_angle, self.key_point, self.key_point72 = [], [], [], [], [], [], []
                        for d in self.data['result']:
                            location = d['location']
                            self.x1.append(location['left'])
                            self.y1.append(location['top'])
                            self.x2.append(location['left'] + location['width'])
                            self.y2.append(location['top'] + location['height'])

                            self.rotation_angle.append(d['rotation_angle'])  # 面部旋转角度

                            for point in d['landmark']:
                                self.key_point.append((point['x'], point['y']))

                            for point in d['landmark72']:
                                self.key_point72.append((point['x'], point['y']))
                    else:
                        self.x1, self.x2, self.y1, self.y2, self.rotation_angle, self.key_point, self.key_point72 = [], [], [], [], [], [], []

                    end = time.time()
                    # print("*****",end , end - start," s")
            except:
                continue

    def detect(self, client):
        """
        检测是否新人
        :param client:
        """
        while True:
            try:
                if not isinstance(self.__faces[0], int):
                    imgs = [
                        self.__faces[0],
                        self.__faces[2]
                    ]
                    res = client.match(imgs)
                    if 'result' in res.keys():
                        if len(res['result']) > 0:
                            score = res['result'][0]['score']
                            if self.__stranger:
                                print(res['result'][0]['score'], time.time())

                                # data=self.data #由于是两个线程在跑,不能保证data的即时性,更可能根本都检测不到面部
                                data = client.detect(imgs[1], self.options)

                                # 开始推荐系统
                                threading.Thread(target=self.__referral_method, args=(data,),
                                                 name="Referral system").start()
                                # self.__referral_method(data)

                                self.__stranger = False
                            if score < 80:
                                self.__stranger = True
                            else:
                                self.__stranger = False
                        else:
                            print("没有检测到人脸")
            except:
                continue

    def start_camera(self):
        """
        启动摄像机
        :return:
        """

        def rotating(x, y, rx0, ry0, a):
            """
            将坐标(x, y)以(rx0, ry0)为原点旋转 a 度
            :param x:
            :param y:
            :param rx0:
            :param ry0:
            :param a:
            :return:
            """
            a = np.radians(a)
            x0 = (x - rx0) * np.cos(a) - (y - ry0) * np.sin(a) + rx0
            y0 = (x - rx0) * np.sin(a) + (y - ry0) * np.cos(a) + ry0
            return int(x0 + 0.5), int(y0 + 0.5)

        def draw_face(x1, x2, y1, y2, rotation_angle):
            """
            绘制面部位置
            :param x1:
            :param x2:
            :param y1:
            :param y2:
            :param rotation_angle:
            :return:
            """
            for i in range(len(self.x1)):
                cv2.line(frame, (x1[i], y1[i]),
                         rotating(x2[i], y1[i], x1[i], y1[i], rotation_angle[i]), (180, 0, 0), 2)
                cv2.line(frame, rotating(x2[i], y2[i], x1[i], y1[i], rotation_angle[i]),
                         rotating(x2[i], y1[i], x1[i], y1[i], rotation_angle[i]), (180, 0, 0), 2)
                cv2.line(frame, (x1[i], y1[i]),
                         rotating(x1[i], y2[i], x1[i], y1[i], rotation_angle[i]), (180, 0, 0), 2)
                cv2.line(frame, rotating(x1[i], y2[i], x1[i], y1[i], rotation_angle[i]),
                         rotating(x2[i], y2[i], x1[i], y1[i], rotation_angle[i]), (180, 0, 0), 2)

        def draw_face_key_point(key_point, key_point72):
            for point in key_point:
                cv2.circle(frame, (int(point[0]), int(point[1])), 10, (55, 255, 155), 1)
            for point72 in key_point72:
                cv2.circle(frame, (int(point72[0]), int(point72[1])), 1, (50, 50, 255), 2)

        while True:
            try:
                pylab.time.sleep(0.1)
                successful, frame = self.__cap.read()
                frame = cv2.flip(frame, 1)  # 镜像翻转
                ret, flow = cv2.imencode('.jpg', frame)
                self.__image_flow = flow.tobytes()

                draw_face(self.x1, self.x2, self.y1, self.y2, self.rotation_angle)  # 绘制面部所在位置矩形框
                draw_face_key_point(self.key_point, self.key_point72)  # 绘制面部关键点

                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except:
                continue

    def start(self):
        t1 = threading.Thread(target=self.get_face, args=(self.__client,), name="Get the coordinates of the face.")
        t1.setDaemon(True)
        t1.start()
        # pylab.time.sleep(0.2)

        t2 = threading.Thread(target=self.detect, args=(self.__client,), name="Detection of strangers")
        t2.setDaemon(True)
        t2.start()

        self.start_camera()  # 启动摄像头并绘制人脸位置

        self.__cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    def start_referral(data):
        """
        推荐系统
        :param data: 返回的JSON人脸数据(已经转为 dict )
        :return:
        """
        # json.dump(data, open('../data/data.json', 'w'), indent=4)

        info = []
        if "result" in data.keys():
            for d in data['result']:
                info.append('age: ' + str(float('%.2f' % d['age'])) \
                            + ', gender: ' + str(d['gender']) \
                            + ', glasses: ' + str(float('%.2f' % d['glasses'])) \
                            + ', beauty: ' + str(float('%.2f' % d['beauty'])))
        print("线程:", threading.current_thread().name, "欢迎您!开始运行推荐系统...\n\t" + str(info))
        print("\tDo something!")


    faceApi = FaceApi(start_referral, 5)  # 传入识别到人脸后执行的方法和识别的人数
    faceApi.start()
