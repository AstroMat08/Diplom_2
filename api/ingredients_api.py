import allure

from api.base_api import BaseApi


class IngredientsApi(BaseApi):
    """Методы для работы с ингредиентами."""

    INGREDIENTS = f"{BaseApi.BASE_URL}/api/ingredients"

    @allure.step("Получить все ингредиенты")
    def get_ingredients(self) -> dict:
        return self.get(self.INGREDIENTS)

    def get_ingredient_ids(self, count: int = 2) -> list:
        """Возвращает список id ингредиентов для заказа."""
        response = self.get_ingredients()
        data = response.json()
        ids = [item["_id"] for item in data["data"]]
        return ids[:count]