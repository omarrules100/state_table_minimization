# meisel's method


def meisel(state_list, pc_table):
    print("\nMinimizing with Meisel's Method...")

    state_frequency = {}
    for state in state_list:
        count = 0
        for key in pc_table:
            pc_states = key.split(',')
            if state in pc_states:
                count += 1
        state_frequency[state] = count

    print('State Frequencies:')
    choices_list = []
    for key, val in state_frequency.items():
        print(f'{key}: {val}')
        choice_tuple = (val, key)
        choices_list.append(choice_tuple)
    choices_list = sorted(choices_list)

    print('State Order:')
    order_string = ''
    for freq, state in choices_list:
        order_string += f'{state}, '
    order_string = order_string[:-2]
    print(order_string)
