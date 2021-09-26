"""
Main script for this most low effort of money trackers. Its possible this may become higher effort over time, with
suggestions including:
      - wrap into an app?
      - historic portfolio viewing?
      - create portfolios and test them against time series?
      - a print 'pizza time' method?

TODO: - class design
      - API for getting the values
      - this might literally be it just the two steps
"""
import os
import sys
import pandas as pd
from typing import List
from pathlib import Path


def unpack_list_to_hyphened_string(input_list: List[str]):
    """Unpack list into a string with a new line and tab, followed by a hyphen then a value in the list, for all values
    in the list.

    Example
    -------
    >>> unpack_list_to_hyphened_string(['test', 'test2', 'test3', 'final test'])
        - test1
        - test2
        - test3
        - final test

    Parameters
    ----------
    input_list: List of strings to be unpacked (might also work with lists of other object types?)

    Returns
    -------
    str
        The elements of input_list unpacked and formatted as described.
    """
    return '\n\t - ' + '\n\t - '.join(input_list)


class MainMenu:
    """Class governing the main menu and access to the individual portfolio managers.

    Includes methods for creating, deleting and viewing / editing each portfolio. The latter of these methods will
    instantiate a portfolio manager class for the individual portfolio
    """
    def __init__(self):
        self.portfolios = [Path(file).stem for file in os.listdir('portfolios')]

    def create_portfolio(self):
        """Create a new empty portfolio in the portfolios folder.
        """
        portfolio_name = input('What do you want to call your new portfolio?\n')
        portfolio = pd.DataFrame(columns=[
            'asset_class',
            'asset_name',
            'asset_ticker',
            'price_per_unit',
            'quantity',
            'value',
            'start_date'
        ])

        self.portfolios.append(portfolio_name)
        portfolio.to_csv(f'portfolios/{portfolio_name}.csv', index=False)

    def select_portfolio(self):
        pass

    def delete_portfolio(self):
        """Delete the specified portfolio from the portfolios folder.

        Parameters
        ----------
        """
        print('which portfolio would you like to delete?'
              f'{unpack_list_to_hyphened_string(self.portfolios)}\n')
        chosen = input()

        if chosen not in self.portfolios:
            print('invalid selection!\n')
            return

        self.portfolios.remove(chosen)
        os.remove(f'portfolios/{chosen}.csv')

    def run_menu(self):
        """Run the main menu method
        """
        if not self.portfolios:
            self.create_portfolio()  # force create at least one portfolio if there are none so far

        choose = input("what would you like to do?:"
                       "\n\t1 - create new portfolio"
                       "\n\t2 - view or edit existing portfolio"
                       "\n\t3 - delete existing portfolio"
                       "\n\t4 - exit system\n")

        if choose == '1':
            self.create_portfolio()
        elif choose == '2':
            self.select_portfolio()
        elif choose == '3':
            self.delete_portfolio()
        elif choose == '4':
            sys.exit(0)
        else:
            print('invalid selection!\n')


if __name__ == '__main__':
    menu = MainMenu()

    run_sys = True
    while run_sys:
        menu.run_menu()
