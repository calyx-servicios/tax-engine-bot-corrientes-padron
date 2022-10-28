"""Modulo de navegacion selenium por la página de DGR"""
import logging
import os
import time
from pathlib import Path
from abc import ABC, abstractmethod

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from xpath import AgenteIngresosBrutosPage, LoginPage, MainPage, NewsRGPage, TxtViewPage

# pylint: disable=unnecessary-ellipsis

class BaseDGRPadron(ABC):
    """Clase base para navegar y scrapear los elementos deDGR Corrientes."""

    PADRON_NAME_TEMPLATE: str = None

    def __init__(
        self,
        month,
        year,
        username,
        password,
        full_download_path,
        driver,
        logger=None,
        implicit_wait=10,
    ):
        self._logger = logger if logger else logging.getLogger("ROBOT.SeleniumPadron")
        self.driver = driver
        self.__user = username
        self.__pass = password
        self._down_path = full_download_path
        self.driver.implicitly_wait(implicit_wait)
        self.__retries = 0
        self.__max_retries = 5
        self._month = month
        self._year = year

    def _login(self):
        """Logearse a la página de Corrientes"""
        self.driver.get(LoginPage.PAGE_URL)
        user_elem = self.driver.find_element(By.XPATH, LoginPage.USER)
        user_elem.send_keys(self.__user)
        pass_elem = self.driver.find_element(By.XPATH, LoginPage.PASS)
        pass_elem.send_keys(self.__pass)
        submit = self.driver.find_element(By.XPATH, LoginPage.SUBMIT)
        submit.click()

    def _goto_news(self):
        """Ir a la sección de novedades"""
        self.driver.find_element(By.XPATH, MainPage.DROPDOWN_SERVICES).click()
        self.driver.find_element(By.XPATH, MainPage.INGRESOS_BRUTOS).click()
        self.driver.find_element(By.XPATH, AgenteIngresosBrutosPage.NEWS_RG).click()

    @abstractmethod
    def _goto_padron(self):
        """Ir a la respectiva sección de descarga de padrones"""
        ...

    @abstractmethod
    def _get_padrones_list(self):
        """Obtener y retornar la lista de filas de padrones"""
        ...

    def _goto_downloads(self, list_element):
        """Retorna el nombre del archivo del padrón más reciente."""
        name = None
        try:
            name = list_element.find_element(By.XPATH, NewsRGPage.RELATIVE_FILENAME).text
        except StaleElementReferenceException as ex:
            time.sleep(0.5)
            self.__retries += 1
            if self.__retries < self.__max_retries:
                list_element = self._get_padrones_list()
                name = self._goto_downloads(list_element)
            else:
                raise Exception(
                    f"No cargó la tabla de padrones despues de {self.__retries} intentos."
                ) from ex
        return name

    def _prepare_download(self):
        """Se logea a la página y la navega hasta dejar al webdriver con la
        tabla a usar activa como para descargar posteriormente.
        """
        self._login()
        self._goto_news()
        self._goto_padron()
        padrones = self._get_padrones_list()
        self._goto_downloads(padrones)

    def _get_padron_name(self):
        return self.PADRON_NAME_TEMPLATE.format(month=self._month, year=self._year)

    def _download_success(self, timeout_secs=600, check_frequency=0.5):
        """Checks for download success by expected filename"""
        dl_wait = True
        seconds = 0
        success = False

        while dl_wait and seconds < timeout_secs:
            time.sleep(check_frequency)
            if self._already_downloaded():
                dl_wait = False
                success = True
            seconds += check_frequency

        return success

    def _already_downloaded(self):
        """Retorna True si ya fue descargado el archivo en el directorio de descargas"""
        filepath = Path(self._down_path, self._get_padron_name()).resolve()
        return filepath.is_file()

    def download_padron(self):
        """Descarga el último padrón. Retorna true si se llegó a descargar
        y false si no se llegó.
        """

        padron_name = self._get_padron_name()
        filename = os.path.join(self._down_path, padron_name)

        if not self._already_downloaded():

            self._logger.info("El padrón no estaba descargado. Iniciando proceso de descarga.")

            self._prepare_download()
            list_element = self._get_padrones_list()
            list_element.find_element(
                By.XPATH, NewsRGPage.FORMAT_PADRON_NAME_DOWNLOAD_BTN.format(padron_name=padron_name)
            ).click()

            if self._download_success():
                return filename
            return ""
        else:
            self._logger.info("Padrón ya descargado")
            return filename


class DGRPadronExcluidos(BaseDGRPadron):
    """Clase para operar sobre el padrón de excluidos"""

    PADRON_NAME_TEMPLATE: str = "CTES_RG202_Novedades_{year}{month}.txt"

    def _goto_padron(self):
        self.driver.find_element(By.XPATH, NewsRGPage.EXCLUDED_HEADER).click()

    def _get_padrones_list(self):
        return self.driver.find_element(By.XPATH, NewsRGPage.EXCLUDED_LIST)

    def _prepare_download(self):
        """prepare_download"""
        self._logger.info("Obteniendo padrón excluidos")
        return super()._prepare_download()

    def download_padron(self):
        """Abre el url con el texto interno del txt y crea un txt en base a el."""

        padron_name = self._get_padron_name()
        filename = os.path.join(self._down_path, padron_name)

        if not self._already_downloaded():
            try:
                self._prepare_download()
                list_element = self._get_padrones_list()
                list_element.find_element(
                    By.XPATH,
                    NewsRGPage.FORMAT_PADRON_NAME_DOWNLOAD_BTN.format(padron_name=padron_name),
                ).click()
                self.driver.switch_to.window(self.driver.window_handles[::-1][0])
                text = self.driver.find_element(By.XPATH, TxtViewPage.FILETEXT).text

                with open(filename, "w", encoding="utf-8") as file:
                    file.write(text)
                return filename
            except Exception as ex:
                self._logger.error(f"No se pudo escribir el .txt. {ex}")
                raise ex
        else:
            self._logger.info("Padrón ya descargado")
            return filename


class DGRPadronPasiblesMultil(BaseDGRPadron):
    """Clase para operar sobre el padrón de pasibles convenio"""

    PADRON_NAME_TEMPLATE: str = "PasiblesConvenioRG202_2020_{year}{month}.xlsx"

    def _goto_padron(self):
        self.driver.find_element(By.XPATH, NewsRGPage.PASIBLES_HEADER).click()
        self.driver.find_element(By.XPATH, NewsRGPage.MULTI_COLLAPSE).click()

    def _get_padrones_list(self):
        return self.driver.find_element(By.XPATH, NewsRGPage.MULTI_LIST)

    def _prepare_download(self):
        """prepare_download"""
        self._logger.info("Obteniendo padrón pasibles miultilateral")
        return super()._prepare_download()


class DGRPadronPasiblesLocal(BaseDGRPadron):
    """Clase para operar sobre el padrón de pasibles locales"""

    PADRON_NAME_TEMPLATE: str = "PasiblesLocalesRG202_2020_{year}{month}.xlsx"

    def _goto_padron(self):
        self.driver.find_element(By.XPATH, NewsRGPage.PASIBLES_HEADER).click()
        self.driver.find_element(By.XPATH, NewsRGPage.LOCAL_COLLAPSE).click()

    def _get_padrones_list(self):
        return self.driver.find_element(By.XPATH, NewsRGPage.LOCAL_LIST)

    def _prepare_download(self):
        """prepare_download"""
        self._logger.info("Obteniendo padrón pasibles local")
        return super()._prepare_download()
