# d6623
# The class for visual classifier

# d6623
# Using the generated model, predict the inputed card

from keras import models
import os
from keras.preprocessing import image
import numpy as np

class Eyes:
    def __init__(self):
        self.tmp_name = 'tmp.jpg'
        self.value_model = 'value-v1.h5'

        self.model = models.load_model(self.value_model)
        print('Loaded old model of', self.value_model)

    def take_photo(self):
        os.system('fswebcam --no-banner %a' % self.tmp_name)

    def read(self):
        # Test on custom image
        img = image.load_img(self.tmp_name, target_size=(150, 150),
                             color_mode='grayscale')

        x = image.img_to_array(img)
        x = x.astype('float32') / 255
        x = x.reshape((1,) + x.shape)  # Convert from (150,150,3) to (1,150,150,3)

        pred = self.model.predict(x, verbose=0)[0]

        print(pred)
        label = self.value_to_label(np.argmax(pred))
        print('Prediction of ', label)
        return label

    def value_to_label(self, value):
        # Cause its really weird the order goes backwards
        # 10, 11, 12, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9
        labels = [1, 10, 11, 12, 13, 2, 3, 4, 5, 6, 7, 8, 9]
        return labels[value]

eyes = Eyes()

while True:
    input('(Press any key to run)\n')
    eyes.take_photo()
    eyes.read()