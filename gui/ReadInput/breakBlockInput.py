
break1 = ""
break2 = ""
break3 = ""
break4 = ""
break5 = ""
break6 = ""
break7 = ""
break8 = ""
break9 = ""
break10 = ""
break11 = ""
break12 = ""

def read_break():
    try:

        with open('input_files/break_block_input.txt', 'r') as f:
            rows = [line.rstrip('\n') for line in f]


        global break1, break2, break3, break4, break5, break6, break7, break8, break9, break10, break11, break12


        break1 = rows[0] if len(rows) > 0 else ""
        break2 = rows[1] if len(rows) > 1 else ""
        break3 = rows[2] if len(rows) > 2 else ""
        break4 = rows[3] if len(rows) > 3 else ""
        break5 = rows[4] if len(rows) > 4 else ""
        break6 = rows[5] if len(rows) > 5 else ""
        break7 = rows[6] if len(rows) > 6 else ""
        break8 = rows[7] if len(rows) > 7 else ""
        break9 = rows[8] if len(rows) > 8 else ""
        break10 = rows[9] if len(rows) > 9 else ""
        break11 = rows[10] if len(rows) > 10 else ""
        break12 = rows[11] if len(rows) > 11 else ""

    except FileNotFoundError:
        print("file not found.")