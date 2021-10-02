"""
Support functions to be called elsewhere in the code.
"""
from typing import List, Tuple


def unpack_list_to_hyphened_string(input_list: List[Tuple[str]]) -> str:
    """Unpack list into a string with a new line and tab, followed by a hyphen then a value in the list, for all values
    in the list.

    Example
    -------
    >>> unpack_list_to_hyphened_string([(1, 'test'), (2, 'test2'), (3, 'test3'), (4, 'final test')])
        1 - test1
        2 - test2
        3 - test3
        4 - final test

    Parameters
    ----------
    input_list : List of strings to be unpacked (might also work with lists of other object types?)

    Returns
    -------
    str
        The elements of input_list unpacked and formatted as described.
    """
    output_list = [f'\n\t{input[0]} - {input[1]}' for input in input_list]

    return ''.join(output_list)
