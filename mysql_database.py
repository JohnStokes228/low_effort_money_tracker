"""
All core database interactivity functions come from here, or at least I'd have thought they would. whos to say at the
end of the day. The class deffo works up till here though we've got ourselves a database bois :O
"""
import pymysql
import yaml
import sys
from sqlalchemy import create_engine  # think we should swap fully to this?
from typing import Any, List, Tuple
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
SQL_TABLES = [portfolios, assets_held, asset_info, prices]

class MYSQLDataBase:
    """Class which handles all MYSQL interactivity for the project.
    
    Based on a recommendation found elsewhere includes methods to do most basic SQL things on its own, including getters
    for the core attributes. Used to also contain a setter but removed it as I realised I didnt really have any use for
    it lol.
    """
    def __init__(
        self,
        database_name: str='portfolio_database'
    ):
        self._database_name = database_name
        self._connection = connect(
                host=MYSQL_USER['host'],
                user=MYSQL_USER['user'],
                password=MYSQL_USER['password'],
        )
        self._cursor = self._connection.cursor(buffered=True)
        self._engine = None  # do we need the other two if we have an engine? need to learn how this works

    @property
    def database_name(self):
        """Get class database_name attribute.
        """
        return self._database_name

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

    @property
    def engine(self):
        """Get class engine attribute.
        """
        return self._engine

    @engine.setter
    def engine(
        self,
        database_name: str,
    ) -> None:
        """Set class engine attribute.

        Parameters
        ----------
        database_name : Name of database to get engine connection to.
        """
        self._engine = create_engine(
            f'mysql+pymysql://{MYSQL_USER["user"]}:{MYSQL_USER["password"]}'
            f'@{MYSQL_USER["host"]}:{MYSQL_USER["port"]}/{database_name}',
            echo=False
        )

    def get_connect_database(
        self,
    ) -> None:
        """Either connects to the database with name database_name if it exists, or creates it from scratch if not.
        """
        databases = [database[0] for database in self.execute_fetch('SHOW DATABASES')]

        if self.database_name in databases:
            self.connect_to_database()
            return

        self.execute(f'CREATE DATABASE {self.database_name}')
        self.connect_to_database()
        deque(map(self.execute, SQL_TABLES))  # deque() force executes the mapped function calls
        print(f'Set up tables for the database "{self.database_name}".')

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

    def connect_to_database(self) -> None:
        """Connect to a given database, establish an engine for the class?
        """
        self.execute(f'USE {self.database_name}')
        self.engine = self.database_name

        print(f'Connected to the database "{self.database_name}"')

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

    def close(
        self,
        commit: bool=True,
        exit: bool=True,
    ) -> None:
        """Close connection to MYSQL database, commiting changes if requested.

        Parameters
        ----------
        commit : Set to True to commit any remaining queries before closing connection.
        exit : Set to True to exit the thread after closing the connection.
        """
        if commit:
            self.commit()

        self.connection.close()

        if exit:
            sys.exit(0)

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
