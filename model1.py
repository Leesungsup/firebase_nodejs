import os
import keras
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
from keras.models import load_model
import keras.utils as image
from PIL import Image
import json
import numpy as np
# {'과메기': 0, '양념치킨': 1, '젓갈': 2, '콩자반': 3, '편육': 4, '피자': 5, '후라이드치킨': 6}
cal={'0':178,'1':323,'2':100,'3':317,'4':156,'5':269,'6':293}
def load_image(img_path, show=False):

    img = image.load_img(img_path, target_size=(299, 299))
    img_tensor = image.img_to_array(img)                    # (height, width, channels)
    img_tensor = np.expand_dims(img_tensor, axis=0)         # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor /= 255.                                      # imshow expects values in the range [0, 1]

    if show:
        plt.imshow(img_tensor[0])                           
        plt.axis('off')
        plt.show()

    return img_tensor


if __name__ == '__main__':
    model = load_model('./'+'0206_InceptionV3 model.h5')
    # sample_img_path = './drive/MyDrive/food/test/콩자반/Img_025_0088.jpg'
    sample_img_path = './uploads/1_13.jpg'
    # sample_img_path = './uploads/'+os.sys.argv[1]
    img = image.load_img(sample_img_path, target_size = (299, 299))
    
    # print(sample_img_path)
    new_image = load_image(sample_img_path)
    # print(model.predict(new_image))
    classes = np.argmax(model.predict(new_image,verbose=0), axis = 1)
    # print(cal[str(classes[0])])
    json_string={"dd":str(cal[str(classes[0])])}
    json_object = json.dumps(json_string)
    print(json_object)