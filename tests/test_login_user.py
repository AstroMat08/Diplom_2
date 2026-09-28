import allure

from api.auth_api import AuthApi


@allure.feature("Логин пользователя")
class TestLoginUser:

    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user(self, auth_api: AuthApi, existing_user: dict):
        response = auth_api.login(
            email=existing_user["email"],
            password=existing_user["password"],
        )
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert "accessToken" in body
        assert "refreshToken" in body
        assert body["user"]["email"] == existing_user["email"]

    @allure.title("Вход с неверным логином и паролем")
    def test_login_with_wrong_credentials(self, auth_api: AuthApi):
        response = auth_api.login(
            email="wrong_email@yandex.ru",
            password="wrong_password",
        )
        body = response.json()

        assert response.status_code == 401
        assert body["success"] is False
        assert body["message"] == "email or password are incorrect"