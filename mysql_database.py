"""
All core database interactivity functions come from here, or at least I'd have thought they would. whos to say at the
end of the day
"""
import yaml
from typing import NoReturn
from mysql.connector import connect
from config.create_tables_sql import(
    portfolios,
    assets,
    prices,
)


with open('config/mysql_user_config.yaml') as f:
    MYSQL_USER = yaml.safe_load(f)
SQL_TABLES = [portfolios, assets, prices]

class MYSQLDataBase:
    """Class which handles all MYSQL interactivity for the project. Not too sure how good of an idea this is but we'll
    see how it goes. worst it can do is fail miserably.
    """
    def __init__(self):
        self._connection = connect(
                host=MYSQL_USER['host'],
                user=MYSQL_USER['user'],
                password=MYSQL_USER['password'],
            )
        self._cursor = self._connection.cursor()

    @property
    def connection(self):
        return self._connection
    
    @property
    def cursor(self):
        return self._cursor

    @connection.setter
    def connection(
        self, 
        database_name: str,
    ):
        """Update the connection and subsequently cursor attributes based on database name.

        Parameters
        ----------
        database_name : Name of dtaabase to connect to.
        """
        self._connection = connect(
            host=MYSQL_USER['host'],
            user=MYSQL_USER['user'],
            password=MYSQL_USER['password'],
            database=database_name
        )
        self._cursor = self._connection.cursor()

    def get_connect_database(
        self,
        database_name: str='portfolio_database'
    ) -> NoReturn:
        """Either connects to the database with name database_name e if it exists, or creates it from scratch if not.
        Updates self.connection and self.cursor to connect to database_name either way.

        Parameters
        ----------
        database_name : Name of database to create if needed and connect to once it exists.
        """
        self.cursor.execute('SHOW DATABASES')
        databases = [db[0] for db in self.cursor]

        if database_name in databases:
            self.connection = database_name
            print(f'Connected to the database "{database_name}"')
            return
        
        self.cursor.execute(f'CREATE DATABASE {database_name}')
        self.connection = database_name
        map(self.execute_query, SQL_TABLES)  # create the required tables in the database
        print(f'Set up the database "{database_name}", and connected to it.')

    def execute_query(
        self,
        query: str,
    ) -> NoReturn:
        """Create a table from an SQL query.

        Parameters
        ----------
        query : String containing SQL query to be run by the cursor.
        """
        self.cursor.execute(query)
        self.connection.commit()


#test = MYSQLDataBase()
#test.create_connect_database()