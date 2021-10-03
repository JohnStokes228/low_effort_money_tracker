"""
Code for editing a given portfolio? maybe? how does this fit together? so dumb John! didnt think this through at all!
"""
import pandas as pd
from support_funcs import choose_file_from_directory
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
        options = (('add new holdings from file', self.add_assets_from_file),
                   ('add new holdings by hand', self.add_assets_by_input),
                   ('remove assets from portfolio', self.remove_assets))
        self.run_menu(options=options,
                      message=f'Now editing portfolio with ID {self.portfolio}',
                      check_portfolios=False)

    def add_assets_from_file(self) -> None:
        """Choose an asset file to add to the portfolio defined by self.portfolio, then input the reqired rows.
        """
        files = choose_file_from_directory(directory='assets')

        if not files:
            return

        for file in files:
            df = pd.read_csv(file)
            df = self.apply_assets_held_schema(df)

            if df is None:
                print(f'Invaid file structure in {file}, could not append contents to database!')
                break

            df.to_sql(name='assets_held', con=self.database_manager.engine, if_exists='append', index=False)
            print(f'Successfully added the assets from {file} into portfolio {self.portfolio}!')

    def apply_assets_held_schema(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Apply the required schema to some pandas data so that it will succesfully get added to the assets_held table.

        Parameters
        ----------
        df : DataFrame containing a list of purchases.

        Returns
        -------
        pd.DataFrame
            DataFrame with only valid rows / columns remaining.
        """
        df['portfolio_id'] = self.portfolio

        if not set(['location', 'units', 'date_purchased']).issubset(df.columns):
            return

        if not 'ticker' in df.columns:
            df['ticker'] = None

        df = df[['portfolio_id', 'location', 'ticker', 'units', 'date_purchased']]

        df.loc[:, 'date_purchased'] = pd.to_datetime(df['date_purchased'], format='%d/%m/%Y')  # big assumption here?
        df.dropna(subset=['location', 'units', 'date_purchased'], inplace=True)

        return df

    def add_assets_by_input(self):
        pass

    def remove_assets(self):
        pass
