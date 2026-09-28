import allure
import pytest

from api.auth_api import AuthApi

@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    @allure.description("Проверяем, что нового пользователя можно зарегистрировать, "
                        "и в ответе приходят accessToken, refreshToken и user.")
    def test_create_unique_user(self, auth_api: AuthApi, new_user_data: dict):
        response = auth_api.register(**new_user_data)
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert "accessToken" in body
        assert "refreshToken" in body
        assert body["user"]["email"] == new_user_data["email"]
        assert body["user"]["name"] == new_user_data["name"]

        # Постусловие: удаляем пользователя
        auth_api.delete_user(body["accessToken"])

    @allure.title("Создание пользователя, который уже зарегистрирован")
    @allure.description("Повторная регистрация с тем же email возвращает 403 "
                        "и сообщение 'User already exists'.")
    def test_create_duplicate_user(self, auth_api: AuthApi, created_user: dict):
        response = auth_api.register(
            email=created_user["email"],
            password=created_user["password"],
            name=created_user["name"],
        )
        body = response.json()

        assert response.status_code == 403
        assert body["success"] is False
        assert body["message"] == "User already exists"

    @allure.title("Создание пользователя без обязательного поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field(
        self, auth_api: AuthApi, new_user_data: dict, missing_field: str
    ):
        response = auth_api.register_without_field(
            email=new_user_data["email"],
            password=new_user_data["password"],
            name=new_user_data["name"],
            missing_field=missing_field,
        )
        body = response.json()

        assert response.status_code == 403
        assert body["success"] is False
        assert body["message"] == "Email, password and name are required fields"