"""Lightweight logging utilities for the app.

This module provides a small, production‑friendly wrapper around Python's
:mod:`logging` with sensible defaults for Streamlit/CLI apps. It supports
console logging, optional rotating file logs, and a helper context manager
for timing code blocks.

Environment Variables
---------------------
LOG_LEVEL : str, optional
    One of DEBUG, INFO, WARNING, ERROR, CRITICAL. Defaults to INFO.
LOG_TO_CONSOLE : str, optional
    "1"/"true" to enable, "0"/"false" to disable. Defaults to enabled.
LOG_FILE : str, optional
    If set, enables rotating file logging at the given path.
LOG_MAX_BYTES : str, optional
    Max file size in bytes before rotation. Default: 1000000.
LOG_BACKUPS : str, optional
    How many rotated files to keep. Default: 3.
LOG_FORMAT : str, optional
    Logging format string. Default: "%(asctime)s | %(levelname)s | %(name)s | %(message)s".
LOG_DATEFMT : str, optional
    Datetime format string. Default: "%Y-%m-%d %H:%M:%S".

Notes
-----
- Defaults are non‑intrusive: if the app already configured logging elsewhere,
  these helpers will not duplicate handlers.
- Explicit function arguments override environment variables.

Examples
--------
>>> from src.services.logging import get_logger
>>> log = get_logger(__name__)
>>> log.info("Hello")
"""

import logging
import os
from logging.handlers import RotatingFileHandler


def _env_bool(key: str, default: str = "1") -> bool:
    """Return a boolean for an environment variable.

    Accepts 1/true/yes/on (case‑insensitive) as True, 0/false/no/off as False.
    """
    val = os.getenv(key, default)
    if val is None:
        return default.lower() in ("1", "true", "yes", "on")
    val = str(val).strip().lower()
    return val in ("1", "true", "yes", "on")


_DEFAULT_FMT = os.getenv("LOG_FORMAT", "%(asctime)s | %(levelname)s | %(name)s | %(message)s")
_DEFAULT_DATEFMT = os.getenv("LOG_DATEFMT", "%Y-%m-%d %H:%M:%S")


def _make_stream_handler(level: int) -> logging.StreamHandler:
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(_DEFAULT_FMT, datefmt=_DEFAULT_DATEFMT)
    handler.setFormatter(formatter)
    return handler


def _make_file_handler(
    file_path: str, level: int, max_bytes: int = 1000000, backup_count: int = 3
) -> RotatingFileHandler:
    handler = RotatingFileHandler(file_path, maxBytes=max_bytes, backupCount=backup_count)
    handler.setLevel(level)
    formatter = logging.Formatter(_DEFAULT_FMT, datefmt=_DEFAULT_DATEFMT)
    handler.setFormatter(formatter)
    return handler


def configure_logging(
    level: str | int | None = None, *, to_console: bool | None = None, file_path: str | None = None
) -> None:
    """Configure root logger with sensible defaults.

    Parameters
    ----------
    level : Optional[str or int], default None
        Desired log level. If ``None``, ``LOG_LEVEL`` env var or ``INFO`` is used.
    to_console : Optional[bool], default None
        If ``None``, derived from ``LOG_TO_CONSOLE`` env var (defaults to True).
    file_path : Optional[str], default None
        If ``None``, uses ``LOG_FILE`` env var (if set) to enable rotating file logging.
    """
    if level is None:
        level_str = os.getenv("LOG_LEVEL", "INFO")
        if isinstance(level_str, str):
            level_str = level_str.upper()
        resolved_level = getattr(logging, level_str, logging.INFO)
    elif isinstance(level, str):
        resolved_level = getattr(logging, level.upper(), logging.INFO)
    else:
        resolved_level = level

    # Resolve console/file settings from env if not explicitly provided
    to_console = _env_bool("LOG_TO_CONSOLE", "1") if to_console is None else to_console
    if file_path is None:
        file_path = os.getenv("LOG_FILE")

    max_bytes = int(os.getenv("LOG_MAX_BYTES", "1000000"))
    backup_count = int(os.getenv("LOG_BACKUPS", "3"))

    root = logging.getLogger()
    root.setLevel(resolved_level)

    if to_console and not any(isinstance(h, logging.StreamHandler) for h in root.handlers):
        root.addHandler(_make_stream_handler(resolved_level))

    if file_path and not any(isinstance(h, RotatingFileHandler) for h in root.handlers):
        try:
            root.addHandler(
                _make_file_handler(
                    file_path, resolved_level, max_bytes=max_bytes, backup_count=backup_count
                )
            )
        except Exception:  # pragma: no cover
            # Ignore file handler errors (e.g., read‑only FS in some PaaS)
            pass


def get_logger(
    name: str | None = None, level: str | int | None = None, file_path: str | None = None
) -> logging.Logger:
    """Get a logger with optional configuration.

    Parameters
    ----------
    name : Optional[str], default None
        Logger name. If ``None``, returns the root logger.
    level : Optional[str or int], default None
        Explicit level (overrides ``LOG_LEVEL`` if provided).
    file_path : Optional[str], default None
        Explicit file path (overrides ``LOG_FILE`` if provided).
    """
    logger = logging.getLogger(name)
    if level is not None or file_path is not None:
        configure_logging(level=level, file_path=file_path)
    return logger
