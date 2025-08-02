import datetime
import csv
from participant import PARTICIPANT_ID

navigation_log = []

def LogNavigation(block, trial, uavs, auto, auto_type):
    curr_format = datetime.datetime.now().strftime("%H:%M:%S")

    data_row = [
        PARTICIPANT_ID, 
        block,
        trial, 
        curr_format
        ]

    for uav in uavs:

        data_row.extend([
            str(uav.uav_item.is_moving),
            str(uav.is_idle),
            str(round(uav.fuel, 2)),
            str(uav.on_path)
        ])

    data_row.extend([
        str(auto),
        auto_type
    ])
    
    navigation_log.append(data_row)

def NavigationCSV(filename="output_files/navigation_log.csv"):

    file_header = [
        "participant_id", "block", "trial", "time",
        "uav1_moving", "uav1_idle", "uav1_fuel", "uav1_path",
        "uav2_moving", "uav2_idle", "uav2_fuel", "uav2_path",
        "uav3_moving", "uav3_idle", "uav3_fuel", "uav3_path",
        "uav4_moving", "uav4_idle", "uav4_fuel", "uav4_path",
        "auto", "auto_type"
    ]

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(file_header)
        writer.writerows(navigation_log)