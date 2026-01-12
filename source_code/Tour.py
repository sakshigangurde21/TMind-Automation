import os
import unittest
import allure
from Base import Base
from Page import LoginPage, TourPage
from locators import TourLocators
from dotenv import load_dotenv

load_dotenv()

@allure.epic("User Onboarding")
@allure.feature("Application Tour")
class TourTests(Base):

    def setUp(self):
        self.driver = super().start_driver()

        self.login = LoginPage(self.driver)
        self.login.enter_email(os.environ.get("USER_EMAIL"))
        self.login.enter_password(os.environ.get("PASSWORD"))
        self.login.click_login()
        assert self.login.is_dashboard_displayed()

        self.tour = TourPage(self.driver)

    # ---------------- NAVIGATION ----------------
    @allure.title("Verify Start Tour button visibility")
    @allure.severity(allure.severity_level.NORMAL)
    def test_start_tour_button_visible(self):
        try:
            start_btn = self.driver.find_element(*TourLocators.START_TOUR_BTN)
            assert start_btn.is_displayed(), "Start Tour button not visible"
        except AssertionError:
            self.attach_screenshot("_start_tour_btn_failure")
            raise

    @allure.title("Verify Start Tour launches popover")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_start_tour(self):
        try:
            self.tour.start_tour()
            assert self.tour.is_popover_visible(), "Popover did not appear"
            title = self.tour.get_popover_title()
            assert len(title) > 0, "Popover title is empty"
        except AssertionError:
            self.attach_screenshot("_start_tour_failure")
            raise

    # ---------------- POPUP NAVIGATION ----------------
    @allure.title("Verify Next and Previous buttons in tour")
    @allure.severity(allure.severity_level.NORMAL)
    def test_next_prev_buttons(self):
        try:
            self.tour.start_tour()
            first_title = self.tour.get_popover_title()

            self.tour.click_next()
            second_title = self.tour.get_popover_title()
            assert first_title != second_title, "Next button failed"

            self.tour.click_prev()
            back_title = self.tour.get_popover_title()
            assert first_title == back_title, "Prev button failed"
        except AssertionError:
            self.attach_screenshot("_next_prev_failure")
            raise

    @allure.title("Verify tour can be closed")
    @allure.severity(allure.severity_level.NORMAL)
    def test_close_tour(self):
        try:
            self.tour.start_tour()
            self.tour.close_tour()
            assert not self.tour.is_popover_visible(), "Tour did not close"
        except AssertionError:
            self.attach_screenshot("_close_tour_failure")
            raise

    # ---------------- FULL TOUR FLOW ----------------
    @allure.title("Verify complete tour flow")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_complete_tour(self):
        try:
            self.tour.complete_tour()
            assert not self.tour.is_popover_visible(), "Tour not completed properly"
        except AssertionError:
            self.attach_screenshot("_complete_tour_failure")
            raise

    # ---------------- VALIDATIONS ----------------
    # @allure.title("Verify tour popover title & description")
    # @allure.severity(allure.severity_level.MINOR)
    # def test_popover_title_description_not_empty(self):
    #     try:
    #         self.tour.start_tour()
    #         while self.tour.is_popover_visible():
    #             title = self.tour.get_popover_title()
    #             desc = self.tour.get_popover_description()
    #             assert len(title) > 0, "Popover title empty"
    #             assert len(desc) > 0, "Popover description empty"
    #             try:
    #                 self.tour.click_next()
    #             except:
    #                 break
    #         self.tour.close_tour()
    #     except AssertionError:
    #         self.attach_screenshot("_popover_validation_failure")
    #         raise

    # ---------------- CLEANUP ----------------
    def tearDown(self):
        self.quit_driver()

