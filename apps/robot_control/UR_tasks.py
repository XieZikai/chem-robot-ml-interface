# ur_tasks.py
from UR_Functions import URfunctions as URControl
from robotiq.robotiq_gripper import RobotiqGripper
import time
import logging
import cv2
import base64

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class URTasks:
    def __init__(self, ip, port):
        self.robot = URControl(ip=ip, port=port)
        self.gripper = RobotiqGripper()
        self.gripper.connect(ip, 63352)

        # config for vials on rack
        self.pre_pick_positions = {
            1: [-0.14479129, -0.49328619, 0.07697303, -0.53206640, -3.09373452, 0.00122079],
            # Add more pre_pick positions for other vials here
        }
        self.pick_positions = {
            1: [-0.14484212, -0.49331475, 0.05350598, -0.53210167, -3.09375955, 0.00129685],
            # Add more pick positions for other vials here
        }
        self.lift_up_positions = {
            1: [-0.14484212, -0.49331475, 0.10350598, -0.53210167, -3.09375955, 0.00129685],
            # Add more lift_up positions for other vials here
        }

        self.drop_positions = {
            1: [-0.14484212, -0.49331475, 0.06050598, -0.53210167, -3.09375955, 0.00129685],
            # Add more drop positions for other vials here
        }
        self.pre_drop_positions = {
            1: [-0.14484212, -0.49331475, 0.13350598, -0.53210167, -3.09375955, 0.00129685],
            # Add more pre_drop positions for other vials here
        }

    def initialize_robot(self):
        """Initializes robot connection and prepares it for operations."""
        self.robot.reconnect_socket()
        print("Robot initialized and ready.")
        
    def go_home(self):
        """Moves the robot to its 'home' position."""
        try:
            self.robot.go_home()
            print("Successfully moved to home position.")
        except Exception as e:
            print(f"Error moving to home position: {e}")
 
    def open_lid(self):
        self.robot.set_digital_output(0, True)

    def close_lid(self):
        self.robot.set_digital_output(0, False)

    def open_laser(self):
        self.robot.set_digital_output(1, True)

    def close_laser(self):
        self.robot.set_digital_output(1, False)

    def go_to_test(self, q):
        self.robot.movej_tcp(q, 0.5, 0.2)

    def get_joint_states(self):
        js = self.robot.get_current_joint_positions()
        formatted_js = ', '.join([f"{val:.8f}" for val in js]) 
        print(f"[{formatted_js}]")
        # print(js)
        return js

    def get_tcp(self):
        tcp = self.robot.get_current_tcp()
        formatted_tcp = ', '.join([f"{val:.8f}" for val in tcp]) 
        print(f"[{formatted_tcp}]")
        # print(tcp)
        return tcp

    '''
    Gripper command
    '''

    def activate_gripper(self):
        print('activate gripper')
        self.gripper.activate()
        # self.gripper.set_force(50)  # from 0 to 100 %
        # self.gripper.set_speed(100)

    def set_gripper_force(self, force):
        self.gripper.set_force(force)

    def set_gripper_speed(self, speed):
        # not tested yet
        self.gripper.set_speed(speed)

    def open_gripper(self):
        # position, speed, force
        self.gripper.move_and_wait_for_pos(0, 255, 255)

    def close_gripper(self):
        self.gripper.move(255, 255, 255)

    def open_gripper_width(self, width):
        self.gripper.move_and_wait_for_pos(255 - width, 255, 255)


    '''
    robot manipulation taks
    '''

    def go_to_middle(self):
        joint_state = [-5.40313069e-01, -1.57078326e+00, -1.57077610e+00, -1.57082667e+00, 1.57079339e+00, -1.07924091e-05]
        logging.info("Moving to middle position...")
        self.robot.move_joint_list(joint_state, 0.9, 0.9)

    def go_to_prepress(self):
        joint_state = [-1.282255, -1.5858809, -1.91530335, -1.21121486, 1.57113647, 0.62762904]
        logging.info("Moving to prepress position...")
        self.robot.move_joint_list(joint_state, 0.9, 0.9)

    def go_to_prebox(self):
        joint_state = [0.44573939, -1.41646136, -1.55788064, -1.73830094, 1.57065821, 0.17541628]
        logging.info("Moving to prebox position...")
        self.robot.move_joint_list(joint_state, 0.9, 0.9)

    def go_to_abovebox(self):
        joint_state = [1.42125487, -1.43969639, -1.42182171, -1.85106530, 1.57041836, 0.17556369]
        logging.info("Moving to above box position...")
        self.robot.move_joint_list(joint_state, 0.9, 0.9)

    def execute_vortex(self):
        logging.info("Starting vortex execution...")
        touch = [6.04667837e-03, -4.92560425e-01, 1.17129372e-01, -5.29484254e-01, -3.09456080e+00, 2.36695984e-03]
        press = [6.02982137e-03, -4.92554178e-01, 1.12534637e-01, -5.29485299e-01, -3.09452354e+00, 2.32032915e-03]
        # self.go_to_middle()
        self.go_to_prepress()
        logging.info("Touching...")
        self.robot.movel_tcp(touch, 0.5, 0.2) #touch pose
        self.open_gripper_width(48)
        logging.info("Pressing...")
        self.robot.movel_tcp(press, 0.5, 0.2) #press pose
        time.sleep(10) # sleep 10 seconds
        self.close_gripper()
        self.go_to_prepress()
        # self.go_to_middle()
        logging.info("Vortex execution completed.")

    def load_vial_to_box(self):
        logging.info("Starting loading vial into box...")
        pre_insertion = [0.1962527, 0.3966312, 0.19777181, -3.099553, 0.51071825, -0.00403169]
        insertion = [0.19633612, 0.39659809, 0.15939875, -3.09958536, 0.51078694, -0.00399349]
        self.go_to_prebox()
        self.go_to_abovebox()
        logging.info("Pre insertion...")
        self.robot.movel_tcp(pre_insertion, 0.5, 0.2) #pre_insertion pose
        logging.info("Inserting...")
        self.robot.movel_tcp(insertion, 0.5, 0.1) #pinsertionress pose
        self.open_gripper_width(48)
        self.robot.movel_tcp(pre_insertion, 0.9, 0.7) #pre_insertion pose
        self.go_to_abovebox()
        self.go_to_prebox()
        logging.info("VIal insertation completed.")

    def unload_vial_from_box(self):
        logging.info("Starting unloading vial from box...")
        pre_pick = [0.19633612, 0.39659809, 0.15939875, -3.09958536, 0.51078694, -0.00399349]
        pick = [0.19634887, 0.39660450, 0.15517973, -3.09952220, 0.51082113, -0.00397204]
        lift_up = [0.19614368, 0.39664403, 0.24424473, -3.09953466, 0.51069771, -0.00402063]
        self.go_to_prebox()
        self.go_to_abovebox()
        logging.info("Pre unload...")
        self.robot.movel_tcp(pre_pick, 0.5, 0.2) #pre_insertion pose
        logging.info("Inserting...")
        self.robot.movel_tcp(pick, 0.5, 0.1) #pinsertionress pose
        self.close_gripper()
        self.robot.movel_tcp(pre_pick, 0.5, 0.2) #pre_insertion pose
        self.robot.movel_tcp(lift_up, 0.5, 0.2) #pre_insertion pose
        self.go_to_abovebox()
        self.go_to_prebox()
        logging.info("VIal insertation completed.")

    def pick_vial_1(self):
        logging.info("Starting picking vial1 from the rack...")
        pre_pick = [-0.14479129, -0.49328619, 0.07697303, -0.53206640, -3.09373452, 0.00122079]
        pick = [-0.14484212, -0.49331475, 0.05350598, -0.53210167, -3.09375955, 0.00129685]
        lift_up = [-0.14484212, -0.49331475, 0.10350598, -0.53210167, -3.09375955, 0.00129685]
        logging.info("Pre pick...")
        self.robot.movel_tcp(pre_pick, 0.5, 0.2) #pre_insertion pose
        logging.info("Picking...")
        self.robot.movel_tcp(pick, 0.5, 0.2) #pinsertionress pose
        self.close_gripper()
        self.robot.movel_tcp(pre_pick, 0.5, 0.2) #pre_insertion pose
        self.robot.movel_tcp(lift_up, 0.8, 0.4) #pre_insertion pose
        logging.info("VIal picking completed.")

    def pick_vial(self, i):
        logging.info(f"Starting picking vial{i} from the rack...")
        pre_pick = self.pre_pick_positions[i]
        pick = self.pick_positions[i]
        lift_up = self.lift_up_positions[i]

        logging.info(f"Pre pick vial{i}...")
        self.robot.movel_tcp(pre_pick, 0.5, 0.2)  # pre_insertion pose
        logging.info(f"Picking vial{i}...")
        self.robot.movel_tcp(pick, 0.5, 0.2)  # pick pose
        self.close_gripper()
        self.robot.movel_tcp(pre_pick, 0.5, 0.2)  # lift to pre_pick pose before lifting further
        self.robot.movel_tcp(lift_up, 0.8, 0.4)  # lift_up pose
        logging.info(f"Vial{i} picking completed.")

    def drop_vial_1(self):
        logging.info("Starting droping vial1 from the box...")
        # pre_pick = [-0.14479129, -0.49328619, 0.07697303, -0.53206640, -3.09373452, 0.00122079]
        drop = [-0.14484212, -0.49331475, 0.06050598, -0.53210167, -3.09375955, 0.00129685]
        pre_drop = [-0.14484212, -0.49331475, 0.13350598, -0.53210167, -3.09375955, 0.00129685]
        # [-0.14457422, -0.49460926, 0.05338074, -0.53147931, -3.09308695, 0.00448485]
        # self.go_to_middle()
        logging.info("Pre droping...")
        self.robot.movel_tcp(pre_drop, 0.5, 0.2) #pre_insertion pose
        logging.info("insertion...")
        self.robot.movel_tcp(drop, 0.3, 0.1) #pinsertionress pose
        self.open_gripper_width(60)
        self.robot.movel_tcp(pre_drop, 0.5, 0.2) #pre_insertion pose
        # self.robot.movel_tcp(lift_up, 0.8, 0.4) #pre_insertion pose
        logging.info("Vial dropping completed.")

    def drop_vial(self, i):
        logging.info(f"Starting dropping vial{i} into the box...")
        drop = self.drop_positions[i]
        pre_drop = self.pre_drop_positions[i]

        logging.info(f"Pre dropping vial{i}...")
        self.robot.movel_tcp(pre_drop, 0.5, 0.2)  # Pre-drop pose
        logging.info(f"Dropping vial{i}...")
        self.robot.movel_tcp(drop, 0.3, 0.1)  # Drop pose
        self.open_gripper_width(60)  
        self.robot.movel_tcp(pre_drop, 0.5, 0.2)  # Move back to pre-drop pose
        logging.info(f"Vial{i} dropping completed.")

    def capture_image(self, i):
        camera_index=0
        image_path='image/image_vial_{i}.jpg'
        # Initialize the webcam
        cap = cv2.VideoCapture(camera_index)

        if not cap.isOpened():
            print("Error: Could not open webcam.")
            return

        # Capture a single frame
        ret, frame = cap.read()

        # Check if capture was successful
        if not ret:
            print("Error: Could not read frame from webcam.")
            return

        # Save the captured image
        cv2.imwrite(image_path, frame)
        print(f"image_vial_{i} saved as {image_path}")

        # Release the webcam
        cap.release()

    def capture_image_base64(self, i):
        camera_index = 0
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            print("Error: Could not open webcam.")
            return
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from webcam.")
            return
        success, encoded_frame = cv2.imencode('.jpg', frame)
        if not success:
            print("Error: Could not read frame from webcam.")
            return
        base64_img = base64.b64encode(encoded_frame).decode('utf-8')
        cap.release()
        return base64_img


# # Example of usage
# if __name__ == "__main__":
#     tasks = URTasks(ip="192.168.56.6", port=30003)
#     tasks.initialize_robot()
#     tasks.go_home()
#     tasks.activate_gripper()
#     tasks.move_to_position([0.5, 0.0, 0.5, 0, 3.1415, 0])  # Example target position
#     tasks.set_digital_output(0, True)  # Example digital output operation
#     tasks.finalize_robot()
