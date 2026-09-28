import allure

from api.auth_api import AuthApi
from api.ingredients_api import IngredientsApi
from api.orders_api import OrdersApi
from data.test_data import INVALID_INGREDIENT_HASH


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_authorized(
        self,
        auth_api: AuthApi,
        orders_api: OrdersApi,
        ingredients_api: IngredientsApi,
        created_user: dict,
    ):
        ingredient_ids = ingredients_api.get_ingredient_ids(count=2)

        response = orders_api.create_order(
            ingredients=ingredient_ids,
            access_token=created_user["access_token"],
        )
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert "order" in body
        assert "number" in body["order"]

    @allure.title("Создание заказа без авторизации")
    @allure.description(
        "По документации заказ требует авторизации и должен возвращать 401. "
        "Фактически API принимает заказ без токена и возвращает 200. "
        "Тест фиксирует реальное поведение бэкенда."
    )
    def test_create_order_unauthorized(
        self,
        orders_api: OrdersApi,
        ingredients_api: IngredientsApi,
    ):
        ingredient_ids = ingredients_api.get_ingredient_ids(count=2)

        response = orders_api.create_order(ingredients=ingredient_ids)
        body = response.json()

        # Фактическое поведение API
        assert response.status_code == 200
        assert body["success"] is True
        assert "order" in body
        assert "number" in body["order"]

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(
        self,
        orders_api: OrdersApi,
        created_user: dict,
    ):
        response = orders_api.create_order(
            ingredients=[],
            access_token=created_user["access_token"],
        )
        body = response.json()

        assert response.status_code == 400
        assert body["success"] is False
        assert body["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_hash(
        self,
        orders_api: OrdersApi,
        created_user: dict,
    ):
        response = orders_api.create_order(
            ingredients=[INVALID_INGREDIENT_HASH],
            access_token=created_user["access_token"],
        )

        assert response.status_code == 500