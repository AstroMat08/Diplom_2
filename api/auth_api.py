import allure

from api.base_api import BaseApi


class AuthApi(BaseApi):
    """Методы для работы с авторизацией и пользователем."""

    REGISTER = f"{BaseApi.BASE_URL}/api/auth/register"
    LOGIN = f"{BaseApi.BASE_URL}/api/auth/login"
    LOGOUT = f"{BaseApi.BASE_URL}/api/auth/logout"
    USER = f"{BaseApi.BASE_URL}/api/auth/user"

    @allure.step("Создать пользователя: email={email}, name={name}")
    def register(self, email: str, password: str, name: str) -> dict:
        payload = {"email": email, "password": password, "name": name}
        return self.post(self.REGISTER, json=payload)

    @allure.step("Создать пользователя без поля {missing_field}")
    def register_without_field(self, email: str, password: str, name: str,
                               missing_field: str) -> dict:
        payload = {"email": email, "password": password, "name": name}
        payload.pop(missing_field, None)
        return self.post(self.REGISTER, json=payload)

    @allure.step("Авторизоваться: email={email}")
    def login(self, email: str, password: str) -> dict:
        return self.post(self.LOGIN, json={"email": email, "password": password})

    @allure.step("Выйти из системы")
    def logout(self, refresh_token: str) -> dict:
        return self.post(self.LOGOUT, json={"token": refresh_token})

    @allure.step("Удалить пользователя")
    def delete_user(self, access_token: str) -> dict:
        return self.delete(self.USER, headers={"Authorization": access_token})