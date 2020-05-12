# d6623
# The class for visual classifier

# d6623
# Using the generated model, predict the inputed card

from keras import models
import os
from keras.preprocessing import image
import numpy as np
import logging

logger = logging.getLogger('jerry.cards.eyes')
#logger.setLevel(logging.INFO)

#logger.info('Loaded eyes class')

class Eyes:
    def __init__(self):
        self.tmp_name = 'tmp.jpg'
        self.base = os.path.dirname(os.path.abspath(__file__))
        self.value_model = os.path.join(self.base, 'value-v1.h5')

        self.model = models.load_model(self.value_model)
        logger.debug('Loaded old model of %a' % self.value_model)

    def take_photo(self):
        os.system('fswebcam --no-banner %a' % self.tmp_name)

    def extract_info(self):
        # Test on custom image
        img = image.load_img(self.tmp_name, target_size=(150, 150),
                             color_mode='grayscale')

        x = image.img_to_array(img)
        x = x.astype('float32') / 255
        x = x.reshape((1,) + x.shape)  # Convert from (150,150,3) to (1,150,150,3)

        pred = self.model.predict(x, verbose=0)[0]

        logger.debug('Value prediction \n%a' % pred)
        label = self.value_to_label(np.argmax(pred))
        logger.info('Prediction of %a' % label)
        return label

    def value_to_label(self, value):
        # Cause its really weird the order goes backwards
        # 10, 11, 12, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9
        labels = [1, 10, 11, 12, 13, 2, 3, 4, 5, 6, 7, 8, 9]
        return labels[value]

    def read(self):
        self.take_photo()
        return self.extract_info()