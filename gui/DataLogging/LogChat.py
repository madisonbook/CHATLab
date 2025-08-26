import datetime
import csv
from participant import PARTICIPANT_ID

chat_log = []

def LogChat(block, trial, gauges, auto, auto_type, total_oob, total_reset):
    curr_format = datetime.datetime.now().strftime("%H:%M:%S")

    data_row = [
        PARTICIPANT_ID, 
        block,
        trial, 
        curr_format
        ]
    
    chat_log.append(data_row)

def ChatCSV(filename="output_files/chat_log.csv"):

    file_header = [
        "participant_id", "block", "trial", "time"
    ]

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(file_header)
        writer.writerows(chat_log)
