"""
Main script for this most low effort of money trackers. Its possible this may become higher effort over time, with
suggestions including:
      - wrap into an app?
      - historic portfolio viewing?
      - a print 'pizza time' method?
      - asset allocation for the portfolios?

TODO: - decide what to do about the edit portfolio method
      - maybe the 'view' portfolio method should be its own thing like as a dashboard or something?
"""
from typing import List, Tuple
from mysql_database import MYSQLDataBase, MYSQL_USER
from edit_selected import EditSelected
from menu import Menu
from support_funcs import unpack_list_to_hyphened_string


class PortfolioMenu(Menu):
    """Class governing the User interactions and inputs with the database.
    """
    def __init__(self):
        super().__init__()
        self.database_manager = MYSQLDataBase()

    @property
    def portfolios(self) -> List[Tuple[int, str]]:
        """Query the database and get the list of portfolios, accessible as a class attr.
        """
        return self.database_manager.execute_fetch(query='SELECT DISTINCT id, name from portfolios')

    def main(self) -> None:
        """Setup and run the system.
        """
        options = [('create new portfolio', self.create_portfolio),
                   ('edit an existing portfolio', self.edit_portfolio),
                   ('delete existing portfolio', self.delete_portfolio),
                   ('exit system', self.database_manager.close)]

        self.database_manager.get_connect_database()
        self.run_menu(message=f'Hello there {MYSQL_USER["user"]}!',
                      options=options,
                      check_portfolios=True)

    def check_for_portfolios(self) -> None:
        """Check the database to ensure theres at least one portfolio saved, else force the creation of a new one.
        """
        portfolio_count = self.database_manager.execute_fetch(query='SELECT * FROM portfolios')

        if not portfolio_count:
            print('Welcome to this somewhat shite portfolio tracker!')
            self.create_portfolio()

    def create_portfolio(self) -> None:
        """Create a portfolio in the portfolios table.
        """
        portfolio_name = input('What do you want to call your new portfolio?\n')
        portfolio_description = input('Write a short description for your portfolio, or hit enter to skip\n')

        query = f"""
        INSERT INTO portfolios (id, name, description) VALUES (NULL, '{portfolio_name}', '{portfolio_description}')
        """
        self.database_manager.execute_commit(query=query)

    def edit_portfolio(self) -> None:
        """Select a portfolio from the 'portfolios' table and then enter the edit menu for that portfolio.
        """
        chosen = input('Which portfolio would you like to view or edit?'
                       f'{unpack_list_to_hyphened_string(self.portfolios)}\n')

        if chosen not in [str(folio[0]) for folio in self.portfolios]:
            print('Invalid selection made!')
            return

        chosen_portfolio = EditSelected(portfolio=int(chosen), database_manager=self.database_manager)
        chosen_portfolio.portfolio_menu()

    def delete_portfolio(self) -> None:
        """Delete the specified portfolio from the portfolios folder.
        """
        print('Type the number of portfolio you\'d like to delete!'
              f'{unpack_list_to_hyphened_string(self.portfolios)}\n')
        chosen = input()

        if chosen not in [str(portfolio[0]) for portfolio in self.portfolios]:
            print('invalid selection!\n')
            return

        self.database_manager.execute_commit(query=f'DELETE FROM portfolios WHERE id = {chosen}')
        print(f'Successfully deleted portfolio {chosen}')


if __name__ == '__main__':
    menu = PortfolioMenu()
    menu.main()
