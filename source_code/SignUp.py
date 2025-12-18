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
        """Initialize driver and SignUpPage"""
        self.driver = super().start_driver()
        self.signup = SignUpPage(self.driver)

    def test_signup_success(self):
        self.signup.navigate_to_signup()

        self.signup.enter_username("newuser123")
        self.signup.enter_email("new123@test.com")
        self.signup.enter_password("StrongPass@123")
        self.signup.click_create_account()

        WebDriverWait(self.driver, 10).until(
            lambda d: self.signup.is_signup_successful())

        self.assertTrue(self.signup.is_signup_successful(), "Signup should succeed for valid inputs")

    def test_signup_empty_fields(self):
        self.signup.navigate_to_signup()
        self.signup.click_create_account()

        toast = self.signup.get_toast_error()
        validation = self.signup.get_validation_message()
        has_error = self.signup.is_error_displayed()

        self.assertTrue(has_error or toast or validation, "Error should be displayed for empty fields")

    def test_signup_invalid_email(self):
        self.signup.navigate_to_signup()

        self.signup.enter_username("dummyuser")
        self.signup.enter_email("invalidemail")
        self.signup.enter_password("Strong@123")
        self.signup.click_create_account()

        toast = self.signup.get_toast_error()
        validation = self.signup.get_validation_message()

        self.assertTrue(self.signup.is_error_displayed() or toast or validation, "Invalid email should trigger validation error")

    def test_signup_weak_password(self):
        self.signup.navigate_to_signup()

        self.signup.enter_username("user1")
        self.signup.enter_email("user1@test.com")
        self.signup.enter_password("1234")
        self.signup.click_create_account()

        toast = self.signup.get_toast_error()
        validation = self.signup.get_validation_message()

        self.assertTrue(self.signup.is_error_displayed() or toast or validation, "Weak password should show error")

    def test_signup_existing_email(self):
        self.signup.navigate_to_signup()

        self.signup.enter_username("exuser")
        self.signup.enter_email("newuser123@test.com")
        self.signup.enter_password("StrongPass@123")
        self.signup.click_create_account()

        toast = self.signup.get_toast_error()

        self.assertTrue(toast or self.signup.is_error_displayed(), "Existing email should show error")

    def test_signup_short_username(self):
        self.signup.navigate_to_signup()

        self.signup.enter_username("a")
        self.signup.enter_email("test@test.com")
        self.signup.enter_password("StrongPass@123")
        self.signup.click_create_account()

        validation = self.signup.get_validation_message()
        self.assertTrue(validation or self.signup.is_error_displayed(), "Short username should be rejected")

    def test_signup_long_username(self):
        self.signup.navigate_to_signup()

        self.signup.enter_username("a" * 200)
        self.signup.enter_email("test@test.com")
        self.signup.enter_password("StrongPass@123")
        self.signup.click_create_account()

        validation = self.signup.get_validation_message()
        self.assertTrue(validation or self.signup.is_error_displayed(), "Over-length username should fail")

    def test_signup_spaces_input(self):
        self.signup.navigate_to_signup()

        self.signup.enter_username("   spaceuser   ")
        self.signup.enter_email("   spaceuser@test.com   ")
        self.signup.enter_password("StrongPass@123")
        self.signup.click_create_account()

        success = self.signup.is_signup_successful()
        error = self.signup.is_error_displayed()

        print("Signup success:", success)
        print("Signup error:", error)

        self.assertTrue(success or error, "Spaces case should either succeed or throw error")

    def tearDown(self):
        self.quit_driver()

if __name__ == "__main__":
    unittest.main()
