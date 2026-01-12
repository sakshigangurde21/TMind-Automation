import os
import time
import allure
import unittest
from Base import Base
from Page import LoginPage, DevicePage, ManageUserPage
from locators import ManageUserLocators
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Manage User")
class ManageUserTests(Base):

    @classmethod
    def setUpClass(cls):
        cls.driver = cls.start_driver()

        login = LoginPage(cls.driver)
        login.enter_email(os.environ.get("USER_EMAIL"))
        login.enter_password(os.environ.get("PASSWORD"))
        login.click_login()

        assert login.is_dashboard_displayed(), "Login failed"

        cls.device = DevicePage(cls.driver)
        cls.manage_user = ManageUserPage(cls.driver)
        cls.manage_user.go_to_manage_user()

    def setUp(self):
        # ---- REUSE SESSION ----
        self.driver = self.__class__.driver
        self.device = self.__class__.device
        self.manage_user = self.__class__.manage_user

    # ------------------------------------------------
    # PAGE LOAD
    # ------------------------------------------------
    @allure.title("Verify Manage User page opens successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_01_verify_manage_user_page_open(self):
        try:
            header = self.manage_user.get_element(ManageUserLocators.PAGE_HEADER)
            assert header.is_displayed()
            assert "User Management" in header.text
        except AssertionError:
            self.attach_screenshot("manage_user_page_failure")
            raise

    # ------------------------------------------------
    # SEARCH
    # ------------------------------------------------
    @allure.title("Verify search for existing user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_02_search_existing_user(self):
        username = "Sakshi"

        try:
            self.manage_user.search_user(username)
            rows = self.manage_user.get_all_user_rows()

            assert len(rows) == 1
            actual_username = rows[0].find_element(
                By.XPATH, ManageUserLocators.USERNAME_CELL
            ).text.strip()

            assert actual_username == username
        except AssertionError:
            self.attach_screenshot("search_existing_user_failure")
            raise

    @allure.title("Verify search for non-existing user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_03_search_non_existing_user(self):
        try:
            self.manage_user.search_user("random_user_123")
            rows = self.manage_user.get_all_user_rows()
            assert len(rows) == 0
        except AssertionError:
            self.attach_screenshot("search_non_existing_user_failure")
            raise

    # ------------------------------------------------
    # ROLE CHANGE
    # ------------------------------------------------
    @allure.title("Verify admin can change user role")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_04_change_user_role(self):
        username = "exuser"
        new_role = "Engineer"
        self.manage_user.reset_search()
        try:
            row = self.manage_user.get_user_row_by_username(username)
            assert row is not None, f"User {username} not found"

            self.manage_user.change_user_role(row, new_role)
            self.device.verify_toast_success("User role updated successfully")
        except AssertionError:
            self.attach_screenshot("change_role_failure")
            raise

    # ------------------------------------------------
    # DELETE USER
    # ------------------------------------------------
    @allure.title("Verify delete user cancel flow")
    @allure.severity(allure.severity_level.NORMAL)
    def test_05_delete_user_cancel(self):
        username = "Tom"

        try:
            self.manage_user.click_delete_user(username)
            self.manage_user.cancel_delete()
            assert self.manage_user.is_user_in_table(username)
        except AssertionError:
            self.attach_screenshot("delete_cancel_failure")
            raise



    # @allure.title("Verify delete user confirm flow")
    # @allure.severity(allure.severity_level.CRITICAL)
    # def test_06_delete_user_confirm(self):
    #     username = "Tom"

    #     try:
    #     # Step 0: Ensure user exists
    #         assert self.manage_user.is_user_in_table(username), f"User '{username}' not in table"

    #     # Step 1: Click delete icon
    #         self.manage_user.click_delete_user(username)

    #     # Step 2: Wait for confirm button to be visible and clickable
    #         button = WebDriverWait(self.driver, 10).until(
    #         EC.visibility_of_element_located(ManageUserLocators.DELETE_MODAL_CONFIRM_BUTTON)
    #     )
    #         WebDriverWait(self.driver, 10).until(
    #         EC.element_to_be_clickable(ManageUserLocators.DELETE_MODAL_CONFIRM_BUTTON)
    #     )

    #     # Step 2.5: Scroll button into view (prevents overlay issues)
    #         self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)

    #     # Step 3: Click confirm button
    #         self.manage_user.click(ManageUserLocators.DELETE_MODAL_CONFIRM_BUTTON)

    #     # Step 4: Wait until user is removed from table
    #         WebDriverWait(self.driver, 10).until(
    #         lambda d: not self.manage_user.is_user_in_table(username)
    #     )

    #     # Final assertion
    #         assert not self.manage_user.is_user_in_table(username), "User was not deleted"

    #     except AssertionError:
    #         self.attach_screenshot("delete_confirm_failure")
    #         raise


    # ------------------------------------------------
    # CSV DOWNLOAD
    # ------------------------------------------------
    @allure.title("Verify CSV download shows success toast")
    @allure.severity(allure.severity_level.NORMAL)
    def test_07_csv_download_toast(self):
        try:
            self.manage_user.download_csv()
            self.device.verify_toast_success("CSV downloaded successfully!")
        except AssertionError:
            self.attach_screenshot("csv_download_failure")
            raise

    # ------------------------------------------------
    # PAGINATION
    # ------------------------------------------------
    @allure.title("Verify pagination Next and Previous buttons")
    @allure.severity(allure.severity_level.NORMAL)
    def test_08_pagination_next_previous(self):
        try:
            pages = self.manage_user.get_all_page_numbers()
            if len(pages) <= 1:
                allure.attach("Only one page present", name="Pagination Skip")
                return

            initial_page = self.manage_user.get_current_page_number()
            self.manage_user.click_next_page()
            assert self.manage_user.get_current_page_number() == initial_page + 1

            self.manage_user.click_previous_page()
            assert self.manage_user.get_current_page_number() == initial_page
        except AssertionError:
            self.attach_screenshot("pagination_next_prev_failure")
            raise

    @allure.title("Verify Prev disabled on first page and Next disabled on last page")
    @allure.severity(allure.severity_level.MINOR)
    def test_09_pagination_button_disabled_states(self):
        try:
            pages = self.manage_user.get_all_page_numbers()
            if len(pages) <= 1:
                return

            self.manage_user.go_to_page(1)
            prev_btn = self.manage_user.get_element(
                ManageUserLocators.PREVIOUS_PAGE_BUTTON
            )
            assert prev_btn.value_of_css_property("pointer-events") == "none"

            self.manage_user.go_to_page(pages[-1])
            next_btn = self.manage_user.get_element(
                ManageUserLocators.NEXT_PAGE_BUTTON
            )
            assert next_btn.value_of_css_property("pointer-events") == "none"
        except AssertionError:
            self.attach_screenshot("pagination_disabled_failure")
            raise

    # ------------------------------------------------
    # SEARCH FILTER VALIDATION
    # ------------------------------------------------
    @allure.title("Verify search filters only by username column")
    @allure.severity(allure.severity_level.NORMAL)
    def test_10_search_filters_by_username_only(self):
        query = "admin"

        try:
            self.manage_user.search_user(query)
            rows = self.manage_user.get_all_user_rows()

            assert len(rows) > 0

            for row in rows:
                username = row.find_element(
                    By.XPATH, ManageUserLocators.USERNAME_CELL
                ).text.lower()
                assert query in username
        except AssertionError:
            self.attach_screenshot("search_filter_failure")
            raise

    @classmethod
    def tearDownClass(cls):
        cls.quit_driver()
