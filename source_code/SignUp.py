import os
import unittest
import time
import allure
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Base import Base
from Page import SignUpPage
from locators import SignUpLocators
load_dotenv()

class SignUpTests(Base):
    def setUp(self):
        self.driver = super().start_driver()
        self.signup = SignUpPage(self.driver)

    @allure.title("Verify user should be able to signup with valid details")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_Verify_user_should_be_able_to_signup_with_valid_details(self):
        self.signup.navigate_to_signup()
        self.signup.send_keys(SignUpLocators.USERNAME_FIELD, "newuser123")
        self.signup.send_keys(SignUpLocators.EMAIL_FIELD, "new123@test.com")
        self.signup.send_keys(SignUpLocators.PASSWORD_FIELD, "StrongPass@123")
        self.signup.click(SignUpLocators.CREATE_ACCOUNT_BUTTON)
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(SignUpLocators.SUCCESS_LOGIN_TEXT))
            assert self.signup.is_visible(SignUpLocators.SUCCESS_LOGIN_TEXT)
        except Exception:
            self.attach_screenshot("_failure")
            raise AssertionError("Signup failed for valid inputs")

    @allure.title("Verify error displays when all signup fields are empty")
    @allure.severity(allure.severity_level.NORMAL)
    def test_Verify_error_should_display_when_all_fields_empty(self):
        self.signup.navigate_to_signup()
        self.signup.click(SignUpLocators.CREATE_ACCOUNT_BUTTON)
        time.sleep(2)
        try:
            error = (self.signup.is_visible(SignUpLocators.ERROR_MESSAGES)
                or self.signup.get_toast_message()
                or self.signup.get_browser_validation_message(SignUpLocators.USERNAME_FIELD))
            assert error
        except Exception:
            self.attach_screenshot("_failure")
            raise AssertionError("No validation shown for empty signup form")

    @allure.title("Verify error displays for invalid email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_Verify_error_for_invalid_email(self):
        self.signup.navigate_to_signup()
        self.signup.send_keys(SignUpLocators.USERNAME_FIELD, "dummyuser")
        self.signup.send_keys(SignUpLocators.EMAIL_FIELD, "invalidemail")
        self.signup.send_keys(SignUpLocators.PASSWORD_FIELD, "Strong@123")
        self.signup.click(SignUpLocators.CREATE_ACCOUNT_BUTTON)
        try:
            assert (self.signup.is_visible(SignUpLocators.ERROR_MESSAGES)
                or self.signup.get_browser_validation_message(SignUpLocators.EMAIL_FIELD)
                or self.signup.get_toast_message())
        except Exception:
            self.attach_screenshot("_failure")
            raise AssertionError("Invalid email validation failed")

    @allure.title("Verify error displays for weak password")
    @allure.severity(allure.severity_level.NORMAL)
    def test_Verify_error_for_weak_password(self):
        self.signup.navigate_to_signup()
        self.signup.send_keys(SignUpLocators.USERNAME_FIELD, "user1")
        self.signup.send_keys(SignUpLocators.EMAIL_FIELD, "user1@test.com")
        self.signup.send_keys(SignUpLocators.PASSWORD_FIELD, "1234")
        self.signup.click(SignUpLocators.CREATE_ACCOUNT_BUTTON)
        time.sleep(2)
        try:
            assert (self.signup.is_visible(SignUpLocators.ERROR_MESSAGES)
                or self.signup.get_browser_validation_message(SignUpLocators.PASSWORD_FIELD)
                or self.signup.get_toast_message())
        except Exception:
            self.attach_screenshot("_failure")
            raise AssertionError("Weak password validation failed")

    @allure.title("Verify error displays for existing email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_Verify_error_for_existing_email(self):
        self.signup.navigate_to_signup()
        self.signup.send_keys(SignUpLocators.USERNAME_FIELD, "exuser")
        self.signup.send_keys(SignUpLocators.EMAIL_FIELD, "exuser@gmail.com")
        self.signup.send_keys(SignUpLocators.PASSWORD_FIELD, "StrongPass@123")
        self.signup.click(SignUpLocators.CREATE_ACCOUNT_BUTTON)
        time.sleep(2)
        try:
            assert (self.signup.get_toast_message()
                or self.signup.is_visible(SignUpLocators.ERROR_MESSAGES))
        except Exception:
            self.attach_screenshot("_failure")
            raise AssertionError("Existing email validation failed")

    @allure.title("Verify error displays for short username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_Verify_error_for_short_username(self):
        self.signup.navigate_to_signup()
        self.signup.send_keys(SignUpLocators.USERNAME_FIELD, "a")
        self.signup.send_keys(SignUpLocators.EMAIL_FIELD, "test@test.com")
        self.signup.send_keys(SignUpLocators.PASSWORD_FIELD, "StrongPass@123")
        self.signup.click(SignUpLocators.CREATE_ACCOUNT_BUTTON)
        time.sleep(2)
        try:
            assert (self.signup.get_browser_validation_message(SignUpLocators.USERNAME_FIELD)
                or self.signup.is_visible(SignUpLocators.ERROR_MESSAGES))
        except Exception:
            self.attach_screenshot("_failure")
            raise AssertionError("Short username validation failed")

    @allure.title("Verify error displays for long username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_Verify_error_for_long_username(self):
        self.signup.navigate_to_signup()
        self.signup.send_keys(SignUpLocators.USERNAME_FIELD, "a" * 51)
        self.signup.send_keys(SignUpLocators.EMAIL_FIELD, "test@test.com")
        self.signup.send_keys(SignUpLocators.PASSWORD_FIELD, "StrongPass@123")
        self.signup.click(SignUpLocators.CREATE_ACCOUNT_BUTTON)
        time.sleep(2)
        try:
            assert (self.signup.get_browser_validation_message(SignUpLocators.USERNAME_FIELD)
                or self.signup.is_visible(SignUpLocators.ERROR_MESSAGES)
                or self.signup.get_toast_message())
        except Exception:
            self.attach_screenshot("_failure")
            raise AssertionError("Long username validation failed")

    @allure.title("Verify signup behavior with spaces in input fields")
    @allure.severity(allure.severity_level.NORMAL)
    def test_Verify_signup_with_spaces_input(self):
        self.signup.navigate_to_signup()
        self.signup.send_keys(SignUpLocators.USERNAME_FIELD, "   spaceuser   ")
        self.signup.send_keys(SignUpLocators.EMAIL_FIELD, "   spaceuser@test.com   ")
        self.signup.send_keys(SignUpLocators.PASSWORD_FIELD, "StrongPass@123")
        self.signup.click(SignUpLocators.CREATE_ACCOUNT_BUTTON)
        try:
            assert (self.signup.is_visible(SignUpLocators.SUCCESS_LOGIN_TEXT)
                or self.signup.is_visible(SignUpLocators.ERROR_MESSAGES)
                or self.signup.get_toast_message())
        except Exception:
            self.attach_screenshot("_failure")
            raise AssertionError("Spaces input case not handled properly")

    def tearDown(self):
        self.quit_driver()

if __name__ == "__main__":
    unittest.main()
