"""Modulo de rutas XPATH de la página"""
# Los nombres de las clases son demasiado genéricos así que
# hay que usar xpaths más largos y complejos para navegar.

# pylint: disable=line-too-long
# flake8: noqa: E501


class LoginPage:
    """XPATH de página de login"""

    PAGE_URL = "https://miportal.dgrcorrientes.gov.ar/"

    USER = "//input[@id='username']"
    PASS = "//input[@id='loginPassword']"
    SUBMIT = "//button[@id='ingresar']"


class MainPage:
    """XPATH de página principal"""

    DROPDOWN_SERVICES = "//*[contains(@class, 'navbar-collapse')]//*[contains(@class, 'dropdown') and contains(@class, 'nav-item')][1]"
    INGRESOS_BRUTOS = "//*[contains(@class, 'navbar-collapse')]//*[contains(@class, 'dropdown-menu')]/a[contains(text(), 'Agentes')]"


class AgenteIngresosBrutosPage:
    """XPATH de página de ingresos brutos"""

    NEWS_RG = "//*[contains(@class, 'box')]//button[last()]"


class NewsRGPage:
    """XPATH de Novedades de RG"""

    EXCLUDED_HEADER = "//*[contains(@class, 'nav-link') and contains(text(), 'Excluido')]"
    PASIBLES_HEADER = "//*[contains(@class, 'nav-link') and contains(text(), 'Pasible')]"

    SECTION_HEADERS = "//div[contains(@class, 'slick-track')]"

    TABLES = "//div[contains(@class, 'listContainer')]"
    EXCLUDED_TABLE = "//div[contains(@class, 'active')]//div[contains(@class, 'tasas')]//div[contains(@class, 'listBody')]"
    MULTI_TABLE = "//div[contains(@class, 'active')]//div[contains(@class, 'accordion') and .//*[contains(text(), 'Multi')]]"
    LOCAL_TABLE = "//div[contains(@class, 'active')]//div[contains(@class, 'accordion') and .//*[contains(text(), 'Local')]]"

    MULTI_COLLAPSE = "//div[contains(@class, 'active')]//div[contains(@class, 'accordion') and .//*[contains(text(), 'Multi')]]"
    LOCAL_COLLAPSE = "//div[contains(@class, 'active')]//div[contains(@class, 'accordion') and .//*[contains(text(), 'Local')]]"

    EXCLUDED_LIST = "//div[contains(@class, 'active')]//div[contains(@class, 'tasas')]//div[contains(@class, 'listBody')]//*"
    MULTI_LIST = "//div[contains(@class, 'active')]//div[contains(@class, 'accordion') and .//*[contains(text(), 'Multi')]]//div[contains(@class, 'listBody')]//*"
    LOCAL_LIST = "//div[contains(@class, 'active')]//div[contains(@class, 'accordion') and .//*[contains(text(), 'Local')]]//div[contains(@class, 'listBody')]//*"

    RELATIVE_FILENAME = (
        ".//div[contains(@class, 'itemTramite')]//div[contains(@class, 'col')][3]//p"
    )
    FORMAT_PADRON_NAME_DOWNLOAD_BTN = (
        "//div[contains(@class, 'itemTramite') and .//*[contains(text(), '{padron_name}')]]"
        "//div[contains(@class, 'buttonsContainer')]//a"
    )


class TxtViewPage:
    """XPATH de página de vista de archivo TXT"""

    FILETEXT = "//pre"
