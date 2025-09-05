
break1 = ""
break2 = ""
break3 = ""
break4 = ""

def read_break():
    try:

        with open('input_files/break_block_input.txt', 'r') as f:
            rows = [line.strip() for line in f.readlines() if line.strip()]

            global break1, break2, break3, break4
            if len(rows) > 0:
                break1 = rows[0]
            if len(rows) > 1:
                break2 = rows[1]
            if len(rows) > 2:
                break3 = rows[2]
            if len(rows) > 3:
                break4 = rows[3]

    except FileNotFoundError:
        print("file not found.")