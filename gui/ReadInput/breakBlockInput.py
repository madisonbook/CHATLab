
break1 = ""
break2 = ""
break3 = ""

def read_break():
    try:

        with open('input_files/break_block_input.txt', 'r') as f:
            rows = [line.strip() for line in f.readlines() if line.strip()]

            global break1, break2, break3
            if len(rows) > 0:
                break1 = rows[0]
                print(f"{break1}")
            if len(rows) > 1:
                break2 = rows[1]
            if len(rows) > 2:
                break3 = rows[2]

    except FileNotFoundError:
        print("file not found.")