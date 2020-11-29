# common functions

def remove_duplicates(input_list):
    """
    removes duplicates from a list
    :param input_list: list
    :return: list
    """

    output_list = []
    for element in input_list:
        if element not in output_list:
            output_list.append(element)
    return output_list
