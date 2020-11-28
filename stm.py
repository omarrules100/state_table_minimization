import sys
from modules.import_csv import import_file
from modules.pairchart import pairchart


def main():
    """ program accepts 1 argument which is the state table file """

    if len(sys.argv) > 1:
        for arg in sys.argv[1:2]:
            print(f'Minimizing state table in "{arg}"...\n')
            state_table = import_file(arg)
            if state_table is None:
                print(f'State table in "{arg}" could not be processed')
            else:
                # TODO: error check state table format
                for key, val in state_table.items():
                    print(f'{key}: {val}')
                num_states = len(state_table) - 1
                num_inputs = int(len(state_table['STATE'])/2)
                print(f'Number of states: {num_states}')
                print(f'Number of inputs: {num_inputs}\n')
                pairchart(state_table, num_states, num_inputs)

    else:
        print('ERROR state table file must be specified')


if __name__ == "__main__":
    # execute only if run as a script
    main()
