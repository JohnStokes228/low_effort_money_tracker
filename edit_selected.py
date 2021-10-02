"""
Code for editing a given portfolio? maybe? how does this fit together? so dumb John! didnt think this through at all!
"""
from mysql_database import MYSQLDataBase
from menu import Menu


class EditSelected(Menu):
    """Class to manipulate a given portfolio's assets. Not 100% sold on this implementation at the moment tbh but we'll
    go with it for now and see if theres not a better way in a bit...
    """
    def __init__(
        self,
        portfolio: int,
        database_manager: MYSQLDataBase,
    ):
        super().__init__()
        self.database_manager = database_manager
        self._portfolio = portfolio

    @property
    def portfolio(self) -> int:
        """Getter method for attribute '_portfolio'.
        """
        return self._portfolio

    def portfolio_menu(self):
        """Make a decision about what to do to your poor portfolio.
        """
        options = [('add new holdings from file', self.add_assets_from_file),
                   ('add new holdings by hand', self.user_input_add_assets),
                   ('remove assets from portfolio', self.remove_assets)]
        self.run_menu(options=options,
                      message=f'Now editing portfolio with ID {self.portfolio}',
                      check_portfolios=False)

    def add_assets_from_file(self):
        pass

    def user_input_add_assets(self):
        pass

    def remove_assets(self):
        pass
