import csv
from PyQt6.QtCore import QPointF

gauge_mean = []
gauge_dist = []
gauge_sd = []
gauge_timer = []
mtr_auto = []
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
chat_timer = []
chat_auto = [] 
duration = 0

def read_multiauto1():
    try:

        with open('input_files/multiauto1_input.csv', 'r', newline='') as filename: 
            reader = csv.reader(filename)

            rows = list(reader)
              
            global gauge_mean, gauge_dist, gauge_sd, gauge_timer, mtr_auto
            gauge_mean = [int(item) for item in rows[0][1:5]]
            gauge_dist = [int(item) for item in rows[1][1:5]]
            gauge_sd = [int(item) for item in rows[2][1:5]]
            gauge_timer = [int(item) for item in rows[3][1:3]]
            mtr_auto = [int(item) for item in rows[4][1:3]]

            global nav_uav_x, nav_uav_y, nav_goal_x, nav_goal_y, nav_storm_x, nav_storm_y, nav_uav_fuel, nav_uav_speed
            nav_uav_x = [int(item) for item in rows[5][1:5]]
            nav_uav_y = [int(item) for item in rows[6][1:5]]      
            nav_goal_x = [int(item) for item in rows[7][1:5]]
            nav_goal_y = [int(item) for item in rows[8][1:5]]
            nav_storm_x = [int(item) for item in rows[9][1:5]]
            nav_storm_y = [int(item) for item in rows[10][1:5]]
            nav_uav_fuel = [int(item) for item in rows[11][1:5]]
            nav_uav_speed = [int(item) for item in rows[12][1:5]]

            global nav_path_angle, nav_auto_path, nav_auto, chat_timer, chat_auto, duration
            nav_path_angle = [int(item) for item in rows[13][1:5]]
            nav_auto_path = int(rows[14][1])
            nav_auto = [int(item) for item in rows[15][1:3]]
            chat_timer = [int(item) for item in rows[16][1:3]]
            chat_auto = [int(item) for item in rows[17][1:3]]

            duration = int(rows[18][1])

    except FileNotFoundError:
        print("file not found.")