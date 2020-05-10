# d6623
# Run this on the Rpi to take photos of the cards and generate the data

# Value is the card size. eg 1=ace, 5=five, 11=jack, 12=queen, 13=king, joker IS NOT DEFINED
# Suit is simplified down to s=spades, h=hearts, d=diamonds, c=clubs

# TODO:
#   - add joker support

values = [1,2,3,4,5,6,7,8,9,10,11,12,13]
suits = ['clubs', 'hearts', 'spades', 'diamonds']

import os
from shutil import copyfile

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
    os.system('fswebcam --no-banner %a' % fname)

done = False
index = 0
while not done:
    command = input('Card value: suit,value\n')
    args = command.split(',')
    assert args[0] == 's' or 'h' or 'c' or 'd'
    assert 0 < int(args[1]) < 14
    print(args)
    take_photo()

    fname = str(index) + ' ' + args[0] + '.jpg'
    print(fname)
    copyfile('tmp.jpg', os.path.join(suits_dir, fname))

    fname = str(index) + ' ' + args[1] + '.jpg'
    print(fname)
    copyfile('tmp.jpg', os.path.join(value_dir, fname))

    index += 1