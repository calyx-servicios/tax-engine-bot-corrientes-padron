"""Selenium Job"""

import logging
from pathlib import Path

from decouple import config
from selenium import webdriver

from padron_types import MODES

_logger = logging.getLogger(__name__)


class SeleniumJob:
    """Selenium Job"""

    def __init__(self, download_directory, month, year, table):
        self._month = month
        self._year = year
        self._cuit = config("CUIT")
        self._password = config("PASSWORD")
        self._download_directory = download_directory
        Path(self._download_directory).mkdir(parents=True, exist_ok=True)
        self._driver = webdriver.Chrome(options=self._get_options())
        self._dgr = MODES[table](
            self._month,
            self._year,
            self._cuit,
            self._password,
            self._download_directory,
            self._driver,
        )

    def _get_options(self):
        """Define Web self._driver options"""
        options = webdriver.ChromeOptions()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        user_agent += "(KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
        _args = [
            f"user-agent={user_agent}",
            "--window-size=1920,1080",
            "--ignore-certificate-errors",
            "--allow-running-insecure-content",
            "--disable-extensions",
            "--start-maximized",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--no-sandbox",
            "--proxy-server='direct://'",
            "--proxy-bypass-list=*",
        ]

        options.headless = True
        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": self._download_directory,
                "download.prompt_for_download": False,
            },
        )
        for arg in _args:
            options.add_argument(arg)
        return options

    def download_from_source(self):
        """Procedimiento de descarga que comparten todos los tipos de padrón.
        Descarga el padrón solo si es más reciente al actual. Retorna una tupla con
        la ruta a él y un booleano correspondiente a si es antiguo o no."""
        padron_name = self._dgr.download_padron()
        if len(padron_name) > 0:
            _logger.info("Se descargó exitosamente.")
            return Path(self._download_directory, padron_name)
        _logger.error("No se pudo descargar el padrón.")
        raise RuntimeError(f"Error al descargar el padrón {padron_name}")
