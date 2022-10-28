"""Pandas Job"""
import logging
from datetime import datetime
from sys import exc_info

import pandas as pd
from padron_types import HEADERS, SEPARATIONS, COL_TYPES

_logger = logging.getLogger(__name__)
pd.options.mode.chained_assignment = None  # default='warn'


class PandasJob:
    """Pandas Job"""

    _chunk_size = 50000

    def __init__(self, month, year, table):
        self._table = table
        self._year = year
        self._month = month

    def _format_date(self, _date):
        """Format date"""
        if isinstance(_date, str):
            _date = datetime.strptime(_date, "%Y%m")
        return _date

    def split_dataframe(self, df, chunk_size):
        chunks = list()
        num_chunks = len(df) // chunk_size + 1
        for i in range(num_chunks):
            chunks.append(df[i * chunk_size : (i + 1) * chunk_size])
        return chunks

    def file_to_dataframe(self, file_path, engine):
        """File to dataframe"""
        try:
            _logger.info("=== File to dataframe ===")
            _logger.info(f"Reading file: {file_path}")

            headers = HEADERS[self._table]

            if self._table == "corrientes_padron_excluidos":
                field_widths = SEPARATIONS[self._table]
                col_types = COL_TYPES[self._table]

                for i, chunk in enumerate(
                    pd.read_fwf(
                        file_path,
                        widths=field_widths,
                        encoding="utf-8",
                        header=None,
                        names=headers,
                        parse_dates=["fecha_vigencia_desde", "fecha_vigencia_hasta"],
                        dtype=col_types,
                        skipinitialspace=True,
                        index_col=False,
                        chunksize=self._chunk_size,
                    )
                ):
                    columns = ["fecha_vigencia_desde", "fecha_vigencia_hasta"]
                    for col in columns:
                        chunk[col] = [self._format_date(fecha) for fecha in chunk[col]]

                    chunk["alicuota"] = [float(al) / 100 for al in chunk["alicuota"]]
                    chunk["razon_social"] = [rs.rstrip("0") for rs in chunk["razon_social"]]

                    chunk.insert(0, "fecha", datetime.now())
                    chunk["periodo"] = f"{self._year}{self._month}"
                    _logger.info(f"Dataframe chunk {i} generated ")
                    chunk.to_sql(self._table, engine, if_exists="append", index=False)

            else:
                dataframe = pd.read_excel(
                    file_path, header=None, names=headers, dtype={"cuit": "str"}, skiprows=[0]
                )
                for i, chunk in enumerate(
                    self.split_dataframe(dataframe, chunk_size=self._chunk_size)
                ):
                    chunk.insert(0, "fecha", datetime.now())
                    chunk["periodo"] = f"{self._year}{self._month}"
                    _logger.info(f"Dataframe chunk {i} generated ")
                    chunk.to_sql(self._table, engine, if_exists="append", index=False)

        except Exception as error:
            traceback = exc_info()[2]
            _logger.error("Dataframe creation error: %s", error.with_traceback(traceback))
            raise error
