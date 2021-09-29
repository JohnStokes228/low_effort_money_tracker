"""
All core database interactivity functions come from here, or at least I'd have thought they would. whos to say at the
end of the day. The class deffo works up till here though we've got ourselves a database bois :O
"""
from typing import Any, List, Tuple
import yaml
from mysql.connector import connect
from collections import deque
from config.create_tables_sql import(
    portfolios,
    assets_held,
    asset_info,
    prices,
)


with open('config/mysql_user_config.yaml') as f:
    MYSQL_USER = yaml.safe_load(f)
SQL_TABLES = [portfolios, asset_info, assets_held, prices]

class MYSQLDataBase:
    """Class which handles all MYSQL interactivity for the project.
    
    Based on a recommendation found elsewhere includes methods to do most basic SQL things on its own, including getters
    for the core attributes. Used to also contain a setter but removed it as I realised I didnt really have any use for
    it lol.
    """
    def __init__(self):
        self._connection = connect(
                host=MYSQL_USER['host'],
                user=MYSQL_USER['user'],
                password=MYSQL_USER['password'],
        )
        self._cursor = self._connection.cursor(buffered=True)

    @property
    def connection(self):
        """Get class connection attribute.
        """
        return self._connection
    
    @property
    def cursor(self):
        """Get class cursor attribute.
        """
        return self._cursor

    def get_connect_database(
        self,
        database_name: str='portfolio_database'
    ) -> None:
        """Either connects to the database with name database_name if it exists, or creates it from scratch if not.

        Parameters
        ----------
        database_name : Name of database to create if needed and connect to once it exists.
        """
        self.execute('SHOW DATABASES')
        databases = [db[0] for db in self.cursor]

        if database_name in databases:
            self.execute(f'USE {database_name}')
            print(f'Connected to the database "{database_name}"')
            return
        
        self.execute(f'CREATE DATABASE {database_name}')
        self.execute(f'USE {database_name}')
        deque(map(self.execute, SQL_TABLES))  # deque() force executes the mapped function calls
        print(f'Set up the database "{database_name}", and connected to it.')

    def close(
        self,
        commit: bool=True,
    ) -> None:
        """Close connection to MYSQL database, commiting changes if requested.

        Parameters
        ----------
        commit : Set to True to commit any remaining queries before closing connection.
        """
        if commit:
            self.commit()
        self.connection.close()

    def execute_commit(
        self,
        query: str,
    ) -> None:
        """Execute and commit a given query in the connected database.

        Parameters
        ----------
        query : String representation of desired query.
        """
        self.execute(query=query)
        self.commit()

    def execute_fetch(
        self,
        query: str,
    ) -> List[Tuple[Any]]:
        """Execute a query, then fetch the response.

        Parameters
        ----------
        query : String representation of the SQL query.

        Returns
        -------
        List[Tuple[Any]]
            List of tuples, containing results of the query. 
        """
        self.execute(query)
        output = self.cursor.fetchall()

        return output

    def execute(
        self,
        query: str,
    ) -> None:
        """Execute SQL query using cursor.

        Parameters
        ----------
        query : String representation of desired query.
        """
        self.cursor.execute(query)

    def commit(self) -> None:
        """Commit query to database.
        """
        self.connection.commit()
