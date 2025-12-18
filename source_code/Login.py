import os
import time
import unittest
from Base import Base
from Page import LoginPage
from locators import LoginLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

class LoginTests(Base):
    def setUp(self):
        """Initialize driver and LoginPage"""
        self.driver = super().start_driver()
        self.login = LoginPage(self.driver)

    def test_positive_login(self):
        """Verify user can login with valid credentials"""
        self.login.enter_email(os.environ.get("USER_EMAIL"))
        self.login.enter_password(os.environ.get("PASSWORD"))
        self.login.click_login()

        # Wait for dashboard
        WebDriverWait(self.driver, 10).until(
            lambda d: self.login.is_dashboard_displayed()
        )
        self.assertTrue(self.login.is_dashboard_displayed())

    def test_negative_login(self):
        """Verify error messages appear for invalid login"""
        test_data = [
            ("invalid@example.com", "wrongpass"),
            ("invalid-email", "Test1234")
        ]
        for email, password in test_data:
            self.login.clear_login_fields()
            self.login.enter_email(email)
            self.login.enter_password(password)
            self.login.click_login()

            toast_msg = self.login.get_toast_message()
            has_error = self.login.is_error_displayed()
            browser_msg = self.login.get_browser_validation_message(LoginLocators.EMAIL_INPUT)

            print(f"\nTest case: {email}")
            print(f"Inline error: {has_error}")
            print(f"Toast message: {toast_msg}")
            print(f"Browser validation: {browser_msg}")

            self.assertTrue(
                has_error or (toast_msg not in [None, ""]) or (browser_msg not in [None, ""]),
                f"No error detected for {email}. Error={has_error}, Toast={toast_msg}, Browser={browser_msg}")

    def test_login_with_empty_password(self):
        self.login.clear_login_fields()
        self.login.enter_email("test@example.com")
        self.login.enter_password("")
        self.login.click_login()

        self.assertTrue(self.login.is_error_displayed() or self.login.get_error_messages())

    def test_login_with_empty_email(self):
        self.login.clear_login_fields()
        self.login.enter_email("")
        self.login.enter_password("Test1234")
        self.login.click_login()

        self.assertTrue(self.login.is_error_displayed() or self.login.get_error_messages())

    def test_login_with_both_fields_empty(self):
        self.login.clear_login_fields()
        self.login.click_login()

        self.assertTrue(self.login.is_error_displayed() or self.login.get_error_messages())

    def test_login_with_short_password(self):
        self.login.clear_login_fields()
        self.login.enter_email("test@example.com")
        self.login.enter_password("123")
        self.login.click_login()

        toast_message = self.login.get_toast_message()
        print("Toast:", toast_message)
        self.assertIn("Invalid email or password", toast_message)

    def test_logout_functionality(self):
        self.login.enter_email(os.environ.get("USER_EMAIL"))
        self.login.enter_password(os.environ.get("PASSWORD"))
        self.login.click_login()

        self.login.wait_for_toast_to_disappear()
        self.login.click_profile_icon()
        self.login.click_logout()

        # Wait for login button to appear
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(LoginLocators.LOGIN_BUTTON))
        self.assertTrue(self.driver.find_element(*LoginLocators.LOGIN_BUTTON).is_displayed())

    def test_back_button_after_login(self):
        self.login.enter_email(os.environ.get("USER_EMAIL"))
        self.login.enter_password(os.environ.get("PASSWORD"))
        self.login.click_login()

        self.login.wait_for_toast_to_disappear()
        self.login.click_profile_icon()  # Ensure dashboard loaded

        self.driver.back()            # Press browser back button

        profile_visible = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(LoginLocators.PROFILE_ICON))
        self.assertTrue(profile_visible.is_displayed())

    def tearDown(self):
        """Quit driver after each test"""
        self.quit_driver()

if __name__ == "__main__":
    unittest.main()
