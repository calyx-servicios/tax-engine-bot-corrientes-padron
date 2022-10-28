"""Modulo con informacion de los tipos de padrones de corrientes"""
from typing import Dict

from dgr_padron import (
    BaseDGRPadron,
    DGRPadronExcluidos,
    DGRPadronPasiblesLocal,
    DGRPadronPasiblesMultil,
)

HEADERS = {
    "corrientes_padron_excluidos": [
        "tipo_operacion",
        "cuit",
        "alicuota",
        "razon_social",
        "fecha_vigencia_desde",
        "fecha_vigencia_hasta",
        "periodo",
    ],
    "corrientes_padron_convenio": ["cuit", "razon_social"],
    "corrientes_padron_locales": ["cuit", "razon_social"],
}

COL_TYPES = {
    "corrientes_padron_excluidos": {
        "tipo_operacion": "str",
        "cuit": "str",
        "alicuota": "str",
        "razon_social": "str",
        "fecha_vigencia_desde": "date",
        "fecha_vigencia_hasta": "date",
        "periodo": "str",
    },
}

SEPARATIONS = {"corrientes_padron_excluidos": [1, 11, 3, 70, 6, 6, 6]}

MODES: Dict[str, BaseDGRPadron] = {
    "corrientes_padron_excluidos": DGRPadronExcluidos,
    "corrientes_padron_locales": DGRPadronPasiblesLocal,
    "corrientes_padron_convenio": DGRPadronPasiblesMultil,
}
