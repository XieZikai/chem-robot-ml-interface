# ur_tasks.py
from UR_Functions import URfunctions as URControl
from robotiq.robotiq_gripper import RobotiqGripper
import time
import logging
import cv2
import subprocess

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class URTasks:
    def __init__(self, ip, port):
        self.robot = URControl(ip=ip, port=port)
        self.gripper = RobotiqGripper()
        self.gripper.connect(ip, 63352)

        # config for vials on rack
        self.pre_pick_positions = {
            1: [-0.66589974, -0.20379388, 0.13137952, -2.21642963, -2.22291281, -0.00233657],
            2: [-0.66538524, -0.17317440, 0.13137952, -2.21645299, -2.22291237, -0.00230370],
            3: [-0.66559643, -0.14172159, 0.13137952, -2.21644114, -2.22288320, -0.00228241],
            4: [-0.63022081, -0.20457515, 0.13137952, -2.21651423, -2.22287894, -0.00230820],
            5: [-0.62946385, -0.17302826, 0.13137952, -2.21649441, -2.22288843, -0.00237794],
            6: [-0.62934022, -0.14159531, 0.13137952, -2.21649715, -2.22288662, -0.00236626],
            7: [-0.59448554, -0.20544908, 0.13137952, -2.21653413, -2.22285360, -0.00233571],
            8: [-0.59440349, -0.17361159, 0.13137952, -2.21646346, -2.22288782, -0.00233906],
            9: [-0.59410049, -0.14283781, 0.13137952, -2.21646861, -2.22290356, -0.00236967],
            10: [-0.56015778, -0.20571312, 0.13137952, -2.21650893, -2.22288711, -0.00234869],
            11: [-0.55886497, -0.17509215, 0.13137952, -2.21649270, -2.22287041, -0.00234114],
            12: [-0.55976000, -0.14300520, 0.13137952, -2.21647773, -2.22281458, -0.00225424],
            # Add more pre_pick positions for other vials here
        }
        self.pick_positions = {
            1: [-0.66589974, -0.20379388, 0.11137952, -2.21642963, -2.22291281, -0.00233657],
            2: [-0.66538524, -0.17317440, 0.11137952, -2.21645299, -2.22291237, -0.00230370],
            3: [-0.66559643, -0.14172159, 0.11137952, -2.21644114, -2.22288320, -0.00228241],
            4: [-0.63022081, -0.20457515, 0.11137952, -2.21651423, -2.22287894, -0.00230820],
            5: [-0.62946385, -0.17302826, 0.11137952, -2.21649441, -2.22288843, -0.00237794],
            6: [-0.62934022, -0.14159531, 0.11137952, -2.21649715, -2.22288662, -0.00236626],
            7: [-0.59448554, -0.20544908, 0.11137952, -2.21653413, -2.22285360, -0.00233571],
            8: [-0.59440349, -0.17361159, 0.11137952, -2.21646346, -2.22288782, -0.00233906],
            9: [-0.59410049, -0.14283781, 0.11137952, -2.21646861, -2.22290356, -0.00236967],
            10: [-0.56015778, -0.20571312, 0.11137952, -2.21650893, -2.22288711, -0.00234869],
            11: [-0.55886497, -0.17509215, 0.11137952, -2.21649270, -2.22287041, -0.00234114],
            12: [-0.55976000, -0.14300520, 0.11137952, -2.21647773, -2.22281458, -0.00225424],
            # Add more pick positions for other vials here
        }
        self.lift_up_positions = {
            1: [-0.15621129, -0.49208866, 0.12350598, -0.53199980, -3.09373162, 0.00136558],
            2: [-0.18597074, -0.48020008, 0.12350598, -0.53204346, -3.09369404, 0.00119162],
            3: [-0.21458722, -0.46806314, 0.12350598, -0.53202747, -3.09370036, 0.00129175],
            # Add more lift_up positions for other vials here
        }

        self.drop_positions = {
            1: [-0.66589974, -0.20379388, 0.12264361, -2.21642963, -2.22291281, -0.00233657],
            2: [-0.66538524, -0.17317440, 0.12264361, -2.21645299, -2.22291237, -0.00230370],
            3: [-0.66559643, -0.14172159, 0.12264361, -2.21644114, -2.22288320, -0.00228241],
            4: [-0.63022081, -0.20457515, 0.12264361, -2.21651423, -2.22287894, -0.00230820],
            5: [-0.62946385, -0.17302826, 0.12264361, -2.21649441, -2.22288843, -0.00237794],
            6: [-0.62934022, -0.14159531, 0.12264361, -2.21649715, -2.22288662, -0.00236626],
            7: [-0.59448554, -0.20544908, 0.12264361, -2.21653413, -2.22285360, -0.00233571],
            8: [-0.59440349, -0.17361159, 0.12264361, -2.21646346, -2.22288782, -0.00233906],
            9: [-0.59410049, -0.14283781, 0.12264361, -2.21646861, -2.22290356, -0.00236967],
            10: [-0.56015778, -0.20571312, 0.12264361, -2.21650893, -2.22288711, -0.00234869],
            11: [-0.55886497, -0.17509215, 0.12264361, -2.21649270, -2.22287041, -0.00234114],
            12: [-0.55976000, -0.14300520, 0.12264361, -2.21647773, -2.22281458, -0.00225424],
            # Add more drop positions for other vials here
        }
        self.pre_drop_positions = {
            1: [-0.66589974, -0.20379388, 0.19264361, -2.21642963, -2.22291281, -0.00233657],
            2: [-0.66538524, -0.17317440, 0.19264361, -2.21645299, -2.22291237, -0.00230370],
            3: [-0.66559643, -0.14172159, 0.19264361, -2.21644114, -2.22288320, -0.00228241],
            4: [-0.63022081, -0.20457515, 0.19264361, -2.21651423, -2.22287894, -0.00230820],
            5: [-0.62946385, -0.17302826, 0.19264361, -2.21649441, -2.22288843, -0.00237794],
            6: [-0.62934022, -0.14159531, 0.19264361, -2.21649715, -2.22288662, -0.00236626],
            7: [-0.59448554, -0.20544908, 0.19264361, -2.21653413, -2.22285360, -0.00233571],
            8: [-0.59440349, -0.17361159, 0.19264361, -2.21646346, -2.22288782, -0.00233906],
            9: [-0.59410049, -0.14283781, 0.19264361, -2.21646861, -2.22290356, -0.00236967],
            10: [-0.56015778, -0.20571312, 0.19264361, -2.21650893, -2.22288711, -0.00234869],
            11: [-0.55886497, -0.17509215, 0.19264361, -2.21649270, -2.22287041, -0.00234114],
            12: [-0.55976000, -0.14300520, 0.19264361, -2.21647773, -2.22281458, -0.00225424],
            # Add more pre_drop positions for other vials here
        }
        self.rack_picking_positions = {
        1: [-0.49766155, -0.08005486, 0.08958987, -1.75489505, -1.76201120, 0.72886448],
        2: [-0.49713261, 0.01301709, 0.09099987, -1.75485895, -1.76205962, 0.72885306],
        3: [-0.49612682, 0.10694698, 0.09077318, -1.75483278, -1.76198852, 0.72879575],
        4: [-0.49531810, 0.19990543, 0.09142524, -1.75488775, -1.76204965, 0.72879855],
        5: [-0.21458722, -0.46806314, 0.13350598, -0.53202747, -3.09370036, 0.00129175],
        # Add more pre_drop positions for other racks here
        }
        self.above_rack_picking_positions = {
        1: [-0.49766092, -0.08006544, 0.19142524, -1.75487583, -1.76204692, 0.72887410],
        2: [-0.49713261, 0.01301709, 0.19142524, -1.75485895, -1.76205962, 0.72885306],
        3: [-0.49612682, 0.10694698, 0.19142524, -1.75483278, -1.76198852, 0.72879575],
        4: [-0.49531810, 0.19990543, 0.19142524, -1.75488775, -1.76204965, 0.72879855],
        5: [-0.21458722, -0.46806314, 0.13350598, -0.53202747, -3.09370036, 0.00129175],
        # Add more pre_drop positions for other racks here
        }

        self.rack_picking_positions_shelf = {
        1: [-0.60188087, 0.12404068, 0.54251319, -2.36690799, -0.03411182, -0.00540021],
        2: [-0.46929819, 0.12265601, 0.54236534, -2.36690056, -0.03416486, -0.00546280],
        3: [-0.60341312, 0.07570277, 0.38172867, -2.36729199, -0.00475407, -0.00575596],
        4: [-0.47208731, 0.07624415, 0.38153452, -2.36330020, -0.01361920, -0.01630257],
        5: [-0.60423117, 0.07493371, 0.22613581, -2.36331603, -0.01367552, -0.01632217],
        6: [-0.47079469, 0.07516056, 0.22632262, -2.36713427, -0.01371642, -0.01630298],
        # Add more pre_drop positions for other vials here
        }
        self.above_rack_picking_shelf = {
        1: [-0.60187701, 0.12405047, 0.55538694, -2.36691872, -0.03412619, -0.00546498],
        2: [-0.46929819, 0.12265601, 0.55538694, -2.36690056, -0.03416486, -0.00546280],
        3: [-0.60341312, 0.07570277, 0.39454858, -2.36729199, -0.00475407, -0.00575596],
        4: [-0.47209071, 0.07624862, 0.39454858, -2.36328350, -0.01364732, -0.01632718],
        5: [-0.60422580, 0.07495113, 0.23838443, -2.36330733, -0.01366827, -0.01641308],
        6: [-0.47079469, 0.07516056, 0.23838443, -2.36713427, -0.01371642, -0.01630298],
        # Add more pre_drop positions for other vials here
        }

        self.rack_pre_picking_shelf = {
        1: [-0.60187701, 0.12405047-0.02, 0.55538694, -2.36691872, -0.03412619, -0.00546498],
        2: [-0.46929819, 0.12265601-0.02, 0.55538694, -2.36690056, -0.03416486, -0.00546280],
        3: [-0.60341312, 0.07570277-0.02, 0.39454858, -2.36729199, -0.00475407, -0.00575596],
        4: [-0.47209071, 0.07624862-0.02, 0.39454858, -2.36328350, -0.01364732, -0.01632718],
        5: [-0.60422580, 0.07495113-0.02, 0.23838443, -2.36330733, -0.01366827, -0.01641308],
        6: [-0.47079469, 0.07516056-0.02, 0.23838443, -2.36713427, -0.01371642, -0.01630298],
        # Add more pre_drop positions for other vials here
        }
        # js
        self.rack_transfer = {
        1: [0.17490527, -1.81201949, 1.56054527, -1.97223916, -2.06451589, 0.60280871],
        2: [0.25136906, -2.03658213, 1.68949110, -1.84155287, -2.10952884, 0.67326355],
        3: [0.18128081, -1.86140313, 1.99800522, -2.35726990, -2.06936580, 0.60922706],
        4: [0.25141478, -2.09843888, 2.12590295, -2.21566167, -2.11040336, 0.67409033],
        5: [0.07113234, -1.75082078, 2.33595735, -2.83919921, -2.00077278, 0.51020914],
        6: [0.17870784, -1.99840655, 2.49405581, -2.65664496, -2.15560991, 0.69171482],
        # Add more pre_drop positions for other vials here
        }

        # self.pre_rack_picking_positions = {
        # 1: [-0.15621129, -0.49208866, 0.13350598, -0.53210167, -3.09375955, 0.00129685],
        # 2: [-0.18597074, -0.48020008, 0.13350598, -0.53206121, -3.09374346, 0.00123783],
        # 3: [-0.21458722, -0.46806314, 0.13350598, -0.53202747, -3.09370036, 0.00129175],
        # 4: [-0.21458722, -0.46806314, 0.13350598, -0.53202747, -3.09370036, 0.00129175],
        # 5: [-0.21458722, -0.46806314, 0.13350598, -0.53202747, -3.09370036, 0.00129175],
        # # Add more pre_drop positions for other vials here
        # }
        # self.pre_rack_dropping_positions = {
        # 1: [-0.15621129, -0.49208866, 0.13350598, -0.53210167, -3.09375955, 0.00129685],
        # 2: [-0.18597074, -0.48020008, 0.13350598, -0.53206121, -3.09374346, 0.00123783],
        # 3: [-0.21458722, -0.46806314, 0.13350598, -0.53202747, -3.09370036, 0.00129175],
        # 4: [-0.21458722, -0.46806314, 0.13350598, -0.53202747, -3.09370036, 0.00129175],
        # 5: [-0.21458722, -0.46806314, 0.13350598, -0.53202747, -3.09370036, 0.00129175],
        # # Add more pre_drop positions for other vials here (not used here)
        # }
        self.above_vial_manipulation_pos = [-0.49804872, -0.17401378, 0.17414927, -1.75489539, -1.76208882, 0.72880159]
        self.vial_manipulation_pos = [-0.49808122, -0.17402322, 0.08971895, -1.75481869, -1.76202418, 0.72891174]
        self.pre_g_vial_manipulation_pos = [-0.47763001, -0.17401059, 0.11013240, -1.75479692, -1.76197776, 0.72894444]


    def initialize_robot(self):
        """Initializes robot connection and prepares it for operations."""
        self.robot.reconnect_socket()
        print("Robot initialized and ready.")
        
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

    def go_to_test_j(self, joint_state):

        self.robot.move_joint_list(joint_state, 0.9, 0.9)

    def get_joint_states(self):
        js = self.robot.get_current_joint_positions()
        formatted_js = ', '.join([f"{val:.8f}" for val in js]) 
        print('joint state, 'f"[{formatted_js}]")
        # print(js)
        return js

    def get_tcp(self):
        tcp = self.robot.get_current_tcp()
        formatted_tcp = ', '.join([f"{val:.8f}" for val in tcp]) 
        print('tcp pose', f"[{formatted_tcp}]")
        # print(tcp)
        return tcp

    '''
    Gripper command
    '''

    def activate_gripper(self):
        print('activate gripper')
        self.gripper.activate()

    def set_gripper_force(self, force):
        self.gripper.set_force(force)

    def set_gripper_speed(self, speed):
        # not tested yet
        self.gripper.set_speed(speed)

    def open_gripper(self):
        # position, speed, force
        self.gripper.move_and_wait_for_pos(0, 255, 255)

    def close_gripper(self, speed = 255, force = 255):
        self.gripper.move(255, speed, force)

    def open_gripper_width(self, width, speed = 255, force = 255):
        self.gripper.move_and_wait_for_pos(255 - width, speed, force)


    '''
    robot manipulation taks
    '''

    def go_to_middle(self):
        joint_state = [1.30902326, -2.16972746, 1.98439867, -1.38549821, -1.57015211, -0.00296575]
        logging.info("Moving to middle position...")
        self.robot.move_joint_list(joint_state, 1.4, 1.05, 0.02)

    def go_to_prepress(self):
        joint_state = [-1.282255, -1.5858809, -1.91530335, -1.21121486, 1.57113647, 0.62762904]
        logging.info("Moving to prepress position...")
        self.robot.move_joint_list(joint_state, 0.9, 0.9)

    def go_to_prebox(self):
        joint_state = [1.99689364, -2.05490031, 1.55281717, -1.06344552, -1.56912166, -1.14483673]
        logging.info("Moving to prebox position...")
        self.robot.move_joint_list(joint_state, 1.4, 1.05, 0.02)

    def go_to_abovebox(self):
        joint_state = [2.82861519, -1.74432435, 1.38056070, -1.20196666, -1.56511623, -0.31242305]
        logging.info("Moving to above box position...")
        self.robot.move_joint_list(joint_state, 1.4, 1.05)

    def go_home(self):
        joint_state = [0.00000744, -1.57083954, 1.57082969, -1.57077511, -1.57079918, -0.00003463]
        logging.info("Moving to home position...")
        self.robot.move_joint_list(joint_state, 1.4, 1.05, 0.02)

    def go_avoid(self):
        joint_state = [0.39507231, -1.78891911, 1.77036840, -1.58379140, -1.59763319, -0.64901668]
        logging.info("Moving to avoid position...")
        self.robot.move_joint_list(joint_state, 0.9, 0.9, 0.02)

    def go_test(self):
        joint_state = [0.17870784, -1.99840655, 2.49405581, -2.65664496, -2.15560991, 0.69171482]
        logging.info("Moving to test position...")
        self.robot.move_joint_list(joint_state, 0.9, 0.9, 0.02)

    def move_up(self, length):
        tcp = self.get_tcp()
        tcp[2] += length # mm
        logging.info("Moving up...")
        self.robot.movel_tcp(tcp, 0.5, 0.2)

    def move_back(self, length):
        tcp = self.get_tcp()
        tcp[1] -= length
        logging.info("Moving back...")
        self.robot.movel_tcp(tcp, 0.5, 0.2)

    def move_down(self, length):
        tcp = self.get_tcp()
        tcp[2] -= length
        logging.info("Moving down...")
        self.robot.movel_tcp(tcp, 0.5, 0.2)

    def go_to_pre_record(self):
        pre_record = [0.37565906, 0.13484910, 0.54545234, 2.22110638, -2.21900675, -0.00766125]
        logging.info("pre recording...")
        self.robot.movel_tcp(pre_record, 1.2, 0.25)

    def go_to_stop_record(self):
        stop_record = [0.37567335, 0.13485381, 0.54547678, -1.20109176, 1.20251809, -1.21144601]
        logging.info("pre recording...")
        self.robot.movel_tcp(stop_record, 1.2, 0.25)

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
        pre_insertion = [0.40947352, 0.00606852, 0.25770348, 2.22268617, -2.22011031, -0.00807953]
        insertion = [0.40932377, 0.00620380, 0.21658348, 2.22264197, -2.22013810, -0.00805042]
        self.go_to_prebox()
        self.go_to_abovebox()
        logging.info("Pre insertion...")
        self.robot.movel_tcp(pre_insertion, 1.2, 0.2) #pre_insertion pose
        logging.info("Inserting...")
        self.robot.movel_tcp(insertion, 0.5, 0.1) #pinsertionress pose
        self.open_gripper_width(55)
        self.robot.movel_tcp(pre_insertion, 0.9, 0.7) #pre_insertion pose
        self.go_to_abovebox()
        self.go_to_prebox()
        logging.info("VIal insertation completed.")

    def unload_vial_from_box(self):
        logging.info("Starting unloading vial from box...")
        pre_pick = [0.40932764, 0.00622493, 0.22394163, -2.22267811, 2.22015937, 0.00786288]
        pick = [0.40932764, 0.00622493, 0.21394163, -2.22267811, 2.22015937, 0.00786288]
        lift_up = [0.40932764, 0.00622493, 0.27299250, -2.22267811, 2.22015937, 0.00786288]
        self.go_to_prebox()
        self.go_to_abovebox()
        logging.info("Pre unload...")
        self.robot.movel_tcp(pre_pick, 1.2, 0.2) #pre_insertion pose
        logging.info("Inserting...")
        self.robot.movel_tcp(pick, 0.5, 0.1) #pinsertionress pose
        time.sleep(0.5)
        self.close_gripper()
        self.robot.movel_tcp(pre_pick, 0.5, 0.2) #pre_insertion pose
        self.robot.movel_tcp(lift_up, 1.2, 0.2) #pre_insertion pose
        self.go_to_abovebox()
        self.go_to_prebox()
        logging.info("VIal insertation completed.")

    def pick_vial(self, i):
        logging.info(f"Starting picking vial{i} from the rack...")
        pre_pick = self.pre_pick_positions[i]
        pick = self.pick_positions[i]
        # lift_up = self.lift_up_positions[i]

        logging.info(f"Pre pick vial{i}...")
        self.robot.movel_tcp(pre_pick, 1.2, 0.2)  # pre_insertion pose
        logging.info(f"Picking vial{i}...")
        self.robot.movel_tcp(pick, 0.5, 0.2)  # pick pose
        self.close_gripper()
        self.robot.movel_tcp(pre_pick, 1.2, 0.2)  # lift to pre_pick pose before lifting further
        # self.robot.movel_tcp(lift_up, 0.8, 0.4)  # lift_up pose
        self.move_up(0.07)
        logging.info(f"Vial{i} picking completed.")


    def pick_place_rack(self, i):
        logging.info(f"Starting picking rack{i} from the bench")
        pre_pick = self.above_rack_picking_positions[i]
        pick = self.rack_picking_positions[i]
        
        logging.info(f"Pre pick rack{i}...")
        self.robot.movel_tcp(pre_pick, 0.5, 0.2)  # pre_insertion pose
        logging.info(f"Picking rack{i}...")
        self.robot.movel_tcp(pick, 0.5, 0.2)  # pick pose
        self.open_gripper_width(110, 50, 100) #pregrasp
        time.sleep(1)
        self.close_gripper()
        
        self.move_up(0.10)
        logging.info(f"Rack{i} picking completed.")

        # self.move_back(0.05)
        self.robot.movel_tcp(self.above_vial_manipulation_pos)
        # logging.info(f"Inserting Rack{i} ...")
        # self.robot.movel_tcp(self.vial_manipulation_pos)
        # self.open_gripper_width(200)
        # self.robot.movel_tcp(self.above_vial_manipulation_pos)
        # logging.info(f"Rack{i} placing completed.")

    def pick_place_rack_from_shelf(self, i):
        logging.info(f"Starting picking rack{i} from the shelf")
        pre_pick = self.rack_pre_picking_shelf[i]
        pick = self.rack_picking_positions_shelf[i]
        transfer = self.rack_transfer[i]
        
        logging.info(f"Pre pick rack{i}...")
        self.robot.movel_tcp(pre_pick, 1.2, 0.2)  # pre_insertion pose
        logging.info(f"Picking rack{i}...")
        self.robot.movel_tcp(pick, 0.5, 0.2)  # pick pose
        self.open_gripper_width(110, 50, 100) #pregrasp
        time.sleep(1)
        self.close_gripper()
        
        self.move_up(0.01287375)
        logging.info(f"Rack{i} picking completed.")
        self.move_back(0.160878)
        # self.move_back(0.05)
        self.robot.move_joint_list(transfer, 1.4, 1.05, 0.02)

        self.robot.movel_tcp(self.above_vial_manipulation_pos, 1.2, 0.2)
        logging.info(f"Inserting Rack{i} ...")
        self.robot.movel_tcp(self.vial_manipulation_pos)
        self.open_gripper_width(200)
        self.robot.movel_tcp(self.above_vial_manipulation_pos, 1.2, 0.2)
        logging.info(f"Rack{i} placing completed.")

    def test_rack(self):
        # all the rack positions have been tested
        i = 3
        pick = self.rack_picking_positions[i]
        above_pick = self.above_rack_picking_positions[i]
        self.robot.movel_tcp(above_pick, 0.5, 0.2)
        self.robot.movel_tcp(pick, 0.5, 0.2)
        # self.open_gripper_width(110, 50, 100)
        # time.sleep(1)
        # self.close_gripper()
        # self.robot.movel_tcp(above_pick, 0.5, 0.2)
        # self.robot.movel_tcp(self.above_vial_manipulation_pos)
        # self.robot.movel_tcp(self.vial_manipulation_pos)
        # self.open_gripper_width(200)
        # self.robot.movel_tcp(self.above_vial_manipulation_pos)
        # self.move_up(0.05)
        # self.open_gripper_width(60)

    def test_vial(self, i):
        # all the vial positions have been tested
        logging.info(f"Starting picking vial{i} from the rack...")
        pre_pick = self.pre_pick_positions[i]
        pick = self.pick_positions[i]
        # lift_up = self.lift_up_positions[i]

        logging.info(f"Pre pick vial{i}...")
        self.robot.movel_tcp(pre_pick, 0.5, 0.2)  # pre_insertion pose
        logging.info(f"Picking vial{i}...")
        self.robot.movel_tcp(pick, 0.5, 0.2)  # pick pose
        self.close_gripper()
        self.robot.movel_tcp(pre_pick, 0.5, 0.2)  # lift to pre_pick pose before lifting further
        # self.robot.movel_tcp(lift_up, 0.8, 0.4)  # lift_up pose
        self.move_up(0.07)
        logging.info(f"Vial{i} picking completed.")
        self.robot.movel_tcp(pre_pick, 0.5, 0.2)
        self.robot.movel_tcp(pick, 0.5, 0.2)  # pick pose
        self.open_gripper_width(60)
        self.move_up(0.07)


    def place_back_rack(self, i):
        logging.info(f"Starting dropping rack{i} back the bench")
        pre_drop = self.above_rack_picking_positions[i]
        drop = self.rack_picking_positions[i]

        self.robot.movel_tcp(self.pre_g_vial_manipulation_pos)
        logging.info(f"Picking rack{i}...")
        self.robot.movel_tcp(self.vial_manipulation_pos)
        self.open_gripper_width(110, 50, 100)
        time.sleep(1)
        self.close_gripper()
        self.move_up(0.10)

        logging.info(f"Pre drop rack{i}...")
        self.robot.movel_tcp(pre_drop, 0.5, 0.2)  # pre_insertion pose
        logging.info(f"Dropping rack{i}...")
        self.robot.movel_tcp(drop, 0.5, 0.2)  # pick pose
        self.open_gripper_width(200)
        self.move_up(0.05)
        logging.info(f"Rack{i} dropping completed.")

    def place_back_rack_to_shelf(self, i):
        logging.info(f"Starting dropping rack{i} back the bench")
        pre_drop = self.above_rack_picking_shelf[i]
        drop = self.rack_picking_positions_shelf[i]
        transfer = self.rack_transfer[i]

        self.robot.movel_tcp(self.pre_g_vial_manipulation_pos)
        logging.info(f"Picking rack{i}...")
        self.robot.movel_tcp(self.vial_manipulation_pos)
        self.open_gripper_width(110, 50, 100)
        time.sleep(1)
        self.close_gripper()
        self.move_up(0.10)

        logging.info(f"Pre drop rack{i}...")
        self.robot.move_joint_list(transfer, 0.9, 0.9, 0.02)
        self.robot.movel_tcp(pre_drop, 0.5, 0.2)  # pre_insertion pose
        logging.info(f"Dropping rack{i}...")
        self.robot.movel_tcp(drop, 0.5, 0.2)  # pick pose
        self.open_gripper_width(200)
        self.move_back(0.05)
        logging.info(f"Rack{i} dropping completed.")

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


    def set_camera_properties(self, device='/dev/video0', focus_value=255):
        try:
            # Disable autofocus
            subprocess.run(["v4l2-ctl", "-d", device, "-c", "focus_automatic_continuous=0"], check=True)
            # Set the desired focus value
            subprocess.run(["v4l2-ctl", "-d", device, "-c", f"focus_absolute={focus_value}"], check=True)
            # time.sleep(10)
            print(f"Focus set successfully to {focus_value}.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to set camera properties: {e}")

    def capture_image_focus_adjustment(self, vial_number, rack_number, sample_name, loop_iteration, device='/dev/video0', start_focus=95, end_focus=106, step=5, target_focus=105):
        # if acquired images are blur, adjust the start_focus into 110, end_focus into 130
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        if not cap.isOpened():
            print("Failed to open camera")
            return

        print("Adjusting focus...")
        for focus_value in range(start_focus, end_focus + step, step):
            self.set_camera_properties(device, focus_value)
            time.sleep(0.5)  # Shorter delay, continuous adjustment

            
            ret, frame = cap.read()
            if ret:
                # Optional: Display the live video feed to see focus changes
                # cv2.imshow('Live Feed', frame)
                if focus_value == target_focus:
                    filename = f'image/rack_{rack_number}_vial_{vial_number}_{sample_name.replace(" ", "_")}_loop{loop_iteration}.jpg'
                    # filename = f'image/rack_{rack_number}_vial_{vial_number}_{sample_name}_loop{loop_iteration}.jpg'
                    cv2.imwrite(filename, frame)
                    print(f"Image saved as {filename} at focus {focus_value}")

                if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
                    break

        cap.release()
        cv2.destroyAllWindows()


    def capture_image_focus_adjustment_test(self, filename, device='/dev/video0', start_focus=95, end_focus=106, step=5, target_focus=105):
        # if acquired images are blur, adjust the start_focus into 110, end_focus into 130
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        if not cap.isOpened():
            print("Failed to open camera")
            return

        print("Adjusting focus...")
        for focus_value in range(start_focus, end_focus + step, step):
            self.set_camera_properties(device, focus_value)
            time.sleep(0.5)  # Shorter delay, continuous adjustment

            
            ret, frame = cap.read()
            if ret:
                # Optional: Display the live video feed to see focus changes
                # cv2.imshow('Live Feed', frame)
                if focus_value == target_focus:
                    filename = f'{filename}.jpg'
                    # filename = f'image/rack_{rack_number}_vial_{vial_number}_{sample_name}_loop{loop_iteration}.jpg'
                    cv2.imwrite(filename, frame)
                    print(f"Image saved as {filename} at focus {focus_value}")

                if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
                    break

        cap.release()
        cv2.destroyAllWindows()

    def capture_image(self, i):
        camera_index=0
        # i = i
        image_path=f'image/image_vial_{i}.jpg'
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

# # Example of usage
# if __name__ == "__main__":
#     tasks = URTasks(ip="192.168.56.6", port=30003)
#     tasks.initialize_robot()
#     tasks.go_home()
#     tasks.activate_gripper()
#     tasks.move_to_position([0.5, 0.0, 0.5, 0, 3.1415, 0])  # Example target position
#     tasks.set_digital_output(0, True)  # Example digital output operation
#     tasks.finalize_robot()
