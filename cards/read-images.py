# d6623
# Using the generated model, predict the inputed card

from keras import models
import os
from keras.preprocessing import image
import numpy as np

value_model = 'value-v1.h5'
tmp_name = 'tmp.jpg'

model = models.load_model(value_model)
print('Loaded old model of %a.' % value_model)

def value_to_label(value):
    # Cause its really weird the order goes backwards
    # 10, 11, 12, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9
    labels = [1, 10, 11, 12, 13, 2, 3, 4, 5, 6, 7, 8, 9]
    return labels[value]


def take_photo(fname=tmp_name):
    os.system('fswebcam --no-banner %a' % fname)

def extract_value():
    # Test on custom image
    img = image.load_img(tmp_name, target_size=(150, 150),
                         color_mode='grayscale')

    x = image.img_to_array(img)
    x = x.astype('float32') / 255
    x = x.reshape((1,) + x.shape)  # Convert from (150,150,3) to (1,150,150,3)

    pred = model.predict(x, verbose=0)[0]

    print(pred)
    print('Prediction of ', value_to_label(np.argmax(pred)))


while True:
    input('(Press any key to run)\n')
    take_photo()
    extract_value()
