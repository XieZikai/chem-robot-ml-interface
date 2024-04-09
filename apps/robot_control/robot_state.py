# -*- encoding:utf-8 -*-
import sys
import os
# Add the directory containing robotiq_preamble.py to the Python search path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'robotiq'))
from UR_tasks import URTasks as URT



def main():


    robot = URT(ip="192.168.56.6", port=30003)

    robot.get_joint_states()
    robot.get_tcp()


if __name__ == '__main__':
    main()
