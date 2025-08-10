"""
Export pandas DataFrames to CSV/Excel byte streams for Streamlit downloads.

Functions
---------
to_csv_bytes(df: pd.DataFrame) -> bytes
    Convert a DataFrame to CSV format as bytes.

to_excel_bytes(df: pd.DataFrame) -> bytes
    Convert a DataFrame to an Excel XLSX file in memory as bytes.
"""

from __future__ import annotations

from io import BytesIO

import pandas as pd


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    """
    Convert a pandas DataFrame to CSV format and return as bytes.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to convert to CSV.

    Returns
    -------
    bytes
        CSV data encoded as UTF-8 bytes.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    >>> csv_bytes = to_csv_bytes(df)
    >>> print(csv_bytes.decode('utf-8'))
    A,B
    1,3
    2,4
    """
    return df.to_csv(index=False).encode("utf-8")


def to_excel_bytes(df: pd.DataFrame) -> bytes:
    """
    Return an in-memory XLSX file for download from a pandas DataFrame.

    Tries to use the 'xlsxwriter' engine first; if unavailable, falls back to 'openpyxl'.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to convert to an Excel XLSX file.

    Returns
    -------
    bytes
        The Excel file as bytes.

    Raises
    ------
    ImportError
        If neither 'xlsxwriter' nor 'openpyxl' engines are available.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    >>> excel_bytes = to_excel_bytes(df)
    >>> with open('output.xlsx', 'wb') as f:
    ...     f.write(excel_bytes)
    """
    buffer = BytesIO()
    try:
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Plan")
    except Exception:
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Plan")
    buffer.seek(0)
    return buffer.read()
