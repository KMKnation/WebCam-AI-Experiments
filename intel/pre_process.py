import cv2
import numpy as np

def pre_process(modelname, input_image):
    if modelname == 'a':
        width = 456
        height = 256
    else:
        width = 456
        height = 510

    input_image = cv2.resize(input_image, (width, height))
    input_image = input_image.transpose(2,0,1)
    input_image = np.expand_dims(input_image, axis=0)

    return input_image