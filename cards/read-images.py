# d6623 (d6897)
# Using the generated model, predict the inputed card

import os
from keras.preprocessing import image
import numpy as np
import tflite_runtime.interpreter as tflite

print('WARNING: Must be run on raspberry pi as uses the webcam')
print('WARNING: This is a test and may break suddenly')

value_model = 'models/value-v3.tflite'
tmp_name = 'tmp.jpg'

interpreter = tflite.Interpreter(model_path=value_model)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

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
    img = image.load_img(tmp_name,
                         target_size=(150, 150),
                         color_mode='grayscale')

    x = image.img_to_array(img)
    x = x.astype('float32') / 255
    x = x.reshape((1,) + x.shape)  # Convert from (150,150,3) to (1,150,150,3)

    interpreter.set_tensor(input_details[0]['index'], x)
    interpreter.invoke()
    out = interpreter.get_tensor(output_details[0]['index'])

    out = out.reshape(13,)

    label = value_to_label(out.argmax(axis=0))
    print('Guess of', label)
    print("With a confidence of", out[out.argmax(axis=0)].__round__(2))

    #pred = model.predict(x, verbose=0)[0]
    #print('Prediction of ', value_to_label(np.argmax(pred)))


while True:
    input('(Press any key to run)\n')
    take_photo()
    extract_value()
