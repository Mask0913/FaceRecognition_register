import cv2
import dlib
from tools import *
import time
import datetime
import pandas as pd

dic_time = {}
features_cap = 0
face_data = open('facedata.txt', 'r+')
database = eval(face_data.read())
cap = cv2.VideoCapture(0)

def reco(content):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('model/shape_predictor_68_face_landmarks.dat')
    facerec = dlib.face_recognition_model_v1("model/dlib_face_recognition_resnet_model_v1.dat")

    now_time = time.time()

    while cap.isOpened():
        flag, im_rd = cap.read()
        dets = detector(im_rd)
        tip = '请有序打卡，不要多人一起打卡，看到自己打卡成功即可离开'
        im_rd = cv2ImgAddText(im_rd, tip, 0, 100, textColor=(0, 0, 255), textSize=23)
        if len(dets) != 0:
            biggest_face = dets[0]
            # 取占比最大的脸
            maxArea = 0
            for det in dets:
                w = det.right() - det.left()
                h = det.top() - det.bottom()
                if w * h > maxArea:
                    biggest_face = det
                    maxArea = w * h
            cv2.rectangle(im_rd, tuple([biggest_face.left(), biggest_face.top()]),
                          tuple([biggest_face.right(), biggest_face.bottom()]),
                          (255, 0, 0), 2)
            # 获取当前捕获到的图像的所有人脸的特征，存储到 features_cap_arr
            if (time.time() - now_time) > 2:
                shape = predictor(im_rd, biggest_face)
                global features_cap
                features_cap = facerec.compute_face_descriptor(im_rd, shape)
                for key, value in database.items():
                    compare = return_euclidean_distance(features_cap, value)
                    if compare == "same":  # 找到了相似脸
                        study_time,ret = take_time(key)
                        if ret == 1:
                            content.setText(str(key + '签到打卡成功现在时间为： ' + str(datetime.datetime.now())))
                        elif ret == 2:
                            content.setText(str(key + '签退打卡成功现在时间为： ' + str(datetime.datetime.now())))
                        elif ret == 3:
                            content.setText(str(key + '已经签到打卡成功现在时间为： ' + str(datetime.datetime.now())) + '请勿重复打卡！')
                        elif ret == 4:
                            content.setText(str(key + '已经签退打卡成功现在时间为： ' + str(datetime.datetime.now())) + '请勿重复打卡！')
                        if (not (dic_time.__contains__(key))):
                            dic_time[key] = [study_time]
                        else:
                            if (study_time != 0):
                                dic_time[key].append(study_time)
                now_time = time.time()

        cv2.imshow('face_recoinition', im_rd)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            now_study_time = {}
            a = []
            b = []
            for key,value in dic_time.items():
                now_study_time[key] = sec_to_data(sum(value))
            print(now_study_time)
            for key,values in now_study_time.items():
                a.append(key)
                b.append(values)
            dataframe = pd.DataFrame({'name': a, 'time': b})
            now = datetime.datetime.now()
            str2 = str(now.month) + '-' + str(now.day)
            fd = open((str2 + '.csv'), mode="w")
            dataframe.to_csv((str2 + '.csv'), encoding="utf_8_sig")
            fd.close()
            break
    cap.release()
    cv2.destroyAllWindows()


