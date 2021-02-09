# d6623
# The class for visual classifier

# d6623, d6898
# Using the generated model, predict the inputted card

import tflite_runtime.interpreter as tflite
import os
from keras.preprocessing import image
import numpy as np
import logging
import subprocess

logger = logging.getLogger('jerry.cards.eyes')

logger.warning('Must be run on raspberry pi as uses the webcam')


class Eyes:
    def __init__(self):
        self.tmp_name = 'tmp.jpg'
        self.base = os.path.dirname(os.path.abspath(__file__))

        self.value_name = '/home/pi/jerry/cards/models/value-v4.tflite'
        self.suit_name = None

        self.load_models()

    def load_models(self):
        self.value_interpreter = tflite.Interpreter(model_path=self.value_name)
        self.value_interpreter.allocate_tensors()

        # self.suit_model = models.load_model(os.path.join(self.base, self.suit_name))
        # self.value_model = models.load_model(os.path.join(self.base, self.value_name))
        logger.debug('Loaded value model of %a' % self.value_name)
        # logger.debug('Loaded suit model of %a' % self.suit_name)

    def take_photo(self):
        cmd = 'fswebcam --no-banner %a' % self.tmp_name
        out = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
        # for line in out.split('\n'):
        #    logger.debug(line)  # If you want to display all the debug garbage
        # os.system('fswebcam --no-banner %a' % self.tmp_name)

    def get_suit(self):
        # Get the suit of the image
        img = image.load_img(self.tmp_name,
                             target_size=(150, 150),
                             color_mode='rgb')

        x = image.img_to_array(img)
        x = x.astype('float32') / 255
        x = x.reshape((1,) + x.shape)  # Convert from (150,150,3) to (1,150,150,3)

        # pred = self.suit_model.predict(x, verbose=0)[0]

        # logger.debug('Suit prediction \n%a' % pred)
        # label = self.suit_to_label(np.argmax(pred))
        label = None
        return label

    def get_value(self):
        # Get the value of the image
        img = image.load_img(self.tmp_name,
                             target_size=(150, 150),
                             color_mode='grayscale')

        x = image.img_to_array(img)
        x = x.astype('float32') / 255
        x = x.reshape((1,) + x.shape)  # Convert from (150,150,1) to (1,150,150,1)

        self.value_interpreter.set_tensor(self.value_interpreter.get_input_details()[0]['index'], x)
        self.value_interpreter.invoke()
        out = self.value_interpreter.get_tensor(self.value_interpreter.get_output_details()[0]['index'])
        out = out.reshape(13, )

        label = self.value_to_label(out.argmax(axis=0))
        confidence = ((out[out.argmax(axis=0)])*100).__round__(0)
        if confidence < 50:
            logger.warning('Confidence is only %a/100. Perhaps a redo?' % confidence)
        logger.debug('Label of %a' % label)
        logger.debug('Confidence of %a/100' % confidence)
        return label

    def value_to_label(self, value):
        # Cause its really weird the order goes backwards
        # 10, 11, 12, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9
        labels = [1, 10, 11, 12, 13, 2, 3, 4, 5, 6, 7, 8, 9]
        return labels[value]

    def suit_to_label(self, suit):
        # Get the human readable from the suit
        labels = ['club', 'diamond', 'heart', 'spade']
        return labels[suit]

    def read(self):
        self.take_photo()
        suit = self.get_suit()
        value = self.get_value()
        logger.info('Prediction of %s of %ss' % (value, suit))
        return suit, value

    def read_value(self):
        self.take_photo()
        value = self.get_value()
        return value


if __name__ == '__main__':
    print('Running eyes loop...')
    logger = logging.getLogger('eyes')
    logger.setLevel(logging.DEBUG)
    e = Eyes()
    while True:
        input(': ')
        v = e.read_value()
        #print('Prediction of %s of %ss' % (v, None))
        print('Prediction of', v)
