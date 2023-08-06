from . import Polytools
from os import path
from .basic import shift, blur
from .vis import color_vis
import numpy
from PIL import Image

def poly(img):
    if(img.size[0]*img.size[1]) > 10000:
        while(True):
            inp = input("Large images can take long to process. Continue? (y/n)")
            if inp == 'y':
                print("Continuing.")
                break
            elif inp == 'n':
                print("Exiting tool.")
                return
            else:
                print('y or n')
    Polytools.runTracker(img)
    Polytools.alter(img)
    return Polytools.polyImage(img)

def gray(img):
    '''convert('LA') puts it in black and white, but for use in some other functions there must be three bands'''
    return img.convert('L')

def thermal(img):
    '''Enhance the RGB values of each pixel to make it look like a thermal image'''
    arr=numpy.array(img)
    for i in range(len(arr)):
        for j in range(len(arr[i])):
                brightness=sum(arr[i][j])/len(arr[i][j])
                r=max(0,255+2*(brightness-255))  #red
                g=max(0,255-4*abs(brightness-122)) #green
                b=max(0,255-2*brightness)
                arr[i][j]=(r,g,b)
    return Image.fromarray(arr)
