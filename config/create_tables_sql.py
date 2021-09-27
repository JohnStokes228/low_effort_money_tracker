portfolios = """
CREATE TABLE portfolios (
    id INT AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL,
    description VARCHAR(100),
    PRIMARY KEY (id)
)
"""

assets = """
CREATE TABLE assets (
    portfolio_id INT NOT NULL,
    asset_type VARCHAR() NOT NULL,
    location VARCHAR(50) NOT NULL,
    asset_name VARCHAR(100),
    ticker VARCHAR(12),
    units INT NOT NULL,
    date_purchased DATE NOT NULL,
    dividends DECIMAL(4, 3),
    FOREIGN KEY portfolio_id REFERENCES portfolios(id),
    PRIMARY KEY (ticker),
    CONSTRAINT 'asset_type_exists' CHECK (asset_type in ('Bank acct.', 'Fund', 'S&S', 'Crypto', 'ETF', 'Other'))
)
"""

prices = """
CREATE TABLE prices (
    date DATE NOT NULL,
    ticker VARCHAR(12) NOT NULL,
    price DECIMAL(10, 2),
    FOREIGN KEY ticker REFERENCES assets(ticker)
)
"""
