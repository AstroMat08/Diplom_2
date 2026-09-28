import allure
import requests


class BaseApi:
    """Базовый класс для работы с API. Содержит обёртки над HTTP-методами."""

    BASE_URL = "https://stellarburgers.education-services.ru"

    @staticmethod
    @allure.step("POST {url}")
    def post(url: str, json: dict = None, headers: dict = None) -> requests.Response:
        return requests.post(url, json=json, headers=headers)

    @staticmethod
    @allure.step("GET {url}")
    def get(url: str, headers: dict = None) -> requests.Response:
        return requests.get(url, headers=headers)

    @staticmethod
    @allure.step("PATCH {url}")
    def patch(url: str, json: dict = None, headers: dict = None) -> requests.Response:
        return requests.patch(url, json=json, headers=headers)

    @staticmethod
    @allure.step("DELETE {url}")
    def delete(url: str, headers: dict = None) -> requests.Response:
        return requests.delete(url, headers=headers)