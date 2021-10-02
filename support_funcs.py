"""
Support functions to be called elsewhere in the code.
"""
import os
from pathlib import Path
from typing import List, Tuple, Any, Optional


def choose_file_from_directory(directory: str) -> Optional[str]:
    """Choose file in directory to get, or fail miserably. There is no try.

    Parameters
    ----------
    directory : Folder path to search for files in.

    Returns
    -------
    Optional[str]
        Either the file path of the desired file, or None
    """
    asset_files = [Path(file) for file in os.listdir(directory)]

    if not asset_files:
        print('No files to select from!')
        return

    chosen = input('Select a file to add to your portfolio!'
                   f'{unpack_list_to_hyphened_string(list(enumerate(asset_files)))}')

    file = get_element_by_string_index(input_string=chosen, input_list=asset_files)

    if not file:
        print('Invalid selection!')
        return

    return f'{directory}/{file}.csv'


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


def get_element_by_string_index(
    input_string: str,
    input_list: List[Any],
    ) -> Optional[Any]:
    """Attempt to get the element in input_list located at index int(input_string), unless such an act is impossible.

    Parameters
    ----------
    input_string : String to represent list index desired.
    input_list : List to get element from.
    Returns
    -------
    Optional[Any]
        Either the element at index int(input_string), or None.
    """
    try:
        index = int(input_string)
        desired_element = input_list[index]

        return desired_element
    except (IndexError, ValueError):
        return
