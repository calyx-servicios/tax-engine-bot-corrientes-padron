"""Bot Tools"""
import logging
from datetime import datetime
import os
from pathlib import Path

from database import Database
from dateutil.relativedelta import relativedelta
from decouple import config
from pandas_job import PandasJob
from selenium_job import SeleniumJob

_logger = logging.getLogger(__name__)


class Bot:
    """Bot"""

    _month = False
    _year = False
    _download_directory = "/mnt/downloads/"

    # Database
    _database = False
    # Pandas
    _pandas_job = False
    # Selenium
    _selenium_job = False

    # Dependency

    def __init__(self):
        """Init"""
        _logger.info("====Starting Bot===")

        self._table_name = os.getenv("TABLE_NAME")

        # Retro is used to fake the current month backwards
        retro = config("RETRO") or 0
        _logger.debug(f"Retro:{retro}")
        today = datetime.today() - relativedelta(months=int(retro))

        self._month = today.strftime("%m")
        self._year = today.strftime("%Y")

        _logger.info(f"Período a descargar: {self._year}{self._month}")

        self._database = Database(self._month, self._year, table=self._table_name)
        self._pandas_job = PandasJob(self._month, self._year, table=self._table_name)
        self._selenium_job = SeleniumJob(
            month=self._month,
            year=self._year,
            download_directory=self._download_directory,
            table=self._table_name,
        )

    def job(self):
        """Job"""

        if self._database.check_already_imported():

            filename = self._selenium_job.download_from_source()

            if filename is not None or len(filename) > 0:
                filepath = Path(self._download_directory, filename)
                self._database.create_partition()
                self._pandas_job.file_to_dataframe(
                    file_path=filepath,
                    engine=self._database.engine,
                )

                self._database.add_history_entry()
        else:
            _logger.info(
                f"""El padrón {self._year}{self._month} ya se encuentra importado en
                la base de datos."""
            )

        _logger.info("====End Bot===")
