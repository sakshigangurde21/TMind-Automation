import os
import unittest
import allure
from Base import Base
from Page import AssetPage, LoginPage, DevicePage
from locators import SignUpLocators, AssetLocators
from dotenv import load_dotenv
import time

load_dotenv()

ASSET_NAME = "Auto_Root_01"
UPDATED_NAME = "Auto_Root_01_Updated"
CHILD_ASSET_NAME = "Auto_Child_01"

class AssetsTests(Base):
    @classmethod
    def setUpClass(cls):
        cls.driver = super().start_driver()

        login = LoginPage(cls.driver)
    
        login.enter_email(os.environ.get("USER_EMAIL"))
        login.enter_password(os.environ.get("PASSWORD"))
        login.click_login()

        assert login.is_dashboard_displayed(), "Login failed"
        cls.device = DevicePage(cls.driver)
        cls.asset = AssetPage(cls.driver)
        
        cls.asset.click(AssetLocators.ASSETS_MENU)

    # 1 ---------------- OPEN ----------------
    @allure.title("Verify Assets page opens successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_01_open_assets_page(self):
        try:
            assert self.asset.is_visible(AssetLocators.ADD_ROOT_BTN)
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Unable to open Assets page")

    # 2 ---------------- CREATE ----------------
    @allure.title("Verify user can create root asset")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_02_create_root_asset(self):
        self.asset.click(AssetLocators.ADD_ROOT_BTN)
        self.asset.send_keys(AssetLocators.ASSET_NAME_INPUT, ASSET_NAME)
        self.asset.click(AssetLocators.ADD_BTN)
        try:
            assert self.asset.is_visible(
                AssetLocators.ASSET_NAME_NODE(ASSET_NAME))
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Root asset not created")

    # 3 ---------------- SEARCH ----------------
    @allure.title("Verify asset search works")
    @allure.severity(allure.severity_level.NORMAL)
    def test_03_search_asset(self):
        self.asset.send_keys(AssetLocators.SEARCH_INPUT, "Auto")
        try:
            assert self.asset.is_visible(
                AssetLocators.ASSET_NAME_NODE(ASSET_NAME))
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Search asset failed")

    # 4 ---------------- PARTIAL SEARCH ----------------
    @allure.title("Verify partial search returns results")
    @allure.severity(allure.severity_level.NORMAL)
    def test_04_search_partial_match(self):
        self.asset.reset_search()
        self.asset.search_asset("Hydraulic")

        try:
            assert self.asset.is_visible(
                AssetLocators.ASSET_NAME_NODE("Hydraulic Press"))
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Partial search failed")

    # 5 ---------------- ADD CHILD ----------------
    @allure.title("Verify user can add child asset")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_05_add_child_asset(self):
        self.asset.reset_search()
        self.asset._hover_asset_row(ASSET_NAME)

        self.driver.execute_script(
            "arguments[0].click();",
            self.asset.get_element(
                AssetLocators.ADD_CHILD_ICON(ASSET_NAME))
        )

        self.asset.send_keys(
            AssetLocators.SUB_ASSET_NAME_INPUT, CHILD_ASSET_NAME)
        self.asset.click(AssetLocators.SUB_ASSET_SAVE_BTN)

        self.driver.execute_script(
            "arguments[0].click();",
            self.asset.get_element(
                AssetLocators.EXPAND_BTN(ASSET_NAME))
        )

        try:
            assert self.asset.is_visible(
                AssetLocators.ASSET_NAME_NODE(CHILD_ASSET_NAME))
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Child asset not added")

    # 6 ---------------- EDIT ----------------
    @allure.title("Verify asset can be edited")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_06_edit_asset(self):
        self.asset._hover_asset_row(ASSET_NAME)

        self.driver.execute_script(
            "arguments[0].click();",
            self.asset.get_element(
                AssetLocators.EDIT_ICON(ASSET_NAME))
        )

        edit_input = self.asset.get_element(
            AssetLocators.EDIT_INPUT)
        edit_input.clear()
        edit_input.send_keys(UPDATED_NAME)

        self.asset.click(AssetLocators.SAVE_CHANGES_BTN)

        try:
            assert self.asset.is_visible(
                AssetLocators.ASSET_NAME_NODE(UPDATED_NAME))
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Asset edit failed")

    # 7 ---------------- EMPTY DETAILS ----------------
    @allure.title("Verify empty details when no asset selected")
    @allure.severity(allure.severity_level.MINOR)
    def test_07_no_asset_selected_shows_empty_details(self):
        self.asset.click(AssetLocators.ASSETS_MENU)

        try:
            assert self.asset.is_visible(
                AssetLocators.NO_ASSET_SELECTED)
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Empty asset details not shown")

    # 8 ---------------- DETAILS ----------------
    @allure.title("Verify asset details are visible")
    @allure.severity(allure.severity_level.NORMAL)
    def test_08_asset_details_visible(self):
        self.asset.click(
            AssetLocators.ASSET_NAME_NODE(UPDATED_NAME))

        asset_type = self.asset.get_element(
            AssetLocators.TYPE_VALUE).text
        asset_level = self.asset.get_element(
            AssetLocators.LEVEL_VALUE).text

        try:
            assert asset_type != ""
            assert asset_level != ""
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Asset details not visible")

    # 9 ---------------- DELETE CHILD ----------------
    @allure.title("Verify child asset can be deleted")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_09_delete_child_asset(self):
        # self.driver.execute_script(
        #     "arguments[0].click();",
        #     self.asset.get_element(
        #         AssetLocators.EXPAND_BTN(UPDATED_NAME)))
        self.asset._hover_asset_row(CHILD_ASSET_NAME)

        self.driver.execute_script(
            "arguments[0].click();",
            self.asset.get_element(
                AssetLocators.DELETE_ICON(CHILD_ASSET_NAME)))
        self.asset.click(AssetLocators.CONFIRM_DELETE_BTN)
        try:
            assert not self.device.verify_toast_success("Deleted successfully")
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Child asset not deleted")

    # 10 ---------------- DELETE PARENT ----------------
    @allure.title("Verify parent asset can be deleted")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_10_delete_parent_asset(self):
        self.asset._hover_asset_row(UPDATED_NAME)
        self.driver.execute_script(
            "arguments[0].click();",
            self.asset.get_element(
                AssetLocators.DELETE_ICON(UPDATED_NAME)))
        self.asset.click(AssetLocators.CONFIRM_DELETE_BTN)
        try:
            assert not self.device.verify_toast_success("Deleted successfully")
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Parent asset not deleted")

    # 11 ---------------- DUPLICATE ----------------
    @allure.title("Verify duplicate asset name not allowed")
    @allure.severity(allure.severity_level.NORMAL)
    def test_11_duplicate_asset_name(self):
        self.asset.click(AssetLocators.ADD_ROOT_BTN)
        self.asset.send_keys(AssetLocators.ASSET_NAME_INPUT, "Hydraulic Press")
        self.asset.click(AssetLocators.ADD_BTN)
        try:
            assert self.asset.is_visible(SignUpLocators.TOAST_ERROR)
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Duplicate asset validation failed")

    # 12 ---------------- EMPTY NAME ----------------
    @allure.title("Verify empty asset name not allowed")
    @allure.severity(allure.severity_level.NORMAL)
    def test_12_empty_asset_name_not_allowed(self):
        # self.asset.click(AssetLocators.ADD_ROOT_BTN)
        self.asset.reset_add_asset()
        try:
            assert self.asset.is_visible(SignUpLocators.INLINE_ERROR)
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Empty asset name allowed")

    # 13 ---------------- INVALID CHARS ----------------
    @allure.title("Verify invalid characters not allowed in asset name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_13_asset_invalid_characters(self):
        # self.asset.click(AssetLocators.ADD_ROOT_BTN)
        self.asset.send_keys(AssetLocators.ASSET_NAME_INPUT, "@@###")
        try:
            assert self.asset.is_visible(
                SignUpLocators.INLINE_ERROR)
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Invalid characters accepted")

    # 14 ---------------- TOO LONG ----------------
    @allure.title("Verify asset name length validation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_14_asset_name_too_long(self):
        # self.asset.click(AssetLocators.ADD_ROOT_BTN)
        self.asset.reset_add_asset()
        self.asset.send_keys(AssetLocators.ASSET_NAME_INPUT, "A" * 150)
        try:
            assert self.asset.is_visible(
                SignUpLocators.INLINE_ERROR)
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Long asset name accepted")

    # 15 ---------------- DELETE ICON RULE ----------------
    @allure.title("Verify delete icon visibility rules")
    @allure.severity(allure.severity_level.NORMAL)
    def test_15_delete_icon_rules(self):
        self.asset.click(AssetLocators.CANCEL_BTN)
        self.driver.execute_script(
            "arguments[0].click();",
            self.asset.get_element(
                AssetLocators.EXPAND_BTN("Hydraulic Press")))

        try:
            assert not self.asset.is_visible(
                AssetLocators.DELETE_ICON("Hydraulic Press"))
            assert self.asset.is_visible(
                AssetLocators.DELETE_ICON("Robotic Arm"))
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Delete icon rule failed")

    # 16 ---------------- DEPTH LIMIT ----------------
    @allure.title("Verify asset hierarchy depth limit")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_16_asset_hierarchy_depth_limit(self):

        root = "Root_1"
        current_parent = root
        path = [root]

        depth = 1
        max_depth = 5

    # ---------- CREATE ROOT ----------
        self.asset.click(AssetLocators.ADD_ROOT_BTN)
        self.asset.send_keys(AssetLocators.ASSET_NAME_INPUT, root)
        self.asset.click(AssetLocators.ADD_BTN)

        self.assertTrue(
            self.asset.is_visible(
            AssetLocators.ASSET_NAME_NODE(root)
        ),
        "Root asset not created"
        )

    # ---------- CREATE HIERARCHY ----------
        while depth < max_depth:

            child_name = f"{current_parent}_Child"

            print(f"[DEPTH {depth}] Parent : {current_parent}")
            print(f"[DEPTH {depth}] Adding child : {child_name}")

        # Select parent
            self.asset.select_asset(current_parent)

        # Hover + add child
            self.asset._hover_asset_row(current_parent)
            self.driver.execute_script(
            "arguments[0].click();",
            self.asset.get_element(
                AssetLocators.ADD_CHILD_ICON(current_parent)
            )
        )

        # Save child
            self.asset.send_keys(
            AssetLocators.SUB_ASSET_NAME_INPUT,
            child_name
        )
            self.asset.click(
            AssetLocators.SUB_ASSET_SAVE_BTN
        )
            # WAIT FOR TREE TO STABILIZE
            time.sleep(2)

        # Expand tree to reveal new child
            self.asset.expand_path(path)

        # # Verify child visibility
        #     self.assertTrue(
        #     self.asset.is_visible(
        #         AssetLocators.ASSET_NAME_NODE(child_name)
        #     ),
        #     f"Child not visible at depth {depth}"
        # )

        # Update hierarchy
            path.append(child_name)
            current_parent = child_name
            depth += 1

        # Validate add-child availability before max depth
            if depth < max_depth:
                self.assertTrue(
                self.asset.can_add_child(current_parent),
                f"Add child must exist at depth {depth}")

    # ---------- VERIFY DEPTH LIMIT ----------
        self.assertFalse(
        self.asset.can_add_child(current_parent),
        "Add child must NOT exist after max depth") 
    
    @allure.title("TC-17: Configure Signals – Add & Persist Signal")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_17_configure_signals_add_and_persist(self):
        asset_name = "Root_1_Child_Child_Child_Child"
    # Select asset
        self.asset.select_asset(asset_name)
    # Open Configure Signals
        self.asset.click(AssetLocators.CONFIGURE_SIGNALS_BTN)
        time.sleep(2)
    # Ensure Available Signals table is visible
        self.assertTrue(self.asset.is_visible(AssetLocators.AVAILABLE_SIGNALS_TABLE), "Available signals table not visible")   
    # Add VOLTAGE signal
        self.asset.click(AssetLocators.ADD_SIGNAL_BTN)
        time.sleep(2)
    # Save changes
        self.asset.click(AssetLocators.SAVE_ALL_CHANGES_BTN)
    # Verify success toast
        self.assertTrue(self.asset.is_visible(AssetLocators.SAVE_SUCCESS_TOAST), "Save success toast not shown")


#     # ----------------- TC-20: Manage Connection – Open Map Dialog -----------------
#     @allure.title("TC-20: Manage Connection – Open Map Dialog")
#     @allure.severity(allure.severity_level.CRITICAL)
#     def test_18_manage_connection_open_map_dialog(self):
#         asset_name = "Root_1_Child_Child_Child_Child"
#         time.sleep(2)
#     # Select asset
#         self.asset.select_asset(asset_name)
#         time.sleep(2)

#     # Open Manage Connection panel
#         self.asset.click(AssetLocators.MANAGE_CONNECTION_BTN)
#         time.sleep(2)  # optional: wait for panel animation

#     # Verify Map dialog opens
#         self.assertTrue(
#         self.asset.is_visible(AssetLocators.MAP_BTN),
#         "Map dialog did not open"
#     )

# #  ----------------- TC-22: Manage Connection – Prevent Mapping Without Selection -----------------
#     @allure.title("TC-22: Manage Connection – Prevent Mapping Without Selection")
#     @allure.severity(allure.severity_level.CRITICAL)
#     def test_19_manage_connection_prevent_mapping_without_selection(self):

#     # Open Manage Connection panel & Map dialog
#         # self.asset.click(AssetLocators.MANAGE_CONNECTION_BTN)
#         self.asset.click(AssetLocators.MAP_BTN)
#         time.sleep(1)

#     # Verify Map Selected is disabled without selecting any register
#         self.assertTrue(
#         self.asset.is_visible(AssetLocators.MAP_DISABLED_BTN),
#         "Map Selected button should be disabled without register selection" )

# # ----------------- TC-21: Manage Connection – Map Register Successfully -----------------
#     @allure.title("TC-21: Manage Connection – Map Register Successfully")
#     @allure.severity(allure.severity_level.CRITICAL)
#     def test_20_manage_connection_map_register_success(self):

#         asset_name = "Root_1_Child_Child_Child_Child"

#     # # Select asset
#     #     self.asset.select_asset(asset_name)

#     # # Open Manage Connection panel & Map dialog
#     #     self.asset.click(AssetLocators.MANAGE_CONNECTION_BTN)
#         # self.asset.click(AssetLocators.MAP_BTN)
#         # time.sleep(1)

#     # Select register 40001
#         self.asset.click(AssetLocators.REGISTER_40001_CHECKBOX)
#         time.sleep(1)

#     # Click Map Selected
#         self.asset.click(AssetLocators.MAP_SELECTED_BTN)

#         self.device.verify_toast_success("Mapping created successfully")
#     # # Verify Map dialog closes
#     #     self.assertFalse(
#     #     self.asset.is_visible(AssetLocators.MAP_DIALOG),
#     #     "Map dialog did not close after mapping"
#     # )


    # ---------------- CLEANUP ----------------
    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
