import os
import time
import unittest
import glob
import csv
from Base import Base
from Page import LoginPage, DevicePage, ManageUserPage
from locators import ManageUserLocators
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

load_dotenv()

class ManageUserTests(Base):

    def setUp(self):
        self.driver = super().start_driver()

        # Login first
        login = LoginPage(self.driver)
        login.enter_email(os.environ.get("USER_EMAIL"))
        login.enter_password(os.environ.get("PASSWORD"))
        login.click_login()
        assert login.is_dashboard_displayed()

        self.device = DevicePage(self.driver)

        # Open Manage User page
        self.manage_user = ManageUserPage(self.driver)
        self.manage_user.go_to_manage_user()

    # ---------------- NAVIGATION ----------------
    def test_open_manage_user_page(self):
        header = self.manage_user.get_element(ManageUserLocators.PAGE_HEADER)
        self.assertTrue(header.is_displayed())
        self.assertIn("User Management", header.text.strip())

    # ---------------- SEARCH ----------------
    def test_search_existing_user(self):
        username = "sakshi"
        self.manage_user.search_user(username)
        rows = self.manage_user.get_all_user_rows()
        self.assertEqual(len(rows), 1)
        self.assertEqual(
            rows[0].find_element("xpath", ManageUserLocators.USERNAME_CELL).text.strip(),
            username
        )

    def test_search_non_existing_user(self):
        self.manage_user.search_user("randomuser123")
        rows = self.manage_user.get_all_user_rows()
        self.assertEqual(len(rows), 0)  # Will pass if "No users found" row is ignored

    # ---------------- ROLE CHANGE ----------------
    def test_change_user_role(self):
        username = "exuser"   # Make sure this user always exists
        new_role = "Engineer"
        print("Users in table:", self.manage_user.get_all_usernames())
    # Step 1: Get the row of the user
        row = self.manage_user.get_user_row_by_username(username)
        self.assertIsNotNone(row, f"User '{username}' not found")
    # Step 2: Change the user role
        self.manage_user.change_user_role(row, new_role)
    # Step 3: Verify success toast (instead of checking table)
        self.device.verify_toast_success("User role updated!")

    # ---------------- DELETE USER ----------------
    def test_delete_user_cancel(self):
        username = "sakshi"
        print("All users:", self.manage_user.get_all_usernames())   # 👈 ADD HERE
        self.manage_user.click_delete_user(username)
        self.manage_user.cancel_delete()
        self.assertTrue(self.manage_user.is_user_in_table(username))

    def test_delete_user_confirm(self):
        username = "anu"
        print("All users:", self.manage_user.get_all_usernames())   # 👈 ADD HERE
        self.assertTrue(self.manage_user.is_user_in_table(username))
        self.manage_user.click_delete_user(username)
        self.manage_user.confirm_delete()
        self.assertFalse(self.manage_user.is_user_in_table(username))

    # ---------------- CSV DOWNLOAD ----------------
    def test_download_csv(self):
        self.manage_user.download_csv()

    def test_download_csv_verification(self):
    # Trigger CSV download
        self.manage_user.download_csv()

    # Folder where CSV is downloaded
        download_folder = os.path.join(os.getcwd(), "Downloads")  # project Downloads folder
        os.makedirs(download_folder, exist_ok=True)

    # Wait for the file to appear (up to 10 seconds)
        timeout = 10
        for _ in range(timeout):
            files = glob.glob(os.path.join(download_folder, "users*.csv"))
            if files:
                latest_file = max(files, key=os.path.getctime)
                break
            time.sleep(1)
        else:
            raise AssertionError("CSV file was not downloaded")

        print("Downloaded CSV:", latest_file)


    # ---------------- Pagination Tests ----------------
    def test_pagination_next_previous(self):
        """Verify Next and Previous buttons navigate pages correctly"""
        initial_page = self.manage_user.get_current_page_number()
    
    # Click Next (if more than 1 page exists)
        pages = self.manage_user.get_all_page_numbers()
        if len(pages) > 1:
            self.manage_user.click_next_page()
            next_page = self.manage_user.get_current_page_number()
            self.assertEqual(next_page, initial_page + 1, "Next page navigation failed")
        
        # Click Previous to go back
            self.manage_user.click_previous_page()
            prev_page = self.manage_user.get_current_page_number()
            self.assertEqual(prev_page, initial_page, "Previous page navigation failed")
        else:
            print("Only 1 page exists, skipping Next/Previous test")

    def test_go_to_specific_page(self):
        """Verify navigation to a specific page number"""
        pages = self.manage_user.get_all_page_numbers()
        if len(pages) > 1:
            target_page = pages[-1]  # go to last page
            self.manage_user.go_to_page(target_page)
            current_page = self.manage_user.get_current_page_number()
            self.assertEqual(current_page, target_page, f"Failed to navigate to page {target_page}")
        else:
            print("Only 1 page exists, skipping specific page navigation")

    def test_pagination_buttons_disabled_on_first_last_page(self):
        """Verify Prev is disabled on first page and Next is disabled on last page"""

        pages = self.manage_user.get_all_page_numbers()

        if len(pages) <= 1:
            print("Only 1 page — skipping pagination button disable test")
            return

    # Go to FIRST page
        self.manage_user.go_to_page(1)
        prev_btn = self.manage_user.get_element(ManageUserLocators.PREVIOUS_PAGE_BUTTON)
        self.assertEqual(prev_btn.value_of_css_property("pointer-events"), "none", "Prev button should be visually disabled on first page")
    # Go to LAST page
        last_page = pages[-1]
        self.manage_user.go_to_page(last_page)
        next_btn = self.manage_user.get_element(ManageUserLocators.NEXT_PAGE_BUTTON)
        self.assertEqual(next_btn.value_of_css_property("pointer-events"), "none", "Next button should be visually disabled on last page")
    
    def test_search_filters_by_username_only(self):
        """Ensure search matches only the username column"""

        query = "admin"
        self.manage_user.search_user(query)

        rows = self.manage_user.get_all_user_rows()

    # If no rows, skip (depends on environment data)
        if len(rows) == 0:
            self.fail("Search returned no rows — cannot validate search behavior")

        for row in rows:
            username = row.find_element(By.XPATH, ManageUserLocators.USERNAME_CELL).text.lower()
            self.assertIn(query, username, f"Search should match ONLY username, found: {username}")

    def test_csv_download_shows_toast(self):
        """Verify CSV download triggers success toast"""
        time.sleep(5)
        self.manage_user.download_csv()
        time.sleep(1)
        self.device.verify_toast_success("CSV downloaded successfully!")


    def tearDown(self):
        self.quit_driver()


if __name__ == "__main__":
    unittest.main()
