# -*- encoding:utf-8 -*-
import sys
import os
import time
import argparse

# Add the directory containing robotiq_preamble.py to the Python search path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'robotiq'))
from UR_tasks import URTasks as URT
from util import row_col_mapping

import sqlite3
import datetime
from cv_model import *


# python Execution.py --vial 1 --shake

def parse_arguments():
    parser = argparse.ArgumentParser(description="Robot control script")
    parser.add_argument('--vial', type=int, required=True, help='Vial number to pick')
    parser.add_argument('--shake', action='store_true', help='Whether to perform shaking')
    return parser.parse_args()


def run_database_monitor():
    conn = sqlite3.connect(os.path.join(os.path.dirname(current_dir), 'history.db'))
    cursor = conn.cursor()
    model_file = 'solubility_model.pth'
    solubility_model = load_model(model_file)

    while True:
        for table in ['Hansen', 'Particle', 'Solubility']:
            try:
                cursor.execute("SELECT * FROM {}".format(table))
                data = cursor.fetchall()
                for row in data:
                    if row[3] == 0:  # ongoing = 0 -> task not running
                        # ongoing = 1 -> task running
                        cursor.execute("UPDATE {} SET ongoing = 1 WHERE id = {}".format(table, row[0]))
                        conn.commit()
                        # select data from sample table
                        cursor.execute("SELECT * from '{}' WHERE father_id = {}".format(table + '-samples', row[0]))
                        sample_data = cursor.fetchall()
                        for sample in sample_data:
                            img = run_experiment(sample[3], sample[4], sample[5])  # sample_row, sample_col, shake
                            current_time = str(datetime.datetime.now())
                            # todo: change this
                            prediction = test_model_on_base64_image(solubility_model, img, device)
                            cursor.execute("INSERT INTO '{}' (father_id, image, time, prediction) VALUES ({}, {}, {}, "
                                           "{})".format(table + '-image', row[0], img, current_time, prediction))
                            conn.commit()
                        # ongoing = 2 -> task finished
                        cursor.execute("UPDATE {} SET ongoing = 2 WHERE id = {}".format(table, row[0]))
                        conn.commit()
            except Exception as e:
                print("Error:", e)
            finally:
                cursor.close()
                conn.close()
            time.sleep(5)


def run_experiment(vial_row, vial_col, shake):
    robot = URT(ip="192.168.56.6", port=30003)
    robot.go_to_middle()
    robot.activate_gripper()
    robot.open_gripper_width(60)
    # robot.pick_vial_1()
    vial = row_col_mapping(vial_row, vial_col)  # todo: implement rol_col_mapping

    robot.pick_vial(vial)

    # Wait for the condition checking thread to finish
    if shake:
        print("Shaking is requested. Executing vortex.")
        robot.execute_vortex()

    # robot.execute_vortex() #tested
    robot.open_lid()  # tested
    time.sleep(0.5)
    robot.load_vial_to_box()  # tested
    robot.close_lid()  # tested
    img = robot.capture_image_base64(vial)  # return img
    time.sleep(5)  # here is the time for ML
    robot.open_lid()  # tested
    time.sleep(0.5)
    robot.unload_vial_from_box()  # tested
    robot.close_lid()  # tested
    time.sleep(1)
    robot.go_to_middle()
    # robot.drop_vial_1()
    robot.drop_vial(vial)
    robot.go_to_middle()

    return img


def main():
    args = parse_arguments()

    robot = URT(ip="192.168.56.6", port=30003)

    # tested commands:
    # robot.go_home() # work
    # robot.activate_gripper() # work
    # robot.close_gripper() # work
    # robot.open_gripper() # work
    # robot.open_gripper_width(50) # work
    # time.sleep(1)
    # robot.close_gripper() # work
    # robot.get_joint_states()
    # robot.get_tcp()

    '''
    WorkFlow: (Tested)
    '''
    robot.go_to_middle()
    robot.activate_gripper()
    robot.open_gripper_width(60)
    # robot.pick_vial_1()
    robot.pick_vial(args.vial)

    # Wait for the condition checking thread to finish
    if args.shake:
        print("Shaking is requested. Executing vortex.")
        robot.execute_vortex()

    # robot.execute_vortex() #tested
    robot.open_lid()  # tested
    time.sleep(0.5)
    robot.load_vial_to_box()  # tested
    robot.close_lid()  # tested
    robot.capture_image(args.vial)  # save image into /image folder
    time.sleep(5)  # here is the time for ML
    robot.open_lid()  # tested
    time.sleep(0.5)
    robot.unload_vial_from_box()  # tested
    robot.close_lid()  # tested
    time.sleep(1)
    robot.go_to_middle()
    # robot.drop_vial_1()
    robot.drop_vial(args.vial)
    robot.go_to_middle()

    # robot.go_to_abovebox()
    # robot.go_to_pre_rack()


if __name__ == '__main__':
    run_database_monitor()
