"""Database tools"""
import logging
import os
from datetime import datetime

import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from taxengine.shared.model.models import DescargaPadronesHistory


_logger = logging.getLogger(__name__)


class Database:
    """Database"""

    engine = False
    _connection = False
    _table = ""
    _pg_host = ""
    _pg_port = 5432
    _pg_db = ""
    _pg_user = ""
    _pg_password = ""
    _month = ""
    _year = ""

    def __init__(self, month, year, table):
        """Init"""
        self._pg_host = os.getenv("PG_HOST")
        self._pg_port = os.getenv("PG_PORT")
        self._pg_db = os.getenv("PG_DB")
        self._pg_user = os.getenv("PG_USER")
        self._pg_password = os.getenv("PG_PASSWORD")
        self._table = table
        self._year = year
        self._month = month

        self._connection = psycopg2.connect(
            database=self._pg_db,
            user=self._pg_user,
            password=self._pg_password,
            host=self._pg_host,
            port=self._pg_port,
        )

        url = "postgresql://"
        url += f"{self._pg_user}:{self._pg_password}"
        url += f"@{self._pg_host}:{int(self._pg_port)}"
        url += f"/{self._pg_db}"

        self.engine = create_engine(url)
        self._session = sessionmaker(self.engine)

    def create_partition(self):
        """Create Partition"""

        cursor = self._connection.cursor()
        try:
            _logger.info(
                f"Delete if exists table partition {self._table}_{self._year}{self._month}_part"
            )
            cursor.execute(f"DROP TABLE IF EXISTS {self._table}_{self._year}{self._month}_part;")

            _logger.info(f"Create table partition {self._table}_{self._year}{self._month}_part")

            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self._table}_{self._year}{self._month}_part "
                f"PARTITION OF {self._table} for values in ('{self._year}{self._month}');"
            )

        except Exception as error:
            _logger.error("Partition creation error")
            raise error
        self._connection.commit()
        self._connection.close()
        cursor.close()

    def check_already_imported(self):
        """check_already_imported"""
        with self._session() as session:
            return (
                session.query(DescargaPadronesHistory)
                .filter(DescargaPadronesHistory.padron == self._table)
                .filter(DescargaPadronesHistory.periodo == f"{self._year}{self._month}")
                .count()
                == 0
            )

    def add_history_entry(self):
        """add_history_entry"""
        with self._session() as session:
            new_entry = DescargaPadronesHistory()
            new_entry.fecha = datetime.now()
            new_entry.padron = self._table
            new_entry.periodo = f"{self._year}{self._month}"
            session.add(new_entry)
            session.commit()
