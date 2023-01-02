import os

import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from skimage.transform import resize
from skimage.color import rgb2lab, gray2rgb

def test_model(test_path, transfer_learning_model, model):
    files = os.listdir(test_path)
    for idx, file in enumerate(files):
        test = img_to_array(load_img(test_path + file))
        test = resize(test, (224, 224), anti_aliasing=True)
        test *= 1.0 / 255
        lab_test = rgb2lab(test)
        luminance_test = lab_test[:, :, 0]
        embedings_test = gray2rgb(luminance_test)
        embedings_test = embedings_test.reshape((1, 224, 224, 3))
        embedings_test = transfer_learning_model.predict(embedings_test)
        ab_test = model.predict(embedings_test)
        ab_test = ab_test * 128
        cur = np.zeros((224, 224, 3))
        cur[:, :, 0] = luminance_test
        cur[:, :, 1:] = ab_test
    return test, luminance_test, cur
