# pairchart technique
INCOMPATIBLE = 0
COMPATIBLE = 1
UNRESOLVED = 2
MAX_PAIRCHART_LOOPS = 1000


class StatePair:
    """ object which shows compatibility for a pair of states and any dependencies """

    compatible = None
    dependent = None
    state1 = None
    state2 = None

    def __init__(self, state1, state2):
        self.compatible = None
        self.dependent = []
        self.state1 = state1
        self.state2 = state2

    def __repr__(self):
        return f'StatePair({self.state1}, {self.state2})'

    def __str__(self):
        return f'({self.state1},{self.state2}) compatible-{self.compatible}, dependencies-{self.dependent}'


def print_pairchart(pc):
    """ formatted output string for a pairchart """

    for key, val in pc.items():
        print(f'{key}:')
        for key2, val2 in val.items():
            print(f'  {key2}: {val2}')


def deep_compare_paircharts(pc1, pc2):
    """
    deep compare of two paircharts and all their elements
    :param pc1: dictionary
    :param pc2: dictionary
    :return: True if they are equal, False if they differ on any element
    """

    if len(pc1) != len(pc2):
        return False
    for key, val in pc1.items():
        for key2, val2 in val.items():
            if f'{pc1[key][key2]}' != f'{pc2[key][key2]}':
                return False
    return True


def pairchart_resolved(pc):
    """
    Checks a pairchart to see if compatibility has been determined for each pair of states
    :param pc: dictionary
    :return: True if complete compatibility has been determined, False otherwise
    """
    for key, val in pc.items():
        for key2, val2 in val.items():
            if val2.compatible is None:
                return False
    return True


def iterative_path(pair_chart, dependency_start, dependency_current, dependency_list):
    """
    Function which checks a dependency's subdependencies for pairchart compatibility
    A closed loop back to initial pair indicates compatibility
    :param pair_chart: dictionary
    :param dependency_start: string
    :param dependency_current: string
    :param dependency_list: list
    :return: COMPATIBLE, INCOMPATIBLE, UNRESOLVED
    """
    new_list = dependency_list.copy()
    new_list.append(dependency_current)
    # closed loop back to start indicates compatibility
    if len(dependency_list) > 0 and dependency_current == dependency_start:
        return COMPATIBLE
    # loop back to somewhere other than start indicates no resolution (yet)
    elif len(dependency_list) > 0 and dependency_current in dependency_list:
        return UNRESOLVED
    else:
        state1, state2 = dependency_current.split(',')
        if pair_chart[state1][state2].compatible is True or pair_chart[state2][state1].compatible is True:
            return COMPATIBLE
        elif pair_chart[state1][state2].compatible is False or pair_chart[state2][state1].compatible is False:
            return INCOMPATIBLE
        else:
            compatible = None
            for dependency in pair_chart[state1][state2].dependent:
                path_explore = iterative_path(pair_chart, dependency_start, dependency, new_list)
                if path_explore == COMPATIBLE:
                    if compatible is None:
                        compatible = True
                elif path_explore == UNRESOLVED:
                    if compatible is True:
                        compatible = UNRESOLVED
                elif path_explore == INCOMPATIBLE:
                    compatible = False
            if compatible == COMPATIBLE:
                return COMPATIBLE
            elif compatible == INCOMPATIBLE:
                return INCOMPATIBLE
            else:
                return UNRESOLVED


def pairchart(state_table, num_inputs):
    """
    Function which creates a pairchart dictionary from a given state table
    :param state_table: dictionary
    :param num_inputs: int
    :return: pairchart dictionary
    """
    pair_chart = {}
    print('\nDetermining state compatibilities...')

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
            sp = StatePair(key, key2)
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

    loops = 0
    while not pairchart_resolved(pair_chart) and loops < MAX_PAIRCHART_LOOPS:
        loops += 1
        for key, val in pair_chart.items():
            for key2, val2 in val.items():
                # compare state names for compatibility
                compared_states = sorted([key, key2])
                if val2.compatible is None and len(val2.dependent) == 0:
                    dependent = False  # assume not dependent until shown otherwise
                    for i in range(num_inputs):
                        idx = i*2
                        ns1 = st[key][idx]
                        ns2 = st[key2][idx]
                        if ns1 != '-' and ns2 != '-':
                            # if the two states reference different non-blank NS and they are not the two being compared
                            if ns1 != ns2 and (ns1 not in compared_states or ns2 not in compared_states):
                                dependent = True
                                state1 = ns1
                                state2 = ns2
                                if state2 < state1:
                                    state_temp = state1
                                    state1 = state2
                                    state2 = state_temp
                                val2.dependent.append(f'{state1},{state2}')
                    if not dependent:
                        val2.compatible = True
                # compare dependencies for compatibility
                elif val2.compatible is None and len(val2.dependent) > 0:
                    paired_compared_states = f'{compared_states[0]},{compared_states[1]}'
                    compatible = None
                    for dependency in val2.dependent:
                        path_explore = iterative_path(pair_chart, paired_compared_states, dependency, [])
                        if path_explore == COMPATIBLE:
                            if compatible is None:
                                compatible = True
                        elif path_explore == UNRESOLVED:
                            if compatible is True:
                                compatible = UNRESOLVED
                        elif path_explore == INCOMPATIBLE:
                            compatible = False
                    if compatible == COMPATIBLE:
                        val2.compatible = True
                    elif compatible == INCOMPATIBLE:
                        val2.compatible = False

    print_pairchart(pair_chart)
    return pair_chart
