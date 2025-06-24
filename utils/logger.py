import logging
import os

# Читаем желаемый уровень логирования из .env (по умолчанию INFO)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

def get_logger(name: str = __name__) -> logging.Logger:
    """
    Настраивает логгер с заданным именем:
    - выводит в консоль
    - форматирует время/уровень/модуль
    - ставит уровень из LOG_LEVEL
    """
    # Один раз настраиваем базовый конфиг
    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    return logger