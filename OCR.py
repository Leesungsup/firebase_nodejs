import json
import re
import cv2
import requests
import sys
import os

LIMIT_PX = 1024
LIMIT_BYTE = 1024*1024  # 1MB
LIMIT_BOX = 40


def kakao_ocr_resize(image_path: str):
    """
    ocr detect/recognize api helper
    ocr api의 제약사항이 넘어서는 이미지는 요청 이전에 전처리가 필요.

    pixel 제약사항 초과: resize
    용량 제약사항 초과  : 다른 포맷으로 압축, 이미지 분할 등의 처리 필요. (예제에서 제공하지 않음)

    :param image_path: 이미지파일 경로
    :return:
    """
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    if LIMIT_PX < height or LIMIT_PX < width:
        ratio = float(LIMIT_PX) / max(height, width)
        image = cv2.resize(image, None, fx=ratio, fy=ratio)
        height, width, _ = height, width, _ = image.shape

        # api 사용전에 이미지가 resize된 경우, recognize시 resize된 결과를 사용해야함.
        image_path = "{}_resized.jpg".format(image_path)
        cv2.imwrite(image_path, image)

        return image_path
    return None


def kakao_ocr(image_path: str, appkey: str):
    """
    OCR api request example
    :param image_path: 이미지파일 경로
    :param appkey: 카카오 앱 REST API 키
    """
    API_URL = 'https://dapi.kakao.com/v2/vision/text/ocr'

    headers = {'Authorization': 'KakaoAK {}'.format(appkey)}

    image = cv2.imread(image_path)
    jpeg_image = cv2.imencode(".jpg", image)[1]
    data = jpeg_image.tobytes()


    return requests.post(API_URL, headers=headers, files={"image": data})


def main():
    if len(sys.argv) != 3:
        print("Please run with args: $ python example.py /path/to/image appkey")
    image_path, appkey = os.sys.argv[1], os.sys.argv[2]

    resize_impath = kakao_ocr_resize(image_path)
    if resize_impath is not None:
        image_path = resize_impath
        # print("원본 대신 리사이즈된 이미지를 사용합니다.")

    output = kakao_ocr(image_path, appkey).json()
    outputdata = json.dumps(output, ensure_ascii=False, sort_keys=True, indent=2)
    # print("[OCR] output:\n{}\n".format(outputdata))

    # 받은 데이터 array로 변환
    outputdata = json.loads(outputdata)
    list1= list()
    for i in range(len(outputdata['result'])):
        # box 모양으로 잘라서 보여주기
        x = outputdata['result'][i]['boxes'][0][0]
        y = outputdata['result'][i]['boxes'][0][1]
        w = (outputdata['result'][i]['boxes'][1][0] - outputdata['result'][i]['boxes'][0][0])
        h = (outputdata['result'][i]['boxes'][2][1] - outputdata['result'][i]['boxes'][0][1])
        # print(outputdata['result'][i]['recognition_words'][0])
        list1.append(outputdata['result'][i]['recognition_words'][0])
    # print(''.join(list1).strip())
    text=''.join(list1)

    start = text.find('신장') + 2
    end = text.find('cm', start)
    stat1=text[start:end]
    start = text.find('kg') - 4
    stat2 = text[start:start+4]
    start = text.find('골격근량') + 10
    end = text.find('골격근량') + 14
    stat3=text[start:end]
    start = text.find('체지방량') + 10
    end = text.find('체지방량') + 14
    stat4 = text[start:end]
    start = text.find('체수분') + 3
    end = text.find('체수분') + 7
    stat5 = text[start:end]
    start = text.find('단백질') + 3
    end = text.find('단백질') + 6
    stat6 = text[start:end]
    start = text.find('BMI') + 10
    end = text.find('BMI') + 14
    stat7 = text[start:end]
    start = text.find('경도비만') + 7
    end = text.find('경도비만') + 11
    stat8 = text[start:end]
    start = text.find('복부지방률') + 7
    end = text.find('복부지방률') + 11
    stat9 = text[start:end]
    start = text.find('기초대사량') + 20
    end = text.find('기초대사량') + 24
    stat10 = text[start:end]

    json_string={"신장":str(stat1),"체중":stat2,"골격근량":stat3,"체수분":stat5,"단백질":stat6,"BMI":stat7,"체지방률":stat8,"복부지방률":stat9,"기초대사량":stat10}
    json_object = json.dumps(json_string)
    print(json_object)
    # print("신장",stat1)
    # print("체중",stat2)
    # print("골격근량",stat3)
    # print("체수분",stat5)
    # print("단백질",stat6)
    # print("BMI",stat7)
    # print("체지방률",stat8)
    # print("복부지방률",stat9)
    # print("기초대사량",stat10)

if __name__ == "__main__":
    main()