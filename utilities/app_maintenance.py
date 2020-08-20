""" Script for deleting google street view images from assets folder.
To be run with a task scheduler either locally or on cloud platform's 
task scheduling software."""

import glob, os

directory = 'assets/'

for i in os.listdir(directory): #(os.path.join(directory,"gsvImg_*")):
    if i.startswith('gsvImg_'):
        os.remove(os.path.join(directory, i))
        # print (i)
    else:
        pass
