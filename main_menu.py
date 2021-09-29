"""
Main script for this most low effort of money trackers. Its possible this may become higher effort over time, with
suggestions including:
      - wrap into an app?
      - historic portfolio viewing?
      - create portfolios and test them against time series?
      - a print 'pizza time' method?
      - asset allocation for the portfolios?

TODO: - add the delete protfolio method
      - add the view / edit portfolio method
"""
import sys
from typing import List, Optional, Tuple
from mysql_database import MYSQLDataBase


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


class MainMenu:
    """Class governing the User interactions and inputs with the database.
    """
    def __init__(self):
        self.database_manager = MYSQLDataBase()
        self._portfolio = None

    @property
    def portfolio(self) -> Optional[str]:
        """Getter method for sometimes available attribute 'portfolio'.
        """
        if not self._portfolio:
            raise AttributeError('No portfolio currently active!')
        return self._portfolio

    def run_menu(self) -> None:
        """Run the main menu method.
        """
        self.database_manager.get_connect_database()
        portfolio_count = self.database_manager.execute_fetch(query='SELECT * FROM portfolios')

        if not portfolio_count:
            print('Welcome to this somewhat shite portfolio tracker!')
            self.create_portfolio()  # force create at least one portfolio if there are none so far

        choose = input("what would you like to do?:"
                       "\n\t1 - create new portfolio"
                       "\n\t2 - view or edit existing portfolio"
                       "\n\t3 - delete existing portfolio"
                       "\n\t4 - exit system\n")

        if choose == '1':  # this if block is quite clunky, is there a more scalable way - prehaps enumerate related?
            self.create_portfolio()
        elif choose == '2':
            self.select_portfolio()
        elif choose == '3':
            self.delete_portfolio()
        elif choose == '4':
            self.database_manager.close()
            sys.exit(0)
        else:
            print('invalid selection!\n')

    def create_portfolio(self) -> None:
        """Create a portfolio in the portfolios table.
        """
        portfolio_name = input('What do you want to call your new portfolio?\n')
        portfolio_description = input('Write a short description for your portfolio, or hit enter to skip\n')

        query = f"""
        INSERT INTO portfolios (id, name, description) VALUES (NULL, '{portfolio_name}', '{portfolio_description}')
        """
        self.database_manager.execute_commit(query=query)

    def select_portfolio(self) -> None:
        pass

    def delete_portfolio(self) -> None:
        """Delete the specified portfolio from the portfolios folder.
        """
        portfolios = self.database_manager.execute_fetch(query='SELECT DISTINCT id, name from portfolios')

        print('Type the number of portfolio you\'d like to delete!'
              f'{unpack_list_to_hyphened_string(portfolios)}\n')  # list all portfolios currently available
        chosen = input()

        if chosen not in [str(portfolio[0]) for portfolio in portfolios]:
            print('invalid selection!\n')
            return  # leave function if user attempts to remove a non-existant portfolio

        self.database_manager.execute_commit(query=f'DELETE FROM portfolios WHERE id = {chosen}')
        print(f'Successfully deleted portfolio {chosen}')


if __name__ == '__main__':
    menu = MainMenu()

    run_sys = True
    while run_sys:
        menu.run_menu()
