import os
import unittest
from Base import Base
from Page import SignUpPage
from locators import SignUpLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

class SignUpTests(Base):

    def setUp(self):
        self.driver = super().start_driver()
        self.signup = SignUpPage(self.driver)

    # ---------------- SIGNUP SUCCESS ----------------
    def test_Verify_user_should_be_able_to_signup_with_valid_details(self):
        self.signup.navigate_to_signup()

        self.signup.send_keys(SignUpLocators.USERNAME_FIELD, "newuser123")
        self.signup.send_keys(SignUpLocators.EMAIL_FIELD, "new123@test.com")
        self.signup.send_keys(SignUpLocators.PASSWORD_FIELD, "StrongPass@123")
        self.signup.click(SignUpLocators.CREATE_ACCOUNT_BUTTON)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(SignUpLocators.SUCCESS_LOGIN_TEXT)
            )
            self.assertTrue(
                self.signup.is_visible(SignUpLocators.SUCCESS_LOGIN_TEXT)
            )
        except Exception:
            raise AssertionError("Signup failed for valid inputs")

    # ---------------- EMPTY FIELDS ----------------
    def test_Verify_error_should_display_when_all_fields_empty(self):
        self.signup.navigate_to_signup()
        self.signup.click(SignUpLocators.CREATE_ACCOUNT_BUTTON)

        try:
            error = (
                self.signup.is_visible(SignUpLocators.ERROR_MESSAGES)
                or self.signup.get_toast_message()
                or self.signup.get_browser_validation_message(SignUpLocators.USERNAME_FIELD))
            self.assertTrue(error)
        except Exception:
            raise AssertionError("No validation shown for empty signup form")

    # ---------------- INVALID EMAIL ----------------
    def test_Verify_error_for_invalid_email(self):
        self.signup.navigate_to_signup()

        self.signup.send_keys(SignUpLocators.USERNAME_FIELD, "dummyuser")
        self.signup.send_keys(SignUpLocators.EMAIL_FIELD, "invalidemail")
        self.signup.send_keys(SignUpLocators.PASSWORD_FIELD, "Strong@123")
        self.signup.click(SignUpLocators.CREATE_ACCOUNT_BUTTON)

        try:
            self.assertTrue(
                self.signup.is_visible(SignUpLocators.ERROR_MESSAGES)
                or self.signup.get_browser_validation_message(SignUpLocators.EMAIL_FIELD)
                or self.signup.get_toast_message())
        except Exception:
            raise AssertionError("Invalid email validation failed")

    # ---------------- WEAK PASSWORD ----------------
    def test_Verify_error_for_weak_password(self):
        self.signup.navigate_to_signup()

        self.signup.send_keys(SignUpLocators.USERNAME_FIELD, "user1")
        self.signup.send_keys(SignUpLocators.EMAIL_FIELD, "user1@test.com")
        self.signup.send_keys(SignUpLocators.PASSWORD_FIELD, "1234")
        self.signup.click(SignUpLocators.CREATE_ACCOUNT_BUTTON)

        try:
            self.assertTrue(
                self.signup.is_visible(SignUpLocators.ERROR_MESSAGES)
                or self.signup.get_browser_validation_message(SignUpLocators.PASSWORD_FIELD)
                or self.signup.get_toast_message())
        except Exception:
            raise AssertionError("Weak password validation failed")

    # ---------------- EXISTING EMAIL ----------------
    def test_Verify_error_for_existing_email(self):
        self.signup.navigate_to_signup()
        self.signup.send_keys(SignUpLocators.USERNAME_FIELD, "exuser")
        self.signup.send_keys(SignUpLocators.EMAIL_FIELD, "exuser@gmail.com")
        self.signup.send_keys(SignUpLocators.PASSWORD_FIELD, "StrongPass@123")
        self.signup.click(SignUpLocators.CREATE_ACCOUNT_BUTTON)

        try:
            self.assertTrue(
                self.signup.get_toast_message()
                or self.signup.is_visible(SignUpLocators.ERROR_MESSAGES))
        except Exception:
            raise AssertionError("Existing email validation failed")

    # ---------------- SHORT USERNAME ----------------
    def test_Verify_error_for_short_username(self):
        self.signup.navigate_to_signup()

        self.signup.send_keys(SignUpLocators.USERNAME_FIELD, "a")
        self.signup.send_keys(SignUpLocators.EMAIL_FIELD, "test@test.com")
        self.signup.send_keys(SignUpLocators.PASSWORD_FIELD, "StrongPass@123")
        self.signup.click(SignUpLocators.CREATE_ACCOUNT_BUTTON)

        try:
            self.assertTrue(
                self.signup.get_browser_validation_message(SignUpLocators.USERNAME_FIELD)
                or self.signup.is_visible(SignUpLocators.ERROR_MESSAGES))
        except Exception:
            raise AssertionError("Short username validation failed")

    # ---------------- LONG USERNAME ----------------
    # def test_Verify_error_for_long_username(self):
    #     self.signup.navigate_to_signup()
    #     self.signup.send_keys(SignUpLocators.USERNAME_FIELD, "a" * 200)
    #     self.signup.send_keys(SignUpLocators.EMAIL_FIELD, "test@test.com")
    #     self.signup.send_keys(SignUpLocators.PASSWORD_FIELD, "StrongPass@123")
    #     self.signup.click(SignUpLocators.CREATE_ACCOUNT_BUTTON)

    #     try:
    #         self.assertTrue(
    #             self.signup.get_browser_validation_message(SignUpLocators.USERNAME_FIELD)
    #             or self.signup.is_visible(SignUpLocators.ERROR_MESSAGES)
    #             or self.signup.get_toast_message())
    #     except Exception:
    #         raise AssertionError("Long username validation failed")

    #  ---------------- SPACES INPUT ----------------
    def test_Verify_signup_with_spaces_input(self):
        self.signup.navigate_to_signup()

        self.signup.send_keys(SignUpLocators.USERNAME_FIELD, "   spaceuser   ")
        self.signup.send_keys(SignUpLocators.EMAIL_FIELD, "   spaceuser@test.com   ")
        self.signup.send_keys(SignUpLocators.PASSWORD_FIELD, "StrongPass@123")
        self.signup.click(SignUpLocators.CREATE_ACCOUNT_BUTTON)

        try:
            self.assertTrue(
                self.signup.is_visible(SignUpLocators.SUCCESS_LOGIN_TEXT)
                or self.signup.is_visible(SignUpLocators.ERROR_MESSAGES)
                or self.signup.get_toast_message())
        except Exception:
            raise AssertionError("Spaces input case not handled properly")

    # ---------------- CLEANUP ----------------
    def tearDown(self):
        self.quit_driver()


if __name__ == "__main__":
    unittest.main()
