import logging
import os
from functools import wraps
from pathlib import Path
from typing import Type
from collections.abc import Callable


def setup_file_logger(
    log_file: str = "app.log",
    log_level: int = logging.INFO,
    logger_name: str = "app_logger"
) -> logging.Logger:
    """
    Инициализирует и возвращает логгер, который пишет в файл с заданным форматом.

    Формат: дата| уровень | путь к файлу | функция | номер строки | Сообщение

    Args:
        log_file (str): Имя файла для логов.
        log_level (int): Уровень логирования.
        logger_name (str): Имя логгера.

    Returns:
        logging.Logger: Настроенный логгер.

    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    # Не добавлять повторно хендлеры
    if not logger.handlers:
        log_dir = Path(log_file).parent
        if log_dir and not log_dir.exists():
            os.makedirs(log_dir, exist_ok=True)

        handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter(
            fmt="%(asctime)s| %(levelname)s | %(pathname)s | %(funcName)s | %(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def with_logger(
    logger_name: str = "app_logger",
    attr_name: str = "logger"
):
    """
    Декоратор класса: добавляет атрибут logger в экземпляр класса,
    получая логгер по имени через logging.getLogger.
    """
    def decorator(cls: type):
        orig_init = cls.__init__

        @wraps(orig_init)
        def __init__(self, *args, **kwargs):
            logger = logging.getLogger(logger_name)
            setattr(self, attr_name, logger)
            orig_init(self, *args, **kwargs)

        cls.__init__ = __init__
        return cls
    return decorator


def log_method(
    level: int = logging.INFO,
    logger_attr: str = "logger"
):
    """Декоратор метода: лоцирует вызовы метода (вход, выход, ошибки)."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            logger = getattr(self, logger_attr, None)
            if logger:
                logger.log(level, f"Вызов метода {func.__qualname__} с args={args}, kwargs={kwargs}")
            try:
                result = func(self, *args, **kwargs)
                if logger:
                    logger.log(level, f"Метод {func.__qualname__} успешно завершён, результат: {result!r}")
            except Exception as e:
                if logger:
                    logger.exception(f"Ошибка в методе {func.__qualname__}: {e}")
                raise
            else:
                return result
        return wrapper
    return decorator

def log_function(
    level: int = logging.INFO,
    logger_name: str = "app_logger"
):
    """
    Декоратор для логирования вызовов обычных функций (не методов класса).
    Логирует вход, выход и ошибки функции.
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(logger_name)
            logger.log(level, f"Вызов функции {func.__qualname__} с args={args}, kwargs={kwargs}")
            try:
                result = func(*args, **kwargs)
                logger.log(level, f"Функция {func.__qualname__} успешно завершена, результат: {result!r}")

            except Exception as e:
                logger.exception(f"Ошибка в функции {func.__qualname__}: {e}")
                raise


        return wrapper
    return decorator
