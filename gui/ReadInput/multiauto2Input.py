import csv
from PyQt6.QtCore import QPointF

gauge_mean = []
gauge_dist = []
gauge_sd = []
gauge_timer = []
mtr_auto1 = []
mtr_auto1_oas = None
mtr_auto1_clickable = None
mtr_auto2 = []
mtr_auto2_oas = None
mtr_auto2_clickable = None
nav_uav_x = []
nav_uav_y = []
nav_goal_x = []
nav_goal_y = []
nav_storm_x = []
nav_storm_y = []
nav_goal_pts = []
nav_uav_fuel = []
nav_uav_speed = []
nav_path_angle = []
nav_auto_path = None
nav_auto = []
nav_auto_oas = None
nav_auto_clickable = None
chat_timer = []
chat_auto = [] 
chat_auto_oas = None
chat_auto_clickable = None
duration = 0

def _as_bool(val, default=False):
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.strip().lower() == "true"
    return default

def read_multiauto2():
    try:

        with open('input_files/multiauto2_input.csv', 'r', newline='') as filename: 
            reader = csv.reader(filename)

            rows = list(reader)
              
            global gauge_mean, gauge_dist, gauge_sd, gauge_timer, mtr_auto1, mtr_auto1_oas, mtr_auto1_clickable, mtr_auto2, mtr_auto2_oas, mtr_auto2_clickable
            gauge_mean = [int(item) for item in rows[0][1:5]]
            gauge_dist = [int(item) for item in rows[1][1:5]]
            gauge_sd = [int(item) for item in rows[2][1:5]]
            gauge_timer = [int(item) for item in rows[3][1:3]]
            mtr_auto1  = [int(item) for item in rows[4][1:3]]
            mtr_auto1_oas = _as_bool(rows[5][1])
            mtr_auto1_clickable = _as_bool(rows[6][1])
            mtr_auto2  = [int(item) for item in rows[7][1:3]]
            mtr_auto2_oas = _as_bool(rows[8][1])
            mtr_auto2_clickable = _as_bool(rows[9][1])

            global nav_uav_x, nav_uav_y, nav_goal_x, nav_goal_y, nav_storm_x, nav_storm_y, nav_uav_fuel, nav_uav_speed
            nav_uav_x = [int(item) for item in rows[10][1:5]]
            nav_uav_y = [int(item) for item in rows[11][1:5]]      
            nav_goal_x = [int(item) for item in rows[12][1:5]]
            nav_goal_y = [int(item) for item in rows[13][1:5]]
            nav_storm_x = [int(item) for item in rows[14][1:5]]
            nav_storm_y = [int(item) for item in rows[15][1:5]]
            nav_uav_fuel = [int(item) for item in rows[16][1:5]]
            nav_uav_speed = [int(item) for item in rows[17][1:5]]

            global nav_path_angle, nav_auto_path, nav_auto, nav_auto_oas, nav_auto_clickable, chat_timer, chat_auto, chat_auto_oas, chat_auto_clickable, duration
            nav_path_angle = [int(item) for item in rows[18][1:5]]
            nav_auto_path = int(rows[19][1])
            nav_auto = [int(item) for item in rows[20][1:3]]
            nav_auto_oas = _as_bool(rows[21][1])
            nav_auto_clickable = _as_bool(rows[22][1])
            chat_timer = [int(item) for item in rows[23][1:3]]
            chat_auto = [int(item) for item in rows[24][1:3]]
            chat_auto_oas = _as_bool(rows[25][1])
            chat_auto_clickable = _as_bool(rows[26][1])

            duration = int(rows[27][1])

    except FileNotFoundError:
        print("file not found.")