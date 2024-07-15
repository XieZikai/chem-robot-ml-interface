# -*- encoding:utf-8 -*-
import sys
import os
import time
import csv
# Add the directory containing robotiq_preamble.py to the Python search path
current_dir = os.path.dirname(os.path.abspath(__file__))
rack_folder = os.path.join(current_dir, 'rack')
sys.path.append(os.path.join(current_dir, 'robotiq'))

from UR_tasks import URTasks as URT

def main():

    robot = URT(ip="192.168.56.6", port=30003)
    robot.capture_image_focus_adjustment_test(filename = '30')

if __name__ == '__main__':
    main()