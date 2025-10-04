import datetime
import csv
from participant import PARTICIPANT_ID


multi_log = []
total_score = 0


def LogMulti(block, trial, log_type, auto, auto_type, gauges, total_oob, total_reset, uavs, chat_box, answer, msg_time):
    
    curr_format = datetime.datetime.now().strftime("%H:%M:%S")
    curr_time = datetime.datetime.now()
    sum_goals = 0
    
    oob_time = []
    reset = []
    oob = []
    rxn_time = "NA"
 
    data_row = [
        PARTICIPANT_ID, 
        block,
        trial, 
        curr_format,
        log_type,
        str(auto),
        auto_type
        ]
  
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
            mtr_rxn_time = (curr_time - oob_time[i]).total_seconds()
            break

    data_row.extend([
        total_oob,
        total_reset,
        str(mtr_rxn_time)
    ])

    for uav in uavs:

        data_row.extend([
            str(uav.uav_item.is_moving),
            str(uav.is_idle),
            str(round(uav.fuel, 2)),
            str(uav.hyp_length),
            str(uav.hit_chancea / 100),
            str(uav.ra_length),
            str(uav.hit_chanceb / 100),
            str(uav.on_path),
            str(uav.storm_hit),
            str(uav.goal_item.idx),
            str(uav.at_goal),
            str(uav.total_goal_reached),
            str(uav.score),
        ])

        sum_goals += uav.total_goal_reached
        
        global total_score
        total_score += uav.score

    data_row.extend([
        str(sum_goals),
        str(total_score),
        chat_box[0],
        chat_box[1],
        answer
    ])

    if chat_box[1] != "N/A":
        chat_rxn_time = (curr_time - msg_time).total_seconds()

        data_row.extend([
            str(chat_rxn_time),
        ])

    else: 
        data_row.extend([
            "N/A",
        ])
    
    multi_log.append(data_row)

def MultiCSV(filename):

    file_header = [
        "participant_id", "block", "trial", "time", "type", "auto", "auto_type",
        "gauge1_level", "gauge1_oob", "gauge1_reset",
        "gauge2_level", "gauge2_oob", "gauge2_reset",
        "gauge3_level", "gauge3_oob", "gauge3_reset",
        "gauge4_level", "gauge4_oob", "gauge4_reset",
        "total_oob", "total_reset", "mtr_rxn_time",
        "uav1_moving", "uav1_idle", "uav1_fuel", "uav1_patha_length", "uav1_patha_stormchance", "uav1_pathb_length", "uav1_pathb_stormchance", "uav1_onpath", "uav1_stormhit", "uav1_goal", "uav1_atgoal", "uav1_goalsreached", "uav1_score",
        "uav2_moving", "uav2_idle", "uav2_fuel", "uav2_patha_length", "uav2_patha_stormchance", "uav2_pathb_length", "uav2_pathb_stormchance", "uav2_onpath", "uav2_stormhit", "uav2_goal", "uav2_atgoal", "uav2_goalsreached", "uav2_score",
        "uav3_moving", "uav3_idle", "uav3_fuel", "uav3_patha_length", "uav3_patha_stormchance", "uav3_pathb_length", "uav3_pathb_stormchance", "uav3_onpath", "uav3_stormhit", "uav3_goal", "uav3_atgoal", "uav3_goalsreached", "uav3_score",
        "uav4_moving", "uav4_idle", "uav4_fuel", "uav4_patha_length", "uav4_patha_stormchance", "uav4_pathb_length", "uav4_pathb_stormchance", "uav4_onpath", "uav4_stormhit", "uav4_goal", "uav4_atgoal", "uav4_goalsreached", "uav4_score",
        "total_goals_reached", "total_score",
        "message", "response", "correct_answer", "chat_rxn_time"
    ]

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(file_header)
        writer.writerows(multi_log)