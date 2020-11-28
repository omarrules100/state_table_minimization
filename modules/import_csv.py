# module for importing state table data from csv file
import csv


def import_file(file_name):
    state_table_temp = {}
    state_table = {}
    num_lines = 0

    try:
        with open(file_name, newline='') as csvfile:
            state_table_file = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in state_table_file:
                if row[0].startswith('#'):
                    continue
                num_lines += 1
                if num_lines == 1:
                    header = []
                    for element in row[1:]:
                        # eliminate first character if it is whitespace
                        if len(element) > 0 and element[0].isspace():
                            header.append(element[1:])
                        else:
                            header.append(element)
                    state_table_temp['STATE'] = header
                else:
                    state = []
                    for element in row[1:]:
                        # eliminate first character if it is whitespace
                        if len(element) > 0 and element[0].isspace():
                            state.append(element[1:])
                        else:
                            state.append(element)
                    state_table_temp[row[0]] = state

            if num_lines < 2:
                print('ERROR in input file. Must contain a header row and at least one state')
                return None
            else:
                # convert blanks to "-"
                for key, val in state_table_temp.items():
                    new_val = []
                    for element in val:
                        if val in ['', ' ']:
                            new_val.append('-')
                        else:
                            new_val.append(element)
                    state_table[key] = new_val
                return state_table

    except Exception as e:
        print(f'ERROR "{e}" opening state table file "{file_name}"')
        return None
