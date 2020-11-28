# pairchart technique
import copy


class StatePair:
    compatible = None
    dependent = None

    def __init__(self):
        self.compatible = None
        self.dependent = []

    def __repr__(self):
        return f'StatePair()'

    def __str__(self):
        return f'compatible-{self.compatible}, dependencies-{self.dependent}'


def print_pairchart(pc):
    for key, val in pc.items():
        print(f'{key}:')
        for key2, val2 in val.items():
            print(f'  {key2}: {val2}')


def deep_compare_paircharts(pc1, pc2):
    if len(pc1) != len(pc2):
        return False
    for key, val in pc1.items():
        for key2, val2 in val.items():
            if f'{pc1[key][key2]}' != f'{pc2[key][key2]}':
                return False
    return True


def pairchart(state_table, num_states, num_inputs):
    pair_chart = {}
    print('Determining state compatibilities...')

    st = {}
    for key, val in state_table.items():
        if key.startswith('STATE'):
            continue
        else:
            st[key] = val

    # first pass based only on output
    for key, val in st.items():
        state_pairs = {}
        for key2, val2 in st.items():
            sp = StatePair()
            if key == key2:
                sp.compatible = True
            else:
                for i in range(num_inputs):
                    idx = i*2 + 1
                    if st[key][idx] != '-' and st[key2][idx] != '-':
                        if st[key][idx] != st[key2][idx]:
                            sp.compatible = False
            state_pairs[key2] = sp
        pair_chart[key] = state_pairs

    pair_chart_prev = {}
    while not deep_compare_paircharts(pair_chart_prev, pair_chart):
        pair_chart_prev = copy.deepcopy(pair_chart)
        for key, val in pair_chart.items():
            for key2, val2 in val.items():
                # compare state names for compatibility
                if val2.compatible is None and len(val2.dependent) == 0:
                    dependent = False  # assume compatible until shown otherwise
                    for i in range(num_inputs):
                        idx = i*2
                        ns1 = st[key][idx]
                        ns2 = st[key2][idx]
                        if ns1 != '-' and ns2 != '-':
                            compared_states = [key, key2]
                            # if the two states reference different non-blank NS and they are not the two being compared
                            if ns1 != ns2 and (ns1 not in compared_states or ns2 not in compared_states):
                                dependent = True
                                state1 = int(ns1)
                                state2 = int(ns2)
                                if state2 < state1:
                                    state_temp = state1
                                    state1 = state2
                                    state2 = state_temp
                                val2.dependent.append(f'{state1}&{state2}')
                    if not dependent:
                        val2.compatible = True
                # compare dependencies for compatibility

    print_pairchart(pair_chart)
