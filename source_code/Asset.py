import os
import unittest
from Base import Base
from Page import AssetPage
from Page import LoginPage
from locators import SignUpLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

ASSET_NAME = "Auto_Root_01"
UPDATED_NAME = "Auto_Root_01_Updated"
CHILD_ASSET_NAME = "Auto_Child_01"


class AssetsTests(Base):

    def setUp(self):
        self.driver = super().start_driver()

        login = LoginPage(self.driver)
        login.enter_email(os.environ.get("USER_EMAIL"))
        login.enter_password(os.environ.get("PASSWORD"))
        login.click_login()
        assert login.is_dashboard_displayed()

        self.asset = AssetPage(self.driver)
        self.asset.open_assets()

    def test_open_assets_page(self):
        self.assertTrue(True)

    # ---------------- CREATE ----------------

    def test_create_root_asset(self):
        self.asset.click_add_root()
        self.asset.create_asset(ASSET_NAME)
        self.asset.select_asset(ASSET_NAME)

        self.asset.verify_asset_visible(ASSET_NAME)

    # ---------------- SEARCH ----------------

    def test_search_asset(self):
        self.asset.search_asset("Auto")

    def test_search_partial_match(self):
        self.asset.search_asset("Paint")
        self.asset.verify_asset_visible("PaintBoothPLC_01")

    # ---------------- CHILD ----------------

    def test_add_child_asset(self):
        self.asset.add_child_asset(ASSET_NAME, CHILD_ASSET_NAME)
        self.asset.expand_asset(ASSET_NAME)
        self.asset.verify_asset_visible(CHILD_ASSET_NAME)

    # ---------------- UPDATE ----------------

    def test_edit_asset(self):
        self.asset.edit_asset(ASSET_NAME, UPDATED_NAME)
        self.asset.verify_asset_visible(UPDATED_NAME)

    # ---------------- DETAILS ----------------

    def test_no_asset_selected_shows_empty_details(self):
        self.asset.open_assets()

        displayed = self.asset.is_no_asset_selected_displayed()
        self.assertTrue(displayed, "'No Asset Selected' message not visible")

        self.asset.verify_no_asset_selected_details_empty()

    def test_asset_details_visible(self):
        self.asset.select_asset(UPDATED_NAME)

        asset_type = self.asset.get_asset_type()
        asset_level = self.asset.get_asset_level()
        sub_assets = self.asset.get_sub_assets()

        print(f"Asset Type: {asset_type}")
        print(f"Asset Level: {asset_level}")
        print(f"Sub Assets: {sub_assets}")

        self.assertNotEqual(asset_type, "", "Asset Type empty")
        self.assertNotEqual(asset_level, "", "Asset Level empty")

    # ---------------- DELETE ----------------

    def test_delete_child_asset(self):
        self.asset.expand_asset(UPDATED_NAME)
        self.asset.delete_asset(CHILD_ASSET_NAME)

    def test_delete_parent_asset(self):
        self.asset.delete_asset(UPDATED_NAME)

    # ---------------- VALIDATION ----------------

    def test_duplicate_asset_name(self):
        self.asset.click_add_root()
        self.asset.create_asset("Factory")     # already exists

        self.asset.verify_toast_error(
            SignUpLocators.TOAST_ERROR,
            "Asset name already exists")

    def test_empty_asset_name_not_allowed(self):
        self.asset.click_add_root()

        self.asset.verify_inline_error(
            SignUpLocators.INLINE_ERROR)

    def test_asset_invalid_characters(self):
        self.asset.click_add_root()
        self.asset.enter_asset_name("@@###")

        self.asset.verify_inline_error(
            SignUpLocators.INLINE_ERROR
        )

    def test_asset_name_too_long(self):
        self.asset.click_add_root()
        self.asset.enter_asset_name("A" * 150)

        self.asset.verify_inline_error(
            SignUpLocators.INLINE_ERROR
        )

    # ---------------- ICON RULES ----------------

    def test_delete_icon_rules(self):
        self.asset.expand_asset("Factory")

        self.asset.verify_delete_icon_hidden("Factory")
        self.asset.verify_delete_icon_visible("workers")

    # ---------------- HIERARCHY ----------------

    def test_asset_hierarchy_depth_limit(self):
        root = "Root_1"

        self.asset.click_add_root()
        self.asset.create_asset(root)

        current_parent = root
        depth = 1
        max_depth = 5

        while depth < max_depth:
            child_name = f"{current_parent}_Child"

            self.asset.select_asset(current_parent)
            self.asset.add_child_asset(current_parent, child_name)
            self.asset.verify_asset_visible(child_name)
            self.asset.expand_asset(current_parent)

            current_parent = child_name
            depth += 1

            if depth < max_depth:
                self.assertTrue(
                    self.asset.can_add_child(current_parent),
                    f"Add child must exist at depth {depth}"
                )

        self.assertFalse(
            self.asset.can_add_child(current_parent),
            "Add child must NOT exist after max depth"
        )

    # ---------------- CLEANUP ----------------

    def tearDown(self):
        self.quit_driver()


if __name__ == "__main__":
    unittest.main()
