# d6623
# Run this on the Rpi to take photos of the cards and generate the data

# Value is the card size. eg 1=ace, 5=five, 11=jack, 12=queen, 13=king, joker IS NOT DEFINED
# Suit is simplified down to s=spades, h=hearts, d=diamonds, c=clubs

# TODO:
#   - add joker support
#   - add lighting changes so better accuracy
#   - change file system to match actual layout

import os
from shutil import copyfile
import subprocess

values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
suits = ['club', 'heart', 'spade', 'diamond']

train = True  # save to train or test folders

location = os.path.dirname(os.path.abspath(__file__))
print('Starting location %a' % location)

if train:
    value_dir = os.path.join(location, 'value', 'train')
    suits_dir = os.path.join(location, 'suits', 'train')
else:
    value_dir = os.path.join(location, 'value', 'test')
    suits_dir = os.path.join(location, 'suits', 'test')


def take_photo(fname='tmp.jpg'):
    subprocess.run(['fswebcam', '--no-banner', fname])
    #os.system('fswebcam --no-banner %a &> /dev/null' % fname)
    print("Took photo with name", fname)


def savephoto(s, v, index):
    p = os.path.join(suits_dir, s, str(v) + '_' + str(index) + '.jpg')
    print('Saving to', p)
    copyfile('tmp.jpg', p)

    p = os.path.join(value_dir, str(v), s + '_' + str(index) + '.jpg')
    print('Saving to', p)
    copyfile('tmp.jpg', p)


done = False
index = 0
for s in suits:
    for v in values:
        input('Input: ' + str(v) + ' ' + s)
        take_photo()
        savephoto(s, v, index)
        index += 1

        input('And upside down: ')
        take_photo()
        savephoto(s, v, index)
        index += 1

        print('')
