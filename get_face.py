import dlib
import cv2
import os
import time

def get_faces(name,content):


    size = os.path.getsize('facedata.txt')
    if size >3:
        face_data = open('facedata.txt', 'r+')
        database = eval(face_data.read())
        face_data.close()
    else:
        database = {}

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('model/shape_predictor_68_face_landmarks.dat')
    facerec = dlib.face_recognition_model_v1("model/dlib_face_recognition_resnet_model_v1.dat")


    cap = cv2.VideoCapture(0)

    now_time = time.time()
    while cap.isOpened():
        flag, im_rd = cap.read()
        dets = detector(im_rd, 1)
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
            if (time.time() - now_time)>2:
                shape = predictor(im_rd, biggest_face)
                features_cap = facerec.compute_face_descriptor(im_rd, shape)
                face_data = open('facedata.txt', 'w')
                database[name] = features_cap
                content.setText(name + '录入成功，按 q  退出')
                face_data.write(str(database))
                face_data.close()
                now_time = time.time()

        cv2.imshow('get_face', im_rd)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
