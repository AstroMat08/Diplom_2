import allure
import pytest

from api.auth_api import AuthApi
from api.ingredients_api import IngredientsApi
from api.orders_api import OrdersApi
from data.test_data import (
    generate_email,
    generate_password,
    generate_name,
    EXISTING_USER_EMAIL,
    EXISTING_USER_PASSWORD,
    EXISTING_USER_NAME,
)


@pytest.fixture
def auth_api() -> AuthApi:
    return AuthApi()


@pytest.fixture
def orders_api() -> OrdersApi:
    return OrdersApi()


@pytest.fixture
def ingredients_api() -> IngredientsApi:
    return IngredientsApi()


@pytest.fixture
def new_user_data() -> dict:
    """Данные для нового уникального пользователя."""
    return {
        "email": generate_email(),
        "password": generate_password(),
        "name": generate_name(),
    }


@pytest.fixture
def created_user(auth_api: AuthApi, new_user_data: dict):
    """Создаёт пользователя и удаляет его после теста. Возвращает
    (email, password, name, access_token, refresh_token)."""
    response = auth_api.register(**new_user_data)
    body = response.json()
    access_token = body.get("accessToken")
    refresh_token = body.get("refreshToken")

    yield {
        **new_user_data,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

    with allure.step("Постусловие: удаление созданного пользователя"):
        auth_api.delete_user(access_token)


@pytest.fixture
def existing_user(auth_api: AuthApi):
    """Регистрирует пользователя и удаляет после теста.
    Возвращает email, password."""
    email = generate_email()
    password = generate_password()
    name = generate_name()

    response = auth_api.register(email, password, name)
    access_token = response.json().get("accessToken")

    yield {"email": email, "password": password}

    with allure.step("Постусловие: удаление пользователя"):
        auth_api.delete_user(access_token)