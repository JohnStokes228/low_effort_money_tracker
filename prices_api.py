"""
Price API interactivity for the bloody system mate. will allow you to get the price timeseries via some kind of API for
all your assets - except the bank ones i guess?

TODO: - test lol
      - build edge case of some sort for money stored out the market?
      - build edge case for niche shitcoins if we intend to continue our degenerate lifestyle into the future?
"""
import pandas_datareader as pdr
import pandas as pd
from typing import List, Tuple, Optional
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
        query = """
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
            List of asset tickers, start and end dates for assets which we need new price data for.
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
    ) -> Optional[pd.DataFrame]:
        """Call aset value in GBP terms from yahoo finance.

        Notes
        -----
        No idea how well this will work for shitcoins or low caps. Also have to imagine some tickers may overlap? we'll
        see how it goes - im sure for a rudimentary project like this one itll do seriously doubt its viability for
        professional purposes...

        Parameters
        ----------
        asset : List of asset tickers, start and end dates for assets which we need new price data for.

        Returns
        -------
        pd.DataFrame
            Probably a dataframe of name, ticker, prices, etc... tbh its all up in the air
        """
        try:
            asset_df = pdr.DataReader(f'{asset[0]}-USD', 'yahoo', asset[1], asset[2])
        except pdr._utils.RemoteDataError:
            asset_df = pdr.DataReader(asset[0], 'yahoo', asset[1], asset[2])
        finally:
            if asset_df.shape[0] == 0:
                return  # if not such pairing exists cancel the rest I guess...?

            asset_df.reset_index(inplace=True)

            asset_df['price'] = asset_df[['High', 'Low']].mean(axis=1).round(decimals=2)
            asset_df['ticker'] = asset[0]
            asset_df.rename(columns={'Date': 'date'}, inplace=True)
            asset_df = asset_df[['ticker', 'price', 'date']]

            return asset_df

    def remove_unheld_assets(self) -> None:
        """Remove price data for assets that are no longer held by any portfolio, to clear up memory.
        """
        query1 = "SELECT DISTINCT(ticker) FROM assets_held"
        assets_held = self.database_manager.execute_fetch(query=query1)

        query2 = "SELECT DISTINCT(ticker) FROM prices"
        prices_held = self.database_manager.execute_fetch(query=query2)

        tickers_to_drop = tuple(ticker for ticker in prices_held if ticker not in assets_held)
        query3 = f"DELETE FROM prices WHERE ticker IN {tickers_to_drop}"
        self.database_manager.execute_commit(query=query3)
