import random
import string


def generate_email() -> str:
    """Генерирует уникальный email для тестов."""
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{suffix}@yandex.ru"


def generate_password() -> str:
    return "password123"


def generate_name() -> str:
    return "TestUser"


# Фиксированные тестовые данные для негативных проверок
EXISTING_USER_EMAIL = "test-data@yandex.ru"
EXISTING_USER_PASSWORD = "password"
EXISTING_USER_NAME = "Username"

WRONG_EMAIL = "wrong_email@yandex.ru"
WRONG_PASSWORD = "wrong_password"

INVALID_INGREDIENT_HASH = "60d3b41abdcacb0026a733c6999"