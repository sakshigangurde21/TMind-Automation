import os
import time
import unittest
from Base import Base
from Page import LoginPage, SignalPage
from locators import SignalLocators
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

class SignalTests(Base):

    def setUp(self):
        self.driver = super().start_driver()
        # -------- Login --------
        login = LoginPage(self.driver)
        login.enter_email(os.environ.get("USER_EMAIL"))
        login.enter_password(os.environ.get("PASSWORD"))
        login.click_login()
        assert login.is_dashboard_displayed()

        # -------- Open Signal Page --------
        self.signal = SignalPage(self.driver)
        self.signal.open_signal_page()   # assume this navigation method exists

    # ---------------- PAGE LOAD ----------------
    def test_open_signal_page(self):
        """Verify Signal page loads properly"""
        graph_card = self.signal.get_element(SignalLocators.SIGNAL_GRAPH_CARD)
        self.assertTrue(graph_card.is_displayed())

    # ---------------- MAIN ASSET ----------------
    def test_select_main_asset(self):
        """Verify main asset selection works"""
        self.signal.select_main_asset("bullll (Level 3)")
        device = self.signal.get_assigned_device_name()
        self.assertIsNotNone(device)

    # ---------------- ASSIGNED DEVICE ----------------
    def test_asset_without_device_shows_not_assigned(self):
        """Verify asset without device shows 'Not Assigned'"""
        self.signal.select_main_asset("Valve B (Level 3)")
        device = self.signal.get_assigned_device_name()
        self.assertIn("Not Assigned", device)

    # ---------------- SIGNAL VISIBILITY ----------------
    def test_no_device_no_signals(self):
        """Verify no signals shown when no device is assigned"""
        self.signal.select_main_asset("Valve B (Level 3)")
        self.assertTrue(
            self.signal.is_no_signals_displayed(),
            "No signals message should be displayed"
        )

    # ---------------- GRAPH ----------------
    def test_graph_empty_state(self):
        """Verify graph shows empty state when no signals exist"""
        self.signal.select_main_asset("Valve B (Level 3)")
        self.assertTrue(
            self.signal.is_graph_empty(),
            "Graph should show 'No data available'"
        )

    def test_graph_visible_for_asset_with_signals(self):
        """Verify graph is visible when signals exist"""
        self.signal.select_main_asset("bullll (Level 3)")
        self.assertTrue(
            self.signal.is_graph_visible(),
            "Signal graph should be visible"
        )

    # ---------------- COMPARE ASSET ----------------
    def test_select_compare_asset(self):
        """Verify compare asset dropdown works"""
        self.signal.select_main_asset("bullll (Level 3)")
        self.signal.select_compare_asset("charger (Level 4)")
        self.assertTrue(self.signal.is_graph_visible())

    # ---------------- DATA CONSISTENCY ----------------
    def test_device_signal_consistency(self):
        """
        If device is not assigned,
        signals should not be displayed
        """
        self.signal.select_main_asset("Valve B (Level 3)")
        self.signal.verify_device_and_signal_consistency()

    def test_signals_change_when_asset_changes(self):
        self.signal.select_main_asset("bullll (Level 3)")
        signals_1 = self.signal.get_signals_text()

        self.signal.select_main_asset("Auto Welding Line (Level 3)")
        signals_2 = self.signal.get_signals_text()

        self.assertNotEqual(
            signals_1,
            signals_2,
            "Signals did not change after asset switch")

    def tearDown(self):
        self.quit_driver()

if __name__ == "__main__":
    unittest.main()
