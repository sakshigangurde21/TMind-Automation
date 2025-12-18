import os
import unittest
from Base import Base
from Page import LoginPage, TourPage
from locators import TourLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

class TourTests(Base):
    def setUp(self):
        self.driver = super().start_driver()
        login = LoginPage(self.driver)
        login.enter_email(os.environ.get("USER_EMAIL"))
        login.enter_password(os.environ.get("PASSWORD"))
        login.click_login()
        assert login.is_dashboard_displayed()

        self.tour = TourPage(self.driver)

    # ---------------- NAVIGATION ----------------
    def test_start_tour_button_visible(self):
        """Check that 'Start Tour' button is visible on a card"""
        start_btn = self.driver.find_element(*TourLocators.START_TOUR_BTN)
        self.assertTrue(start_btn.is_displayed(), "Start Tour button not visible")

    def test_start_tour(self):
        """Click Start Tour and verify first popover appears"""
        self.tour.start_tour()
        self.assertTrue(self.tour.is_popover_visible(), "Popover did not appear after starting tour")
        title = self.tour.get_popover_title()
        self.assertTrue(len(title) > 0, "Popover title is empty")

    # ---------------- POPUP NAVIGATION ----------------
    def test_next_prev_buttons(self):
        """Navigate forward and backward in the tour"""
        self.tour.start_tour()
        first_title = self.tour.get_popover_title()
        
        self.tour.click_next()
        second_title = self.tour.get_popover_title()
        self.assertNotEqual(first_title, second_title, "Next button did not change popover")

        self.tour.click_prev()
        back_title = self.tour.get_popover_title()
        self.assertEqual(first_title, back_title, "Prev button did not return to first popover")

    def test_close_tour(self):
        """Close the tour using the close button"""
        self.tour.start_tour()
        self.tour.close_tour()
        self.assertFalse(self.tour.is_popover_visible(), "Popover still visible after closing tour")

    # ---------------- FULL TOUR FLOW ----------------
    def test_complete_tour(self):
        """Iterate through all tour steps automatically and close"""
        self.tour.complete_tour()
        self.assertFalse(self.tour.is_popover_visible(), "Popover still visible after completing tour")

    # ---------------- VALIDATIONS ----------------
    def test_popover_title_description_not_empty(self):
        """Verify that each popover has title and description"""
        self.tour.start_tour()
        while self.tour.is_popover_visible():
            title = self.tour.get_popover_title()
            desc = self.tour.get_popover_description()
            self.assertTrue(len(title) > 0, "Popover title is empty")
            self.assertTrue(len(desc) > 0, "Popover description is empty")
            try:
                self.tour.click_next()
            except:
                break
        self.tour.close_tour()

    # ---------------- CLEANUP ----------------
    def tearDown(self):
        self.quit_driver()


if __name__ == "__main__":
    unittest.main()
