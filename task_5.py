'''
*****************************************************************************************
*
*                ===============================================
*                   Nirikshak Bot (NB) Theme (eYRC 2020-21)
*                ===============================================
*
*  This script is to implement Task 5 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD (now MOE) project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''

# Team ID:          [ Team-ID ]
# Author List:      [ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:         task_5.py
# Functions:        
#                   [ Comma separated list of functions in this file ]
# Global variables: 
#                     [ List of global variables defined in this file ]

# NOTE: Make sure you do NOT call sys.exit() in this code.

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
import numpy as np
import cv2
import os, sys
import traceback
import time
import math
import json

##############################################################

start_coord_4 = (0, 5)
start_coord_1, end_coords_1, end_coord_4 = (0, 0), (0, 0), (0, 0)
gate = True

# Importing the sim module for Remote API connection with CoppeliaSim
try:
    import sim

except Exception:
    print('\n[ERROR] It seems the sim.py OR simConst.py files are not found!')
    print('\n[WARNING] Make sure to have following files in the directory:')
    print(
        'sim.py, simConst.py and appropriate library - remoteApi.dll (if on Windows), remoteApi.so (if on Linux) or remoteApi.dylib (if on Mac).\n')

# Import 'task_1b.py' file as module
try:
    import task_1b

except ImportError:
    print('\n[ERROR] task_1b.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure task_1b.py is present in this current directory.\n')


except Exception as e:
    print('Your task_1b.py throwed an Exception. Kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)

# Import 'task_1a_part1.py' file as module
try:
    import task_1a_part1

except ImportError:
    print('\n[ERROR] task_1a_part1.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure task_1a_part1.py is present in this current directory.\n')


except Exception as e:
    print('Your task_1a_part1.py throwed an Exception. Kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)

# Import 'task_2a.py' file as module
try:
    import task_2a

except ImportError:
    print('\n[ERROR] task_2a.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure task_2a.py is present in this current directory.\n')


except Exception as e:
    print('Your task_2a.py throwed an Exception. Kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)

# Import 'task_2b.py' file as module
try:
    import task_2b

except ImportError:
    print('\n[ERROR] task_2b.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure task_2b.py is present in this current directory.\n')


except Exception as e:
    print('Your task_2b.py throwed an Exception. Kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)

# Import 'task_3.py' file as module
try:
    import task_3

except ImportError:
    print('\n[ERROR] task_3.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure task_3.py is present in this current directory.\n')


except Exception as e:
    print('Your task_3.py throwed an Exception. Kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)

# Import 'task_4a.py' file as module
try:
    import task_4a

except ImportError:
    print('\n[ERROR] task_4a.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure task_4a.py is present in this current directory.\n')


except Exception as e:
    print('Your task_4a.py throwed an Exception. Kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)


##############################################################


# NOTE:    YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:    send_color_and_collection_box_identified
#        Inputs:    ball_color and collection_box_name
#       Outputs:    None
#       Purpose:    1. This function should only be called when the task is being evaluated using
#                        test executable.
#                    2. The format to send the data is as follows:
#                       'color::collection_box_name'                   
def send_color_and_collection_box_identified(ball_color, collection_box_name):
    global client_id

    color_and_cb = [ball_color + '::' + collection_box_name]
    inputBuffer = bytearray()
    return_code, retInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(client_id,
                                                                                        'evaluation_screen_respondable_1',
                                                                                        sim.sim_scripttype_childscript,
                                                                                        'color_and_cb_identification',
                                                                                        [], [], color_and_cb,
                                                                                        inputBuffer,
                                                                                        sim.simx_opmode_blocking)


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################
def get_start_end_coord(data, cl):
    global start_coord_1, end_coord_1, end_coord_4
    tmp = data[cl][0]
    del data[cl][0]
    if tmp == "T1_CB1":
        end_coord_4 = (5, 9)
        start_coord_1 = (5, 0)
        end_coord_1 = (0, 4)
    elif tmp == "T1_CB2":
        end_coord_4 = (5, 9)
        start_coord_1 = (5, 0)
        end_coord_1 = (4, 9)
    elif tmp == "T1_CB3":
        end_coord_4 = (5, 9)
        start_coord_1 = (5, 0)
        end_coord_1 = (9, 5)

    return tmp


def draw_setpoint(client_id, coords, table):
    coppelia_coord = []

    for element in coords:
        coppelia_coord.append(((10 * element) - 45) / 100)

    inputBuffer = bytearray()

    return_code, retInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(client_id,
                                                                                        "top_plate_respondable_t" + str(table) + "_1",
                                                                                        sim.sim_scripttype_customizationscript,
                                                                                        "drawSetpoint", [],
                                                                                        coppelia_coord, [],
                                                                                        inputBuffer,
                                                                                        sim.simx_opmode_blocking)


def send_data_to_draw_path(client_id, path, n):
    coppelia_sim_coord_path = []

    for coord in path:
        for element in coord:
            coppelia_sim_coord_path.append(((10 * element) - 45) / 100)

    inputBuffer = bytearray()

    return_code, retInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(client_id,
                                                                                        "top_plate_respondable_t" + str(n) + "_1",
                                                                                        sim.sim_scripttype_customizationscript,
                                                                                        'drawPath', [],
                                                                                        coppelia_sim_coord_path, [],
                                                                                        inputBuffer,
                                                                                        sim.simx_opmode_blocking)

    ##################################################
def convert_path_to_pixels(path):
    pixel_path = []
    for coord in path:
        pixel_path.append((coord[0] * 128 + 64, coord[1] * 128 + 64))

    return pixel_path


def convert_pixel_to_path(coord):
    coord = [(coord[0] - 64) / 128, (coord[1] - 64) / 128]

    return coord


def traverse_path(pixel_path, table):
    global gate

    turns = []
    prev_turn = pixel_path[0]
    n = len(pixel_path)
    signx, signy = 1, 1
    tmp = 30
    for i in range(1, len(pixel_path) - 1):
        signx = -1 * np.sign(pixel_path[i][0] - pixel_path[i - 1][0])
        signy = -1 * np.sign(pixel_path[i][1] - pixel_path[i - 1][1])
        if (pixel_path[i][0] == pixel_path[i - 1][0] and pixel_path[i][1] == pixel_path[i + 1][1]) or \
                (pixel_path[i][1] == pixel_path[i - 1][1] and pixel_path[i][0] == pixel_path[i + 1][0]):
            turns.append([pixel_path[i][1] + signy * tmp, pixel_path[i][0] + signx * tmp])
            prev_turn = pixel_path[i]
        elif abs(prev_turn[0] - pixel_path[i][0]) > 100 or abs(prev_turn[1] - pixel_path[i][1]) > 100:
            turns.append([pixel_path[i][1] + signy * tmp, pixel_path[i][0] + signx * tmp])
            prev_turn = pixel_path[i]

    for i in range(0, len(turns)):
        if turns[i][0] < 70:
            turns[i][0] = turns[i][0] + 30
        if turns[i][0] > 1200:
            turns[i][0] = turns[i][0] - 35
        if turns[i][1] < 70:
            turns[i][1] = turns[i][1] + 30
        if turns[i][1] > 1200:
            turns[i][1] = turns[i][1] - 35

    turns.append([pixel_path[n - 1][1] + signy * 25, pixel_path[n - 1][0] + signx * 25])
    t1, t2 = 0, 0

    print("\nTurns array generated!", len(turns))

    cnt = 0
    for i in range(0, len(turns)):
        cnt = 0
        task_3.change_setpoint(turns[i])
        gate = True
        #draw_setpoint(client_id, convert_pixel_to_path(turns[i]), table)

        flag = 0
        while True:
            vision_sensor_image, image_resolution, return_code = task_2a.get_vision_sensor_image(client_id,
                table)

            transformed_image = task_2a.transform_vision_sensor_image(vision_sensor_image, image_resolution)
            warped_img = task_1b.applyPerspectiveTransform_vs(transformed_image)

            if warped_img is None:
                continue

            shapes = task_1a_part1.scan_image(warped_img, True)

            print(shapes)
            print("Current setpoint: ", turns[i])
            print("\n")
            if len(shapes) == 0:
                continue

            center_x = shapes['Circle'][1]
            center_y = shapes['Circle'][2]
            return_code_signal, t1_string = sim.simxGetStringSignal(client_id, 'time', sim.simx_opmode_streaming)

            if return_code_signal == 0:
                t1 = float(t1_string)

            if turns[i][0] + 30 > center_x > turns[i][0] - 30 and turns[i][
                1] + 30 > center_y > turns[i][1] - 30:
                while turns[i][0] + 30 > center_x > turns[i][0] - 30 and turns[i][
                    1] + 30 > center_y > turns[i][1] - 30:

                    print("\nInside safe zone!\n")

                    return_code_signal, t2_string = sim.simxGetStringSignal(client_id, 'time', sim.simx_opmode_buffer)

                    if return_code_signal == 0:
                        t2 = float(t2_string)

                    vision_sensor_image, image_resolution, return_code = task_2a.get_vision_sensor_image(client_id,
                        table)
                    transformed_image = task_2a.transform_vision_sensor_image(vision_sensor_image, image_resolution)
                    warped_img = task_1b.applyPerspectiveTransform_vs(transformed_image)

                    if warped_img is None:
                        continue

                    shapes = task_1a_part1.scan_image(warped_img, True)
                    if len(shapes) == 0:
                        continue

                    center_x = shapes['Circle'][1]
                    center_y = shapes['Circle'][2]

                    if t2 - t1 > 0.3:
                        print("Hue hue hue")
                        flag = 1
                        break
                    else:
                        print("Calling control logic 1!")

                        if gate:
                            print("Waiting1")
                            time.sleep(0)
                            gate = False
                            previous_error_x = turns[i][1] - center_x
                            previous_error_y = turns[i][0] - center_y
                            task_3.control_logic(center_x, center_y, table, client_id, previous_error_x, previous_error_y)
                        else:
                            task_3.control_logic(center_x, center_y, table, client_id, 0, 0)
            else:
                print("Calling control logic 2!")

                if gate:
                    print("Waiting2")
                    time.sleep(0)
                    gate = False
                    previous_error_y = turns[i][0] - center_x
                    previous_error_x = turns[i][1] - center_y
                    task_3.control_logic(center_x, center_y, table, client_id, previous_error_x, previous_error_y)
                else:
                    task_3.control_logic(center_x, center_y, table, client_id, 0, 0)

            if flag == 1:
                break

            print(i)
            if len(turns) -1 == i and cnt == 20:
                break
            else:
                cnt = cnt +1


def main(rec_client_id):
    maze_t4 = cv2.imread('maze_t4.jpg')
    maze_t1 = cv2.imread('maze_t1.jpg')
    print("Maze images read!\n")

    warped_img_t4 = task_1b.applyPerspectiveTransform(maze_t4)
    warped_img_t1 = task_1b.applyPerspectiveTransform(maze_t1)
    maze_array_t4 = task_1b.detectMaze(warped_img_t4)
    maze_array_t1 = task_1b.detectMaze(warped_img_t1)
    print("Maze array detected: \nT4: ", maze_array_t4, "T1: ", maze_array_t1)

    return_code = task_2b.send_data(rec_client_id, maze_array_t4, "top_plate_respondable_t4_1")
    return_code = task_2b.send_data(rec_client_id, maze_array_t1, "top_plate_respondable_t1_1")
    print("\nMaze generated!\n")

    with open("ball_details.json") as f:
        data = json.load(f)
    print(data)

    return_code = task_2a.start_simulation(rec_client_id)
    print("Simulation started!\n")

    task_3.init_setup(rec_client_id)

    shapes = {}
    while shapes.get("Circle") is None:
        img_vs5, res, _ = task_2b.get_vision_sensor_image(rec_client_id, 5)
        img = task_2b.transform_vision_sensor_image(img_vs5, res)
        shapes = task_1a_part1.scan_image(img, False)

    cl = shapes["Circle"][0]
    print(cl)
    tmp = get_start_end_coord(data, cl)
    send_color_and_collection_box_identified(cl, tmp)
    print(start_coord_1, end_coord_1, end_coord_4, start_coord_4)

    # start coord and end coord from json ---- for t_4 start coord = (0, 4) end coord depends on cl end coord = (5, 9)
    # for t_4
    path_t4 = task_4a.find_path(maze_array_t4, start_coord_4, end_coord_4)
    send_data_to_draw_path(rec_client_id, path_t4, 4)

    path_t1 = task_4a.find_path(maze_array_t1, start_coord_1, end_coord_1)
    send_data_to_draw_path(rec_client_id, path_t1, 1)

    print("\nPath sent to CoppeliaSim\n")
    pixel_path_t4 = convert_path_to_pixels(path_t4)
    print("Entering traverse path\n")
    traverse_path(pixel_path_t4, 4)
    print("Ball traversed!")
    time.sleep(1) # why this addition
    # for t_1 ----- for t_1 start coord = (0, 5) end coord depend on cl end coord = (0, 4)
    print("Path sent to CoppeliaSim")
    pixel_path_t1 = convert_path_to_pixels(path_t1)
    print("Entering traverse path\n")
    traverse_path(pixel_path_t1, 1)
    print("Ball traversed!")

    return_code = task_2a.stop_simulation(rec_client_id)

    ##################################################


# Function Name:    main (built in)
#        Inputs:    None
#       Outputs:    None
#       Purpose:    To call the main(rec_client_id) function written by teams when they
#                    run task_5.py only.

# NOTE: Write your solution ONLY in the space provided in the above functions. This function should not be edited.
if __name__ == "__main__":
    client_id = task_2a.init_remote_api_server()
    main(client_id)
