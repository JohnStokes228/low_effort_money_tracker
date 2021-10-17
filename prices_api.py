"""
Price API interactivity for the bloody system mate. will allow you to get the price timeseries via some kind of API for
all your assets - except the bank ones i guess?

pdr.DataReader('LTC-USD', 'yahoo', start_date, end_date)  <- pulls the price of ltc-usd pair

if you always need todays data at least maybe theres something to be done here with regards to today vs previous max?
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
        self.end_date = datetime.today().date()

    def update_asset_historic_prices(self):
        """Updates the prices table based on what assets are currently held and for how long.
        """
        query = f"""
        SELECT ticker, MIN(date_purchased)
        FROM assets_held
        GROUP BY ticker
        """
        asset_startdates = self.database_manager.execute_fetch(query)
        asset_startdates = [(*asset, self.end_date) for asset in asset_startdates]  # append date today to each result

        missing_dates = self.check_asset_timeseries(asset_startdates=asset_startdates)
        asset_prices = [self.get_price_from_api(asset=asset) for asset in missing_dates]

        if not asset_prices:
            return

        df = pd.concat(asset_prices)
        df.to_sql(name='prices', con=self.database_manager.engine, if_exists='append', index=False)
        self.remove_unheld_assets()

    def check_asset_timeseries(
        self,
        asset_startdates: List[Tuple[str, datetime, datetime]],
    ) -> List[Tuple[str, datetime, datetime]]:
        """Find the ticker names, and start and end dates of periods of missing price data in the 'prices' table.

        Parameters
        ----------
        asset_startdates : Results of a query to the assets_held table containing each ticker and the date it was first
        held by any protfolios in the portfolios table.

        Returns
        -------
        List[Tuple[str, datetime.datetime, datetime.datetime]]
            List of asset tickers, satrt and end dates for assets which we need new price data for.
        """
        query = """
        SELECT ticker, MIN(date), MAX(date)
        FROM prices
        GROUP BY ticker
        """
        existing_timeseries = self.database_manager.execute_fetch(query=query)  # prices table
        new_timeseries = [asset for asset in asset_startdates if asset not in existing_timeseries]  # ignore unchanged

        new_assets = [asset for asset in asset_startdates if asset[0] in [asset for asset, *_ in new_timeseries]]
        updated_assets = [asset for asset in asset_startdates if asset not in new_assets]

        if updated_assets:
            for asset in updated_assets:
                og_asset = next((i for i, v in enumerate(existing_timeseries) if v[0] == asset[0]), None)
                og_asset = existing_timeseries[og_asset]  # get the existing data for the ticker which has been updated

                if og_asset[1] > asset[1]:  # if we have a new start date
                    new_assets.append((asset[0], asset[1], og_asset[1]))

                if og_asset[2] < asset[2]:  # if we have a new end date
                    new_assets.append((asset[0], og_asset[2], asset[2]))

        return new_assets

    def get_price_from_api(
        self,
        asset: List[Tuple[str, datetime, datetime]],
    ) -> pd.DataFrame:
        """Probably what it'll be is it'll look for the price of the asset via the missing dates.
        Do I need to have some method of addressing the difference between crypto assets, S&S, funds, bonds, etc...?
        I'll need to play with the api and see i think. This could require a bunch of edge cases. It may also require
        the user to sepcify the type of asset in the assets held database which would be somewhat annoying...
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
