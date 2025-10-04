import datetime
import csv
from participant import PARTICIPANT_ID

chat_log = []

def LogChatBox(block, trial, chat_box, answer, msg_time, auto, auto_type):
    curr_format = datetime.datetime.now().strftime("%H:%M:%S")
    curr_time = datetime.datetime.now()

    data_row = [
        PARTICIPANT_ID, 
        block,
        trial, 
        curr_format,
        auto,
        auto_type,
        chat_box[0],
        chat_box[1],
        answer
        ]
    
    if chat_box[1] != "N/A":
        rxn_time = (curr_time - msg_time).total_seconds()

        data_row.extend([
            str(rxn_time),
        ])

    else: 
        data_row.extend([
            "N/A",
        ])
    
    chat_log.append(data_row)

def ChatBoxCSV(filename="output_files/chat_log.csv"):

    file_header = [
        "participant_id", "block", "trial", "time", "auto", "auto_type", "message", "response", "correct_answer", "rxn_time"
    ]

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(file_header)
        writer.writerows(chat_log)
