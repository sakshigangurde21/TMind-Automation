import os
import unittest
import time
import allure
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Base import Base
from Page import LoginPage
from locators import LoginLocators

load_dotenv()

class LoginTests(Base):

    def setUp(self):
        self.driver = super().start_driver()
        self.login = LoginPage(self.driver)

    @allure.title("Verify user can login with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_Verify_user_should_be_able_to_login_with_valid_credentials(self):
        self.login.send_keys(LoginLocators.EMAIL_INPUT, os.environ.get("USER_EMAIL"))
        self.login.send_keys(LoginLocators.PASSWORD_INPUT, os.environ.get("PASSWORD"))
        self.login.click(LoginLocators.LOGIN_BUTTON)
        WebDriverWait(self.driver, 10).until(EC.url_contains("/dashboard"))
        try:
            assert "/dashboard" in self.driver.current_url
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Unable to login with valid credentials")

    @allure.title("Verify error displays for invalid login")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_Verify_error_should_display_for_invalid_login(self):
        self.login.send_keys(LoginLocators.EMAIL_INPUT, "User21@gmail.com")
        self.login.send_keys(LoginLocators.PASSWORD_INPUT, "User@123")
        self.login.click(LoginLocators.LOGIN_BUTTON)
        time.sleep(2)
        try:
            assert self.login.is_visible(LoginLocators.TOAST_ERROR), "Error message not shown for invalid login"
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify error for empty email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_Verify_error_for_empty_email(self):
        self.login.send_keys(LoginLocators.PASSWORD_INPUT, "Test@123")
        self.login.click(LoginLocators.LOGIN_BUTTON)
        time.sleep(2)
        try:
            assert self.login.is_visible(LoginLocators.ERROR_MSG), \
                "Validation not shown for empty email"
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify error for empty password")
    @allure.severity(allure.severity_level.NORMAL)
    def test_Verify_error_for_empty_password(self):
        self.login.send_keys(LoginLocators.EMAIL_INPUT, "test@test.com")
        self.login.click(LoginLocators.LOGIN_BUTTON)
        time.sleep(2)
        try:
            assert self.login.is_visible(LoginLocators.ERROR_MSG), \
                "Validation not shown for empty password"
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify error when both fields are empty")
    @allure.severity(allure.severity_level.NORMAL)
    def test_Verify_error_when_both_fields_empty(self):
        self.login.click(LoginLocators.LOGIN_BUTTON)
        time.sleep(2)
        try:
            assert self.login.is_visible(LoginLocators.ERROR_MSG), \
                "Validation not shown when both fields are empty"
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify error for short password")
    @allure.severity(allure.severity_level.NORMAL)
    def test_Verify_error_for_short_password(self):
        self.login.send_keys(LoginLocators.EMAIL_INPUT, "test@test.com")
        self.login.send_keys(LoginLocators.PASSWORD_INPUT, "123")
        self.login.click(LoginLocators.LOGIN_BUTTON)
        time.sleep(2)
        try:
            assert self.login.is_visible(LoginLocators.TOAST_ERROR), "Short password validation failed"
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify user can logout successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_Verify_user_should_be_able_to_logout(self):
        self.login.send_keys(LoginLocators.EMAIL_INPUT, os.environ.get("USER_EMAIL"))
        self.login.send_keys(LoginLocators.PASSWORD_INPUT, os.environ.get("PASSWORD"))
        self.login.click(LoginLocators.LOGIN_BUTTON)
        time.sleep(5)
        self.login.click(LoginLocators.PROFILE_ICON)
        self.login.click(LoginLocators.LOGOUT_BUTTON)
        time.sleep(2)
        try:
            assert self.login.is_visible(LoginLocators.LOGIN_BUTTON), "Logout failed"
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    # 8 ---------------- BACK BUTTON ----------------
    @allure.title("Verify back button does not logout user after login")
    @allure.severity(allure.severity_level.NORMAL)
    def test_Verify_back_button_should_not_logout_user_after_login(self):
        self.login.send_keys(LoginLocators.EMAIL_INPUT, os.environ.get("USER_EMAIL"))
        self.login.send_keys(LoginLocators.PASSWORD_INPUT, os.environ.get("PASSWORD"))
        self.login.click(LoginLocators.LOGIN_BUTTON)
        time.sleep(5)
        self.login.click(LoginLocators.PROFILE_ICON)
        self.driver.back()
        time.sleep(2)
        try:
            assert self.login.is_visible(LoginLocators.PROFILE_ICON), "User logged out after browser back"
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    # ---------------- CLEANUP ----------------
    def tearDown(self):
        self.quit_driver()

if __name__ == "__main__":
    unittest.main()
