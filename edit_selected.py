"""
Code for editing a given portfolio? maybe? how does this fit together? so dumb John! didnt think this through at all!
"""
import pandas as pd
from datetime import datetime
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
                   ('add or remove individual assets by hand', self.edit_assets_by_input))
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
            self.append_df_to_assets_held_table(df=df, location=file)

    def edit_assets_by_input(self) -> None:
        """Add or remove assets based off user input.

        Notes
        -----
        probs be mad tedious but could be worse ey ;).
        """
        choices = dict()

        choices['ticker'] = input('Whats the assets ticker? (maximum 12 characters, hit enter if adding liquid)')

        try:
            choices['units'] = float(
                input(f'How many units of asset {choices["ticker"]} would you like to add or remove?')
            )
        except ValueError:
            print('Invalid quantity input!')
            return

        choices['location'] = input(f'Where are you storing {choices["units"]} units of {choices["ticker"]}?')

        choices['date_purchased'] = input(f'When did this transaction occur? (dd/mm/yyyy, hit enter for "today")')
        if not choices['date_purchased']:
            choices['date_purchased'] = datetime.today().strftime('%d/%m/%Y')

        df = pd.DataFrame([choices], columns=choices.keys())
        self.append_df_to_assets_held_table(df=df, location='user input')

    def append_df_to_assets_held_table(
        self,
        df: pd.DataFrame,
        location: str,
    ) -> None:
        """Update the assets_held table with the data stored in df.

        Parameters
        ----------
        df : dataframe with 'portfolio_id', 'ticker', 'units', 'location' and 'date_purchased' columns.
        location : where did this add request come from lad?
        """
        df = self.apply_assets_held_schema(df)

        if df is None:
            print(f'Invaid file structure in {location}, could not append contents to database!')
            return

        df.to_sql(name='assets_held', con=self.database_manager.engine, if_exists='append', index=False)
        print(f'Successfully added the assets from {location} into portfolio {self.portfolio}!')

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

        try:
            df.loc[:, 'date_purchased'] = pd.to_datetime(df['date_purchased'], format='%d/%m/%Y')  # big assumption here?
        except ValueError:
            print('Invalid date format, please use dd/mm/yyyy and try again!')
            return

        df.dropna(subset=['location', 'units', 'date_purchased'], inplace=True)

        return df
