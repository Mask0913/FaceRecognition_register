import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import time

dic = {}

def return_euclidean_distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    feature_1 = np.around(feature_1, decimals= 3)
    feature_2 = np.around(feature_2, decimals= 3)
    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    if dist > 0.3:
        return "diff"
    else:
        return "same"


def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    if (isinstance(img, np.ndarray)):  #判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontText = ImageFont.truetype(
        "simsun.ttc", textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=fontText)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)



#ret：1 签到打卡成功  2签退打卡成功  3已经签到打卡成功  4已经签退打卡成功
def take_time(name):
    ret = 0
    if (not (dic.__contains__(name))):
        dic[name] = [time.time()]
        ret = 1
        return 0,ret
    else:
        for key,value in dic.items():
            if key == name:
                lenth = len(value)
                if lenth % 2 == 0:
                    if (time.time() - value[-1]) > 30:
                        ret = 1
                        dic[name].append(time.time())
                        return 0,ret
                    else:
                        ret = 4
                        return 0,ret
                else:
                    if (time.time() - value[-1]) > 30:
                        dic[name].append(time.time())
                        study_time = value[-1] - value[-2]
                        ret = 2
                        return study_time,ret
                    else:
                        ret = 3
                        return 0,ret
                    

def convert_time_to_str(time):
    #时间数字转化成字符串，不够10的前面补个0
    if (time < 10):
        time = '0' + str(time)
    else:
        time=str(time)
    return time

def sec_to_data(y):

    h=int(y//3600 % 24)
    d = int(y // 86400)
    m =int((y % 3600) // 60)
    s = round(y % 60,2)
    h=convert_time_to_str(h)
    m=convert_time_to_str(m)
    s=convert_time_to_str(s)
    d=convert_time_to_str(d)
    # 天 小时 分钟 秒
    return d + ":" + h + ":" + m + ":" + s






