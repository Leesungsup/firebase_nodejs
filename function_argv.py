import sys
import cv2 as cv

def getName(name, age):
    print(name + " : " + age)

if __name__ == '__main__':
    print("./uploads/"+sys.argv[3])
    img = cv.imread("./uploads/"+sys.argv[3])
    img = cv.resize(img, (350, 500))
    cv.imshow("",img)
    cv.waitKey(0)
    a=23
    getName(sys.argv[1], sys.argv[2])
    print(a)