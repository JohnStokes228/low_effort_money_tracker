"""
Price API interactivity for the bloody system mate. will allow you to get the price timeseries via some kind of API for
all your assets - except the bank ones i guess?

pdr.DataReader('LTC-USD', 'yahoo', start_date, end_date)  <- pulls the price of ltc-usd pair
"""
#import pandas_datareader as pdr
import pandas as pd
from typing import List, Tuple
from datetime import datetime
from mysql_database import MYSQLDataBase


class PricesAPI:
    """Class for interacting with the API for getting asset prices.

    This will likely need to be a thing which happens whenever you want to view the portfolios? should it always run or
    sometimes ignore it?
    """
    def __init__(
        self,
        database_manager: MYSQLDataBase,
    ):
        self.database_manager = database_manager
        self.end_date = datetime.today()

    def update_asset_historic_prices(self):
        query = f"""
        SELECT ticker, MIN(date_purchased)
        FROM assets_held
        GROUP BY ticker
        """
        asset_startdates = self.database_manager.execute_fetch(query)
        missing_dates = self.check_asset_timeseries(asset_startdates=asset_startdates)

        asset_prices = [self.get_price_from_api(asset=asset) for asset in missing_dates]
        df = pd.concat(asset_prices)

        df.to_sql(name='prices', con=self.database_manager.engine, if_exists='append', index=False)
        self.remove_unheld_assets()

    def check_asset_timeseries(
        self,
        asset_startdates: Tuple[str, datetime.datetime],
    ) -> List[datetime.datetime]:
        """This one will look for what of the time series is covered by the existing data. 
        is it better to make n queries or to make one query then iterate through the results...?
        """
        query = """
        SELECT ticker, MIN(date)
        FROM prices
        GROUP BY ticker
        """
        existing_timeseries = self.database_manager.execute_fetch(query=query)
        new_timeseries = []
        # get the asset, min date pairs which arent in prices but are in holdings
        # if the asset exists with a different min date then check which the earliest is and take that
        # return list of asset / min date combos including entirely issing assets and assets with new min dates.

        return new_timeseries

    def get_price_from_api(
        self,
        asset: str,
    ) -> pd.DataFrame:
        """Probably what it'll be is it'll look for the price of the asset via the missing dates
        """
        pass

    def remove_unheld_assets(self) -> None:
        """Remove price data for assets that are no longer held by any portfolio, to clear up memory.
        """
        query1 = "SELECT UNIQUE(ticker) FROM assets_held"
        assets_held = self.database_manager.execute_fetch(query=query1)

        query2 = "SELECT UNIQUE(ticker) FROM prices"
        prices_held = self.database_manager.execute_fetch(query=query2)

        tickers_to_drop = tuple(ticker for ticker in prices_held if ticker not in assets_held)
        query3 = f"DELETE FROM prices WHERE ticker IN {tickers_to_drop}"
        self.database_manager.execute_commit(query=query3)
