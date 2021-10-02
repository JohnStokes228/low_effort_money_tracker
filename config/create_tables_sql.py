portfolios = """
CREATE TABLE `portfolios` (
    `id` INT AUTO_INCREMENT,
    `name` VARCHAR(30) NOT NULL,
    `description` VARCHAR(100),
    PRIMARY KEY (`id`)
)
"""

asset_info = """
CREATE TABLE `asset_info` (
    `ticker` VARCHAR(12),
    `asset_name` VARCHAR(100),
    `asset_type` VARCHAR(10) NOT NULL CHECK (`asset_type` in ('Bank acct.', 'Fund', 'S&S', 'Crypto', 'ETF', 'Other')),
    `dividends` DECIMAL(4, 3),
    PRIMARY KEY (`ticker`)
)
"""

assets_held = """
CREATE TABLE `assets_held` (
    `portfolio_id` INT NOT NULL,
    `location` VARCHAR(50) NOT NULL,
    `ticker` VARCHAR(12),
    `units` DECIMAL(13, 6) NOT NULL,
    `date_purchased` DATE NOT NULL,
    FOREIGN KEY (`portfolio_id`) REFERENCES portfolios(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`ticker`) REFERENCES asset_info(`ticker`) ON DELETE CASCADE
)
"""

prices = """
CREATE TABLE `prices` (
    `date` DATE NOT NULL,
    `ticker` VARCHAR(12) NOT NULL,
    `price` DECIMAL(10, 2),
    FOREIGN KEY (`ticker`) REFERENCES asset_info(`ticker`) ON DELETE CASCADE
)
"""
