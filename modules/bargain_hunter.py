# bargain hunter's algorithm
from itertools import combinations

from .common import remove_duplicates


def pc_is_covered(pc1, pc2):
    """
    Function returns True if PC2 covers PC1
    :param pc1: list
    :param pc2: list
    :return: boolean
    """
    pc1_set = set(state for state in pc1.split(','))
    pc2_set = set(state for state in pc2.split(','))

    # smaller sets can't cover
    if len(pc2_set) <= len(pc1_set):
        return False

    # intersection is same as original set
    if pc1_set == pc2_set.intersection(pc1_set):
        return True

    return False


def cs_is_covered(cs1, cs2):
    """
    Function returns True if each set in CS2 is contained in some set in CS1
    :param cs1: set
    :param cs2: set
    :return: boolean
    """
    cs1_list = []
    for cs in cs1:
        cs1_list.append(set(cs))
    cs2_list = []
    for cs in cs2:
        cs2_list.append(set(cs))

    cs2_contained_by_cs1 = True
    for class_set2 in cs2_list:
        for class_set1 in cs1_list:
            if class_set2 != class_set1.intersection(class_set2):
                cs2_contained_by_cs1 = False

    return cs2_contained_by_cs1


def print_pc_table(pc_table):
    """ formatted output string for a prime compatibility table """

    print('PC: Class Set')
    for key, val in pc_table.items():
        print(f'{key}: {val}')


def bargain(state_table, mccs, num_inputs):
    """
    Function which creates a Prime Compatibility table from a given state table and MCCs
    :param state_table: dictionary
    :param mccs: list
    :param num_inputs: int
    :return: dictionary
    """
    pc_table = {}  # prime compatibles tables

    print('\nDetermining prime compatibles...')

    # create pre-PC table
    for mcc in mccs:
        mcc_len = len(mcc)
        for combo_len in range(mcc_len, 0, -1):
            comb = list(combinations(mcc, combo_len))
            for pc in comb:
                pc_list = list(pc)
                pc_string = ','
                pc_string = pc_string.join(list(pc))

                class_set = []
                for i in range(0, num_inputs):
                    idx = i*2
                    ns_set = []
                    for pc_state in pc_list:
                        ns = state_table[pc_state][idx]
                        if ns != '-':
                            ns_set.append(ns)
                    ns_set = remove_duplicates(ns_set)
                    if len(ns_set) > 1:
                        set_is_all_part_of_pc = True
                        # check if the set is comprised only of states in the PC
                        for state in ns_set:
                            if state not in pc_list:
                                set_is_all_part_of_pc = False
                        if not set_is_all_part_of_pc:
                            class_set.append(sorted(ns_set))

                class_set = remove_duplicates(class_set)
                pc_table[pc_string] = class_set

    # create final PC table by searching for bargains
    pc_reduced_table = {}
    for pc, cs in pc_table.items():
        pc_and_cs_is_covered = False
        for pc2, cs2 in pc_table.items():
            # skip comparison to self
            if pc == pc2:
                continue
            # if pc is covered by pc2; a) S contains S’
            if pc_is_covered(pc, pc2):
                # if the class set is more of a bargain; b) each Cj is contained in some C’j’
                if len(cs2) == 0:
                    pc_and_cs_is_covered = True
                else:
                    if len(cs) >= len(cs2):
                        if cs_is_covered(cs, cs2):
                            pc_and_cs_is_covered = True

        if not pc_and_cs_is_covered:
            pc_reduced_table[pc] = cs

    print_pc_table(pc_reduced_table)
    return pc_reduced_table
