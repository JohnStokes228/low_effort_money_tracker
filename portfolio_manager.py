"""
Portfolio manager class to be called when we need it to lad.
"""
import pandas as pd


class PortfolioManager:

    def __init__(self, portfolio_name):
        self.portfolio_name = portfolio_name
        self.portfolio = pd.read_csv(f'portfolios/{portfolio_name}.csv')

    def add_asset(self):
        pass

    def remove_asset(self):
        pass

    def lookup_asset_value(self):
        pass

    def display_asset_value(self):
        pass
