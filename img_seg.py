import cv2
import numpy as np
import matplotlib.pyplot as plt

def getAreaOfFood(img1):
    img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img_filt = cv2.medianBlur( img, 5)
    img_th = cv2.adaptiveThreshold(img_filt,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    contours, _ = cv2.findContours(img_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # find contours. sort. and find the biggest contour. the biggest contour corresponds to the plate and fruit.
    mask = np.zeros(img.shape, np.uint8)
    largest_areas = sorted(contours, key=cv2.contourArea)
    cv2.drawContours(mask, [largest_areas[-1]], 0, (255,255,255,255), -1)
    img_bigcontour = cv2.bitwise_and(img1,img1,mask = mask)

    # plt.imshow(cv2.cvtColor(img_bigcontour, cv2.COLOR_BGR2RGB))
    # plt.title("Plate and food")
    # plt.show()

    # convert to hsv. otsu threshold in s to remove plate
    hsv_img = cv2.cvtColor(img_bigcontour, cv2.COLOR_BGR2HSV)
    mask_plate = cv2.inRange(hsv_img, np.array([0,0,100]), np.array([255,90,255]))
    mask_not_plate = cv2.bitwise_not(mask_plate)
    fruit_skin = cv2.bitwise_and(img_bigcontour,img_bigcontour,mask = mask_not_plate)

    # plt.imshow(cv2.cvtColor(fruit_skin, cv2.COLOR_BGR2RGB))
    # plt.title("Remove plate")
    # plt.show()

    #convert to hsv to detect and remove skin pixels
    hsv_img = cv2.cvtColor(fruit_skin, cv2.COLOR_BGR2HSV)
    skin = cv2.inRange(hsv_img, np.array([0,10,60]), np.array([10,160,255])) #Scalar(0, 10, 60), Scalar(20, 150, 255)
    not_skin = cv2.bitwise_not(skin); #invert skin and black
    fruit = cv2.bitwise_and(fruit_skin,fruit_skin,mask = not_skin) #get only fruit pixels

    # plt.imshow(cv2.cvtColor(fruit, cv2.COLOR_BGR2RGB))
    # plt.title("Only Food")
    # plt.show()

    fruit_bw = cv2.cvtColor(fruit, cv2.COLOR_BGR2GRAY)
    fruit_bin = cv2.inRange(fruit_bw, 10, 255) #binary of fruit
    

    #erode before finding contours
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    erode_fruit = cv2.erode(fruit_bin,kernel,iterations = 1)

    #find largest contour since that will be the fruit
    img_th = cv2.adaptiveThreshold(erode_fruit,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    contours, _ = cv2.findContours(img_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    mask_fruit = np.zeros(fruit_bin.shape, np.uint8)
    largest_areas = sorted(contours, key=cv2.contourArea)
    cv2.drawContours(mask_fruit, [largest_areas[-2]], 0, (255,255,255), -1)
    #dilate now
    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(13,13))
    mask_fruit2 = cv2.dilate(mask_fruit,kernel2,iterations = 1)
    fruit_final = cv2.bitwise_and(img1,img1,mask = mask_fruit2)

    # plt.imshow(cv2.cvtColor(fruit_final, cv2.COLOR_BGR2RGB))
    # plt.title("Fruit with Contour")
    # plt.show()

    #find area of fruit
    img_th = cv2.adaptiveThreshold(mask_fruit2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    contours, _ = cv2.findContours(img_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    largest_areas = sorted(contours, key=cv2.contourArea)
    fruit_contour = largest_areas[-2]
    fruit_area = cv2.contourArea(fruit_contour)

    # plt.imshow(cv2.cvtColor(img_th, cv2.COLOR_BGR2RGB))
    # plt.title("Food Contour")
    # plt.show()

    #finding the area of skin. find area of biggest contour
    skin2 = skin - mask_fruit2
    #erode before finding contours
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    skin_e = cv2.erode(skin2,kernel,iterations = 1)
    img_th = cv2.adaptiveThreshold(skin_e,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    contours, _ = cv2.findContours(img_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    mask_skin = np.zeros(skin.shape, np.uint8)
    largest_areas = sorted(contours, key=cv2.contourArea)

    cv2.drawContours(mask_skin, [largest_areas[-2]], 0, (255,255,255), -1)

    skin_rect = cv2.minAreaRect(largest_areas[-2])
    box = cv2.boxPoints(skin_rect)
    box = np.int0(box)
    mask_skin2 = np.zeros(skin.shape, np.uint8)
    cv2.drawContours(mask_skin2,[box],0,(255,255,255), -1)

    pix_height = max(skin_rect[1])

    pix_to_cm_multiplier = 5.0/pix_height
    
    skin_area = cv2.contourArea(box)

    return fruit_area, mask_fruit2, fruit_final, skin_area, fruit_contour, pix_to_cm_multiplier

if __name__ == '__main__':
    img1 = cv2.imread("./Dataset/images/All_Images/2_1.jpg")
    area, bin_fruit, img_fruit, skin_area, fruit_contour, pix_to_cm_multiplier = getAreaOfFood(img1)

    cv2.waitKey()
    cv2.destroyAllWindows()