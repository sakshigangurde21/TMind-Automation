import os
import unittest
from Base import Base
from Page import AssetPage, LoginPage
from locators import SignUpLocators, AssetLocators
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
        self.asset.click(AssetLocators.ASSETS_MENU)

    # 1 ---------------- OPEN ----------------
    def test_01_open_assets_page(self):
        try:
            self.assertTrue(
                self.asset.is_visible(AssetLocators.ADD_ROOT_BTN))
        except Exception as e:
            raise AssertionError("Unable to open Assets page")

    # 2 ---------------- CREATE ----------------
    def test_02_create_root_asset(self):
        try:
            self.asset.click(AssetLocators.ADD_ROOT_BTN)
            self.asset.send_keys(AssetLocators.ASSET_NAME_INPUT, ASSET_NAME)
            self.asset.click(AssetLocators.ADD_BTN)

            self.assertTrue(
                self.asset.is_visible(AssetLocators.ASSET_NAME_NODE(ASSET_NAME)))
        except Exception:
            raise AssertionError("Unable to create root asset")

    # 3 ---------------- SEARCH ----------------
    def test_03_search_asset(self):
        try:
            self.asset.send_keys(AssetLocators.SEARCH_INPUT, "Auto")
            self.assertTrue(
                self.asset.is_visible(AssetLocators.ASSET_NAME_NODE(ASSET_NAME)))
        except Exception:
            raise AssertionError("Search asset failed")

    # 4 ---------------- PARTIAL SEARCH ----------------
    def test_04_search_partial_match(self):
        try:
            self.asset.send_keys(AssetLocators.SEARCH_INPUT, "Hydraulic")
            self.assertTrue(
                self.asset.is_visible(
                    AssetLocators.ASSET_NAME_NODE("Hydraulic Press")))
        except Exception:
            raise AssertionError("Partial search failed")

    # 5 ---------------- ADD CHILD ----------------
    def test_05_add_child_asset(self):
        try:
            self.asset._hover_asset_row(ASSET_NAME)
            self.driver.execute_script(
                "arguments[0].click();",
                self.asset.get_element(
                    AssetLocators.ADD_CHILD_ICON(ASSET_NAME)))

            self.asset.send_keys(
                AssetLocators.SUB_ASSET_NAME_INPUT, CHILD_ASSET_NAME)
            self.asset.click(AssetLocators.SUB_ASSET_SAVE_BTN)

            self.driver.execute_script(
                "arguments[0].click();",
                self.asset.get_element(
                    AssetLocators.EXPAND_BTN(ASSET_NAME)))

            self.assertTrue(
                self.asset.is_visible(
                    AssetLocators.ASSET_NAME_NODE(CHILD_ASSET_NAME)))
        except Exception:
            raise AssertionError("Unable to add child asset")

    # 6 ---------------- EDIT ----------------
    def test_06_edit_asset(self):
        try:
            self.asset._hover_asset_row(ASSET_NAME)
            self.driver.execute_script(
                "arguments[0].click();",
                self.asset.get_element(
                    AssetLocators.EDIT_ICON(ASSET_NAME)))

            edit_input = self.asset.get_element(AssetLocators.EDIT_INPUT)
            edit_input.clear()
            edit_input.send_keys(UPDATED_NAME)

            self.asset.click(AssetLocators.SAVE_CHANGES_BTN)

            self.assertTrue(
                self.asset.is_visible(
                    AssetLocators.ASSET_NAME_NODE(UPDATED_NAME)))
        except Exception:
            raise AssertionError("Unable to edit asset")

    # 7 ---------------- EMPTY DETAILS ----------------
    def test_07_no_asset_selected_shows_empty_details(self):
        try:
            self.asset.click(AssetLocators.ASSETS_MENU)
            self.assertTrue(
                self.asset.is_visible(
                    AssetLocators.NO_ASSET_SELECTED))
        except Exception:
            raise AssertionError("Empty asset details not shown")

    # 8 ---------------- DETAILS ----------------
    def test_08_asset_details_visible(self):
        try:
            self.asset.click(
                AssetLocators.ASSET_NAME_NODE(UPDATED_NAME))

            asset_type = self.asset.get_element(
                AssetLocators.TYPE_VALUE).text
            asset_level = self.asset.get_element(
                AssetLocators.LEVEL_VALUE).text

            self.assertNotEqual(asset_type, "")
            self.assertNotEqual(asset_level, "")
        except Exception:
            raise AssertionError("Asset details not visible")

    # 9 ---------------- DELETE CHILD ----------------
    def test_09_delete_child_asset(self):
        try:
            self.driver.execute_script(
                "arguments[0].click();",
                self.asset.get_element(
                    AssetLocators.EXPAND_BTN(UPDATED_NAME)))

            self.asset._hover_asset_row(CHILD_ASSET_NAME)
            self.driver.execute_script(
                "arguments[0].click();",
                self.asset.get_element(
                    AssetLocators.DELETE_ICON(CHILD_ASSET_NAME)))

            self.asset.click(AssetLocators.CONFIRM_DELETE_BTN)

            self.assertFalse(
                self.asset.is_visible(
                    AssetLocators.ASSET_NAME_NODE(CHILD_ASSET_NAME)))
        except Exception:
            raise AssertionError("Unable to delete child asset")

    # 10 ---------------- DELETE PARENT ----------------
    def test_10_delete_parent_asset(self):
        try:
            self.asset._hover_asset_row(UPDATED_NAME)
            self.driver.execute_script(
                "arguments[0].click();",
                self.asset.get_element(
                    AssetLocators.DELETE_ICON(UPDATED_NAME)))

            self.asset.click(AssetLocators.CONFIRM_DELETE_BTN)

            self.assertFalse(
                self.asset.is_visible(
                    AssetLocators.ASSET_NAME_NODE(UPDATED_NAME)))
        except Exception:
            raise AssertionError("Unable to delete parent asset")

    # 11 ---------------- DUPLICATE ----------------
    def test_11_duplicate_asset_name(self):
        try:
            self.asset.click(AssetLocators.ADD_ROOT_BTN)
            self.asset.send_keys(
                AssetLocators.ASSET_NAME_INPUT, "Hydraulic Press")
            self.asset.click(AssetLocators.ADD_BTN)

            self.assertTrue(
                self.asset.is_visible(SignUpLocators.INLINE_ERROR))
        except Exception:
            raise AssertionError("Duplicate asset validation failed")

    # 12 ---------------- EMPTY NAME ----------------
    def test_12_empty_asset_name_not_allowed(self):
        try:
            self.asset.click(AssetLocators.ADD_ROOT_BTN)
            self.assertTrue(
                self.asset.is_visible(SignUpLocators.INLINE_ERROR))
        except Exception:
            raise AssertionError("Empty asset name allowed")

    # 13 ---------------- INVALID CHARS ----------------
    def test_13_asset_invalid_characters(self):
        try:
            self.asset.click(AssetLocators.ADD_ROOT_BTN)
            self.asset.send_keys(
                AssetLocators.ASSET_NAME_INPUT, "@@###")

            self.assertTrue(
                self.asset.is_visible(SignUpLocators.INLINE_ERROR))
        except Exception:
            raise AssertionError("Invalid characters accepted")

    # 14 ---------------- TOO LONG ----------------
    def test_14_asset_name_too_long(self):
        try:
            self.asset.click(AssetLocators.ADD_ROOT_BTN)
            self.asset.send_keys(
                AssetLocators.ASSET_NAME_INPUT, "A" * 150)

            self.assertTrue(
                self.asset.is_visible(SignUpLocators.INLINE_ERROR))
        except Exception:
            raise AssertionError("Long asset name accepted")

    # 15 ---------------- DELETE ICON RULES ----------------
    def test_15_delete_icon_rules(self):
        try:
            self.driver.execute_script(
                "arguments[0].click();",
                self.asset.get_element(
                    AssetLocators.EXPAND_BTN("Hydraulic Press")))

            self.assertFalse(
                self.asset.is_visible(
                    AssetLocators.DELETE_ICON("Hydraulic Press")))
            self.assertTrue(
                self.asset.is_visible(
                    AssetLocators.DELETE_ICON("Robotic Arm")))
        except Exception:
            raise AssertionError("Delete icon rule validation failed")

    # 16 ---------------- DEPTH LIMIT ----------------
    def test_16_asset_hierarchy_depth_limit(self):
        try:
            root = "Root_1"
            path = [root]
            current_parent = root
            depth = 1
            max_depth = 5

            self.asset.click(AssetLocators.ADD_ROOT_BTN)
            self.asset.send_keys(
                AssetLocators.ASSET_NAME_INPUT, root)
            self.asset.click(AssetLocators.ADD_BTN)

            while depth < max_depth:
                child_name = f"{current_parent}_Child"

                self.asset.select_asset(current_parent)
                self.asset._hover_asset_row(current_parent)

                self.driver.execute_script(
                    "arguments[0].click();",
                    self.asset.get_element(
                        AssetLocators.ADD_CHILD_ICON(current_parent)))

                self.asset.send_keys(
                    AssetLocators.SUB_ASSET_NAME_INPUT, child_name)
                self.asset.click(AssetLocators.SUB_ASSET_SAVE_BTN)

                self.asset.expand_path(path)

                self.assertTrue(
                    self.asset.is_visible(
                        AssetLocators.ASSET_NAME_NODE(child_name)))

                path.append(child_name)
                current_parent = child_name
                depth += 1

            self.assertFalse(
                self.asset.can_add_child(current_parent))
        except Exception:
            raise AssertionError("Asset hierarchy depth validation failed")

    # ---------------- CLEANUP ----------------
    def tearDown(self):
        self.quit_driver()


if __name__ == "__main__":
    unittest.main()
