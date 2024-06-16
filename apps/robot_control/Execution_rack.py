# -*- encoding:utf-8 -*-
import sys
import os
import time
import argparse 
import csv
# Add the directory containing robotiq_preamble.py to the Python search path
current_dir = os.path.dirname(os.path.abspath(__file__))
rack_folder = os.path.join(current_dir, 'rack')
sys.path.append(os.path.join(current_dir, 'robotiq'))

from UR_tasks import URTasks as URT

# python3 Execution_rack.py --rack_number 1 --rack_number 2 --rack_number 3 --loop 5


def parse_arguments():
    parser = argparse.ArgumentParser(description="Robot control script")
    parser.add_argument('--rack_number', type=int, action='append', required=True, help='Rack numbers (1-5)')
    parser.add_argument('--loops', type=int, default=1, help='Number of times to loop the task execution')
    return parser.parse_args()


def read_rack_file(rack_number):
    file_path = os.path.join(rack_folder, f'rack_{rack_number}.csv')
    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return []



def main():
    args = parse_arguments()
    robot = URT(ip="192.168.56.6", port=30003)
    
    for loop_index in range(args.loops):
        for rack_number in args.rack_number:

            print(f"Processing Rack {rack_number}")
            rack_info = read_rack_file(rack_number)
            
            robot.activate_gripper()
            robot.open_gripper_width(200)
            # robot.pick_place_rack(rack_number)
            robot.pick_place_rack_from_shelf(rack_number)
            for vial_info in rack_info:
                vial_number = int(vial_info['vial'])
                shake = vial_info['shake'].lower() == 'true'
                sample_name = vial_info['name']

                print(f"Processing Vial {vial_number} ({sample_name}) - Shake: {shake}")

                robot.open_gripper_width(60)
                robot.pick_vial(vial_number)

                if shake:
                    print("Shaking is requested. Executing vortex.")
                    robot.execute_vortex()
                robot.go_avoid()
                robot.go_to_middle()
                robot.open_lid()
                time.sleep(0.5)
                robot.load_vial_to_box()
                robot.close_lid()
                time.sleep(1)
                robot.open_laser()
                robot.capture_image_focus_adjustment(vial_number=vial_number, rack_number=rack_number, sample_name=sample_name, loop_iteration=loop_index)
                time.sleep(5)
                robot.close_laser()
                robot.open_lid()
                time.sleep(0.5)
                robot.unload_vial_from_box()
                robot.close_lid()
                time.sleep(1)
                robot.go_to_middle()
                robot.go_avoid()
                robot.drop_vial(vial_number)
                robot.move_up(0.05)

            robot.move_up(0.07)
            robot.open_gripper_width(200)
            robot.place_back_rack_to_shelf(rack_number)
            robot.go_home()

def test():
    # the code to acquire images work

    args = parse_arguments()
    robot = URT(ip="192.168.56.6", port=30003)   

    for rack_number in args.rack_number:

        print(f"Processing Rack {rack_number}")
        rack_info = read_rack_file(rack_number)
        
        robot.activate_gripper()
        robot.open_gripper_width(200)
        # robot.pick_place_rack(args.rack_numver)

        for vial_info in rack_info:
            vial_number = int(vial_info['vial'])
            shake = vial_info['shake'].lower() == 'true'
            sample_name = vial_info['name']

            print(f"Processing Vial {vial_number} ({sample_name}) - Shake: {shake}")

            robot.capture_image_focus_adjustment(vial_number=vial_number, rack_number=rack_number, sample_name=sample_name)


if __name__ == '__main__':
    main()
    # test()


