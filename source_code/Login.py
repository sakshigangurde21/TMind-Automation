import os
import unittest
from Base import Base
from Page import LoginPage
from locators import LoginLocators
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import time

load_dotenv()

class LoginTests(Base):

    def setUp(self):
        self.driver = super().start_driver()
        self.login = LoginPage(self.driver)

    # 1 ---------------- POSITIVE LOGIN ----------------
    def test_Verify_user_should_be_able_to_login_with_valid_credentials(self):

        self.login.send_keys(LoginLocators.EMAIL_INPUT, os.environ.get("USER_EMAIL"))
        self.login.send_keys(LoginLocators.PASSWORD_INPUT, os.environ.get("PASSWORD"))
        self.login.click(LoginLocators.LOGIN_BUTTON)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/dashboard"))
            self.assertTrue("/dashboard" in self.driver.current_url)
        except Exception:
            try:
                self.assertEqual(0, 1)
            except AssertionError:
                raise AssertionError("Unable to login with valid credentials")

    # 2 ---------------- INVALID LOGIN ----------------
    def test_Verify_error_should_display_for_invalid_login(self):

        self.login.send_keys(LoginLocators.EMAIL_INPUT, "invalid@test.com")
        self.login.send_keys(LoginLocators.PASSWORD_INPUT, "wrongpass")
        self.login.click(LoginLocators.LOGIN_BUTTON)

        try:
            self.login.is_visible(LoginLocators.TOAST_ERROR)
        except Exception:
            try:
                self.assertEqual(0, 1)
            except AssertionError:
                raise AssertionError("Error message not shown for invalid login")

    # 3 ---------------- EMPTY PASSWORD ----------------
    def test_Verify_error_for_empty_password(self):

        self.login.send_keys(LoginLocators.EMAIL_INPUT, "test@test.com")
        self.login.click(LoginLocators.LOGIN_BUTTON)

        try:
            self.login.is_visible(LoginLocators.ERROR_MSG)
        except Exception:
            try:
                self.assertEqual(0, 1)
            except AssertionError:
                raise AssertionError("Empty password validation failed")

    # 4 ---------------- EMPTY EMAIL ----------------
    def test_Verify_error_for_empty_email(self):

        self.login.send_keys(LoginLocators.PASSWORD_INPUT, "Test1234")
        self.login.click(LoginLocators.LOGIN_BUTTON)

        try:
            self.login.is_visible(LoginLocators.ERROR_MSG)
        except Exception:
            try:
                self.assertEqual(0, 1)
            except AssertionError:
                raise AssertionError("Empty email validation failed")

    # 5 ---------------- BOTH FIELDS EMPTY ----------------
    def test_Verify_error_when_both_fields_empty(self):

        self.login.click(LoginLocators.LOGIN_BUTTON)

        try:
            self.login.is_visible(LoginLocators.ERROR_MSG)
        except Exception:
            try:
                self.assertEqual(0, 1)
            except AssertionError:
                raise AssertionError("No validation shown for empty login form")

    # 6 ---------------- SHORT PASSWORD ----------------
    def test_Verify_error_for_short_password(self):

        self.login.send_keys(LoginLocators.EMAIL_INPUT, "test@test.com")
        self.login.send_keys(LoginLocators.PASSWORD_INPUT, "123")
        self.login.click(LoginLocators.LOGIN_BUTTON)

        try:
            self.login.is_visible(LoginLocators.TOAST_ERROR)
        except Exception:
            try:
                self.assertEqual(0, 1)
            except AssertionError:
                raise AssertionError("Short password validation failed")

    # 7 ---------------- LOGOUT ----------------
    def test_Verify_user_should_be_able_to_logout(self):

        self.login.send_keys(LoginLocators.EMAIL_INPUT, os.environ.get("USER_EMAIL"))
        self.login.send_keys(LoginLocators.PASSWORD_INPUT, os.environ.get("PASSWORD"))
        self.login.click(LoginLocators.LOGIN_BUTTON)

        time.sleep(5)

        self.login.click(LoginLocators.PROFILE_ICON)
        self.login.click(LoginLocators.LOGOUT_BUTTON)

        try:
            self.login.is_visible(LoginLocators.LOGIN_BUTTON)
        except Exception:
            try:
                self.assertEqual(0, 1)
            except AssertionError:
                raise AssertionError("Logout failed")
            
    def test_Verify_back_button_should_not_logout_user_after_login(self):

        self.login.send_keys(LoginLocators.EMAIL_INPUT, os.environ.get("USER_EMAIL"))
        self.login.send_keys(LoginLocators.PASSWORD_INPUT, os.environ.get("PASSWORD"))
        self.login.click(LoginLocators.LOGIN_BUTTON)

        time.sleep(5)
        self.login.click(LoginLocators.PROFILE_ICON)
        self.driver.back()

        try:
            self.login.is_visible(LoginLocators.PROFILE_ICON)
        except Exception:
            try:
                self.assertEqual(0, 1)
            except AssertionError:
                raise AssertionError("User logged out or profile icon not visible after browser back button")

    # ---------------- CLEANUP ----------------
    def tearDown(self):
        self.quit_driver()

if __name__ == "__main__":
    unittest.main()
