import os
import unittest
import allure
import time
from Base import Base
from Page import LoginPage, AssetPage, SignalPage
from locators import SignalLocators
from dotenv import load_dotenv
from selenium.webdriver.support.ui import Select

load_dotenv()

class SignalTests(Base):

    @classmethod
    def setUpClass(cls):
        cls.driver = super().start_driver()

        login = LoginPage(cls.driver)
        login.enter_email(os.environ.get("USER_EMAIL"))
        login.enter_password(os.environ.get("PASSWORD"))
        login.click_login()
        assert login.is_dashboard_displayed(), "Login failed"
        cls.signal = SignalPage(cls.driver)
        # ---------- OPEN SIGNAL MODULE ----------
        cls.signal.click(SignalLocators.SIGNAL_MENU)
    # 1 ---------------- OPEN ----------------
    @allure.title("Verify Signal module opens successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_01_open_signal_module(self):
        try:
            assert self.signal.is_visible(SignalLocators.TIME_RANGE_DROPDOWN)
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Signal module did not open")

    # 2 ---------------- TIME RANGE ----------------
    @allure.title("Verify Time Range dropdown is visible and enabled")
    @allure.severity(allure.severity_level.NORMAL)
    def test_02_time_range_dropdown_enabled(self):
        try:
            dropdown = self.signal.get_element(
                SignalLocators.TIME_RANGE_DROPDOWN
            )
            time.sleep(1)
            assert dropdown.is_displayed(), "Time Range dropdown not visible"
            assert dropdown.is_enabled(), "Time Range dropdown disabled"
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Time Range dropdown validation failed")
        
# 8 ---------------- TIME RANGE SELECTION ----------------
    @allure.title("Verify user can select Time Range value")
    @allure.severity(allure.severity_level.NORMAL)
    def test_03_select_time_range_value(self):
        try:
            dropdown_element = self.signal.get_element(
            SignalLocators.TIME_RANGE_DROPDOWN
        )

            select = Select(dropdown_element)
            select.select_by_value("7d")  # Last 7 Days

            time.sleep(1)

            selected_option = select.first_selected_option.text
            assert selected_option == "Last 7 Days", \
            f"Expected 'Last 7 Days' but got '{selected_option}'"

        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Time Range selection failed")

    # 3 ---------------- MAIN ASSET ----------------
    @allure.title("Verify Main Asset dropdown is clickable")
    @allure.severity(allure.severity_level.NORMAL)
    def test_04_main_asset_dropdown_clickable(self):
        try:
            asset_dropdown = self.signal.get_element(
                SignalLocators.MAIN_ASSET_DROPDOWN
            )
            asset_dropdown.click()
            time.sleep(1)
            assert asset_dropdown.is_enabled(), "Main Asset dropdown disabled"
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Main Asset dropdown not clickable")

    # 4 ---------------- SIGNAL BUTTON ----------------
    @allure.title("Verify Signals button is disabled by default")
    @allure.severity(allure.severity_level.NORMAL)
    def test_05_signals_button_disabled_by_default(self):
        try:
            signals_btn = self.signal.get_element(
                SignalLocators.SIGNALS_BUTTON
            )
            time.sleep(1)
            assert not signals_btn.is_enabled(), \
                "Signals button should be disabled initially"
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Signals button state validation failed")

    # 5 ---------------- ASSIGNED DEVICE ----------------
    @allure.title("Verify Assigned Device shows Not Assigned")
    @allure.severity(allure.severity_level.NORMAL)
    def test_06_assigned_device_not_assigned(self):
        try:
            device_text = self.signal.get_text(
                SignalLocators.ASSIGNED_DEVICE_VALUE
            )
            time.sleep(1)
            assert "Not Assigned" in device_text, \
                "Assigned device text incorrect"
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Assigned Device validation failed")

    # 6 ---------------- COMPARE ASSET ----------------
    @allure.title("Verify Compare Asset dropdown is disabled initially")
    @allure.severity(allure.severity_level.NORMAL)
    def test_07_compare_asset_dropdown_disabled(self):
        try:
            compare_dropdown = self.signal.get_element(
                SignalLocators.COMPARE_ASSET_DROPDOWN
            )
            assert not compare_dropdown.is_enabled(), \
                "Compare Asset dropdown should be disabled"
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Compare Asset dropdown validation failed")

    # 7 ---------------- GRAPH EMPTY STATE ----------------
    @allure.title("Verify No data available message shown in Signals Graph")
    @allure.severity(allure.severity_level.NORMAL)
    def test_08_no_data_message_in_graph(self):
        try:
            no_data_text = self.signal.get_text(
                SignalLocators.GRAPH_NO_DATA_TEXT
            )
            assert "No data available" in no_data_text, \
                "No data message not displayed"
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Signals graph empty state validation failed")

    # ---------------- CLEANUP ----------------
    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
