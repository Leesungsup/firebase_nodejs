import os
import sys
import cv2 as cv
import json


def getName(name, age):
    json_string={"dd":str(name + ": " + age)}
    json_object = json.dumps(json_string)
    print( json_object )

if __name__ == '__main__':
    # print("gasgd")
    # print("./uploads/"+os.sys.argv[3])
    img = cv.imread("./uploads/"+os.sys.argv[3])
    img = cv.resize(img, (350, 500))
    cv.imshow("",img)
    cv.waitKey(0)
    a=23
    getName(os.sys.argv[1], os.sys.argv[2])
    json_string={"key":str(a)}
    json_object1 = json.dumps(json_string)
    print(json_object1)