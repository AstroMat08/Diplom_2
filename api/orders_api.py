import allure

from api.base_api import BaseApi


class OrdersApi(BaseApi):
    """Методы для работы с заказами."""

    ORDERS = f"{BaseApi.BASE_URL}/api/orders"

    @allure.step("Создать заказ с ингредиентами: {ingredients}")
    def create_order(self, ingredients: list, access_token: str = None) -> dict:
        headers = {"Authorization": access_token} if access_token else {}
        return self.post(self.ORDERS, json={"ingredients": ingredients}, headers=headers)