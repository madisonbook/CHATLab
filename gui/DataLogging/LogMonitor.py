import datetime
import csv
import os
from participant import PARTICIPANT_ID

monitor_log = []

def LogMonitor(block, trial, gauges, auto, auto_type, total_oob, total_reset):
    curr_time = datetime.datetime.now()
    curr_format = datetime.datetime.now().strftime("%m:%d:%Y_%H:%M:%S")

    data_row = [
        PARTICIPANT_ID, 
        block,
        trial, 
        curr_format,
        str(auto),
        auto_type
        ]
    
    oob_time = []
    reset = []
    oob = []
    rxn_time = "NA"
    
    for gauge in gauges:
        oob_time.append(gauge.oob_time)
        oob.append(gauge.oob)
        reset.append(gauge.reset)

        data_row.extend([
            str(round(gauge.monitor_level, 1)),
            str(gauge.oob),
            str(gauge.reset)
        ])

    for i in range(4): 
        if not oob[i] and reset[i]:
            rxn_time = (curr_time - oob_time[i]).total_seconds()
            break

    data_row.extend([
        total_oob,
        total_reset,
        str(rxn_time)
    ])

    monitor_log.append(data_row)

def MonitorCSV(filename="output_files/monitor_log.csv"):

    file_header = [
        "participant_id", "block", "trial", "time", "auto", "auto_type",
        "gauge1_level", "gauge1_oob", "gauge1_reset",
        "gauge2_level", "gauge2_oob", "gauge2_reset",
        "gauge3_level", "gauge3_oob", "gauge3_reset",
        "gauge4_level", "gauge4_oob", "gauge4_reset",
        "total_oob", "total_reset", "rxn_time"
    ]

    file_exists = os.path.exists(filename)
    write_header = not file_exists or os.path.getsize(filename) == 0

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)

        if write_header:
            writer.writerow(file_header)

        writer.writerows(monitor_log)
