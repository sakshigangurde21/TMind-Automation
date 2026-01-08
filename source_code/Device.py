import os
import unittest
from Base import Base
from Page import LoginPage, DevicePage
from locators import SignUpLocators, DeviceLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys
import allure
import time

load_dotenv()

DEVICE_NAME = "BatteryMonitor_01"

class DevicesTests(Base):
    def setUp(self):
        self.driver = super().start_driver()
        login = LoginPage(self.driver)
        login.enter_email(os.environ.get("USER_EMAIL"))
        login.enter_password(os.environ.get("PASSWORD"))
        login.click_login()
        assert login.is_dashboard_displayed()

        self.device = DevicePage(self.driver)
        self.device.go_to_devices()
        
    @allure.title("Verify Devices module opens successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_Verify_devices_module_navigation(self):

        try:
            assert self.device.is_visible(DeviceLocators.ADD_DEVICE_BUTTON), \
                "Add Device button not visible"
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify user can create a device with valid data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_Verify_create_device_successfully(self):

        self.device.click(DeviceLocators.ADD_DEVICE_BUTTON)
        self.device.send_keys(DeviceLocators.DEVICE_NAME_INPUT, DEVICE_NAME)
        self.device.send_keys(DeviceLocators.DEVICE_DESCRIPTION_INPUT, "Battery monitoring")
        self.device.click(DeviceLocators.SAVE_DEVICE_BUTTON)

        try:
            assert self.device.is_visible(SignUpLocators.TOAST_SUCCESS), \
                "Success toast not displayed"
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Device not created")

    @allure.title("Verify error when creating device without name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_Verify_error_for_empty_device_name(self):

        self.device.click(DeviceLocators.ADD_DEVICE_BUTTON)
        self.device.click(DeviceLocators.SAVE_DEVICE_BUTTON)

        try:
            self.device.verify_inline_error()
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify device creation succeeds with empty description")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_Verify_add_device_with_empty_description_allowed(self):

        self.device.click(DeviceLocators.ADD_DEVICE_BUTTON)
        self.device.send_keys(DeviceLocators.DEVICE_NAME_INPUT, "TyrePressureStation_01")
        self.device.send_keys(DeviceLocators.DEVICE_DESCRIPTION_INPUT, "")
        self.device.click(DeviceLocators.SAVE_DEVICE_BUTTON)

        try:
            assert self.device.is_visible(SignUpLocators.TOAST_SUCCESS), \
                "Success toast not displayed"
            assert self.device.is_device_visible_in_table("TyrePressureStation_01")
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify inline error for device name with special characters")
    @allure.severity(allure.severity_level.NORMAL)
    def test_Verify_error_for_device_name_special_characters(self):

        self.device.click(DeviceLocators.ADD_DEVICE_BUTTON)
        self.device.send_keys(DeviceLocators.DEVICE_NAME_INPUT, "Car@123")

        try:
            self.device.verify_inline_error()
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify inline error for device name with only special symbols")
    @allure.severity(allure.severity_level.NORMAL)
    def test_Verify_error_for_device_name_only_special_symbols(self):

        self.device.click(DeviceLocators.ADD_DEVICE_BUTTON)
        self.device.send_keys(DeviceLocators.DEVICE_NAME_INPUT, "#@!*")

        try:
            self.device.verify_inline_error()
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify inline error for device name starting with dash")
    @allure.severity(allure.severity_level.NORMAL)
    def test_Verify_error_for_device_name_starting_with_dash(self):

        self.device.click(DeviceLocators.ADD_DEVICE_BUTTON)
        self.device.send_keys(DeviceLocators.DEVICE_NAME_INPUT, "-Station01")

        try:
            self.device.verify_inline_error()
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify inline error for device name shorter than minimum length")
    @allure.severity(allure.severity_level.NORMAL)
    def test_Verify_error_for_device_name_too_short(self):

        self.device.click(DeviceLocators.ADD_DEVICE_BUTTON)
        self.device.send_keys(DeviceLocators.DEVICE_NAME_INPUT, "AB")

        try:
            self.device.verify_inline_error()
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify inline error for device name exceeding maximum length")
    @allure.severity(allure.severity_level.NORMAL)
    def test_Verify_error_for_device_name_too_long(self):

        self.device.click(DeviceLocators.ADD_DEVICE_BUTTON)
        self.device.send_keys(DeviceLocators.DEVICE_NAME_INPUT, "A" * 101)

        try:
            self.device.verify_inline_error()
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify error for duplicate device name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_Verify_error_for_duplicate_device(self):

        duplicate_name = "TyrePressureStation_01"

        self.device.click(DeviceLocators.ADD_DEVICE_BUTTON)
        self.device.send_keys(DeviceLocators.DEVICE_NAME_INPUT, duplicate_name)
        self.device.send_keys(DeviceLocators.DEVICE_DESCRIPTION_INPUT, "Duplicate test")
        self.device.click(DeviceLocators.SAVE_DEVICE_BUTTON)

        try:
            assert self.device.is_visible(SignUpLocators.TOAST_ERROR), \
                "Duplicate device error toast not shown"
        except AssertionError:
            self.attach_screenshot("_failure")
            raise


    @allure.title("Verify user can delete a device successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_11_delete_device(self):

        try:
            self.device.click(DeviceLocators.DELETE_BUTTON(DEVICE_NAME))
            popup_name = self.driver.find_element(*DeviceLocators.DELETE_POPUP_DEVICE_NAME).text.replace('"', '').strip()
            assert popup_name == DEVICE_NAME, "Incorrect device shown in delete popup"

            self.device.click(DeviceLocators.YES_DELETE_IT_BUTTON)
            self.device.verify_toast_success("deleted successfully")
            assert not self.device.is_device_visible_in_table(DEVICE_NAME)

        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify delete device cancel action")
    @allure.severity(allure.severity_level.NORMAL)
    def test_12_delete_device_cancel(self):

        device = "TyrePressureStation_01"
        self.device.click(DeviceLocators.DELETE_BUTTON(device))
        self.device.click(DeviceLocators.NO_KEEP_IT_BUTTON)
        try:
            assert self.device.is_device_visible_in_table(device), \
            "Device should remain after cancel delete"
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify user can edit device name successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_13_edit_device_name_success(self):
        old_name = "TyrePressureStation_01"
        new_name = "TyrePressureStation_01_updated"
        self.device.click(DeviceLocators.EDIT_BUTTON(old_name))
        self.device.wait.until(EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER))
        self.device.send_keys(DeviceLocators.DEVICE_NAME, new_name)
        self.device.click(DeviceLocators.SAVE_CHANGES)
        self.device.verify_toast_success("updated successfully")
        try:
            assert self.device.is_device_visible_in_table(new_name)
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify error when editing device without name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_14_edit_device_without_name(self):
        device = "TyrePressureStation_01_updated"
        try:
            self.device.click(DeviceLocators.EDIT_BUTTON(device))
            self.device.wait.until(EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER))
            self.device.send_keys(DeviceLocators.DEVICE_NAME, "")
            self.device.click(DeviceLocators.SAVE_CHANGES)
            msg = self.device.get_browser_validation_message(DeviceLocators.DEVICE_NAME_INPUT)
            assert "fill" in msg.lower(), "Validation message not shown"
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify search returns existing device")
    @allure.severity(allure.severity_level.NORMAL)
    def test_15_search_device(self):
        existing_device = "TyrePressureStation_01_updated"
        try:
            self.device.send_keys(DeviceLocators.SEARCH_DEVICES_INPUT, existing_device)
            assert self.device.is_device_visible_in_table(existing_device)
        except AssertionError:
            self.attach_screenshot("_failure")
            raise


    @allure.title("Verify search returns no results for invalid device")
    @allure.severity(allure.severity_level.NORMAL)
    def test_16_search_non_existing_device(self):
        invalid_device = "INVALID_DEVICE_999"
        try:
            self.device.send_keys(DeviceLocators.SEARCH_DEVICES_INPUT, invalid_device)
            assert not self.device.is_device_visible_in_table(invalid_device)
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    # ---------------- CONFIG ----------------

    def test_17_open_device_config_page(self):
        device = "PressureSensor"

    # Click CONFIG button
        self.device.click(DeviceLocators.CONFIG_BUTTON(device))

    # Wait for config page header
        self.device.wait.until(
            EC.visibility_of_element_located(DeviceLocators.CONFIG_HEADER))

    # Verify header displayed
        header = self.driver.find_element(*DeviceLocators.CONFIG_HEADER)
        self.assertTrue(header.is_displayed(), "Config header not visible")


    def test_18_save_device_configuration(self):
        device = "PressureSensor"

    # Open config page
        self.device.click(DeviceLocators.CONFIG_BUTTON(device))

        self.device.wait.until(
            EC.visibility_of_element_located(DeviceLocators.CONFIG_HEADER))

    # Update config fields
        self.device.send_keys(DeviceLocators.CONFIG_NAME, "Default Config")
        self.device.send_keys(DeviceLocators.POLL_INTERVAL, "2000")
        self.device.send_keys(DeviceLocators.IP_ADDRESS, "192.168.1.1")
        self.device.send_keys(DeviceLocators.PORT, "502")

    # Save configuration
        self.device.click(DeviceLocators.SAVE_CONFIG)

    # Validate toast
        self.device.verify_toast_success("updated successfully")


    # ---------------- EDIT - CONFIG VALIDATIONS ----------------

    # -------- POLL INTERVAL --------
    def test_19_edit_poll_interval_below_min(self):
        device = "Controller_01"
        self.device.click(DeviceLocators.EDIT_BUTTON(device))

        self.device.wait.until(
            EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER))

        self.device.send_keys(DeviceLocators.POLL_INTERVAL_EDIT, "99")
        self.device.send_keys(DeviceLocators.IP_ADDRESS_EDIT, "192.168.1.1")
        self.device.send_keys(DeviceLocators.PORT_EDIT, "502")

        self.device.click(DeviceLocators.SAVE_CHANGES)
        self.device.verify_toast_error(
            "Poll interval must be between 100 and 300000 milliseconds.")


    def test_20_edit_poll_interval_above_max(self):
        device = "Controller_01"
        self.device.click(DeviceLocators.EDIT_BUTTON(device))

        self.device.wait.until(
            EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER))

        self.device.send_keys(DeviceLocators.POLL_INTERVAL_EDIT, "300001")
        self.device.send_keys(DeviceLocators.IP_ADDRESS_EDIT, "192.168.1.1")
        self.device.send_keys(DeviceLocators.PORT_EDIT, "502")

        self.device.click(DeviceLocators.SAVE_CHANGES)
        self.device.verify_toast_error("Poll interval must be between 100 and 300000 milliseconds.")


    def test_21_edit_poll_interval_empty(self):
        device = "Controller_01"
        self.device.click(DeviceLocators.EDIT_BUTTON(device))
        self.device.wait.until(EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER))

    # ---- Properly clear Poll Interval ----
        poll_field = self.device.get_element(DeviceLocators.POLL_INTERVAL_EDIT)
        poll_field.send_keys(Keys.CONTROL, "a")
        poll_field.send_keys(Keys.DELETE)

    # Valid IP
        self.device.send_keys(DeviceLocators.IP_ADDRESS_EDIT, "192.168.1.1")

    # Valid port
        self.device.send_keys(DeviceLocators.PORT_EDIT, "502")

    # Click save
        self.device.click(DeviceLocators.SAVE_CHANGES)

    # Fetch browser validation
        msg = self.device.get_browser_validation_message(DeviceLocators.POLL_INTERVAL_EDIT)
        print("\nBROWSER VALIDATION MESSAGE (POLL INTERVAL):", msg)

    # -------- IP ADDRESS --------
    def test_22_edit_ip_random_text(self):
        device = "Controller_01"
        self.device.click(DeviceLocators.EDIT_BUTTON(device))

        self.device.wait.until(EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER))

        self.device.send_keys(DeviceLocators.POLL_INTERVAL_EDIT, "2000")
        self.device.send_keys(DeviceLocators.IP_ADDRESS_EDIT, "abcdxyz")
        self.device.send_keys(DeviceLocators.PORT_EDIT, "502")

        self.device.click(DeviceLocators.SAVE_CHANGES)
        self.device.verify_toast_error("Invalid IP Address")

    def test_23_edit_ip_wrong_format(self):
        device = "Controller_01"
        self.device.click(DeviceLocators.EDIT_BUTTON(device))

        self.device.wait.until(EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER))

        self.device.send_keys(DeviceLocators.POLL_INTERVAL_EDIT, "2000")
        self.device.send_keys(DeviceLocators.IP_ADDRESS_EDIT, "300.200.1")
        self.device.send_keys(DeviceLocators.PORT_EDIT, "502")

        self.device.click(DeviceLocators.SAVE_CHANGES)
        self.device.verify_toast_error("Invalid IP Address")


    def test_24_edit_ip_letters_only(self):
        device = "Controller_01"
        self.device.click(DeviceLocators.EDIT_BUTTON(device))

        self.device.wait.until(EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER))

        self.device.send_keys(DeviceLocators.POLL_INTERVAL_EDIT, "2000")
        self.device.send_keys(DeviceLocators.IP_ADDRESS_EDIT, "abcdefgh")
        self.device.send_keys(DeviceLocators.PORT_EDIT, "502")

        self.device.click(DeviceLocators.SAVE_CHANGES)
        self.device.verify_toast_error("Invalid IP Address")


    def test_25_edit_ip_empty(self):
        device = "Controller_01"
        self.device.click(DeviceLocators.EDIT_BUTTON(device))

        self.device.wait.until(EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER))

    # Fill valid values
        self.device.send_keys(DeviceLocators.POLL_INTERVAL_EDIT, "2000")

    # ---- Properly clear IP field ----
        ip_field = self.device.get_element(DeviceLocators.IP_ADDRESS_EDIT)
        ip_field.send_keys(Keys.CONTROL, "a")
        ip_field.send_keys(Keys.DELETE)

    # Keep port valid
        self.device.send_keys(DeviceLocators.PORT_EDIT, "502")

    # Click save
        self.device.click(DeviceLocators.SAVE_CHANGES)

    # Fetch browser validation
        msg = self.device.get_browser_validation_message(
            DeviceLocators.IP_ADDRESS_EDIT)
        print("\nBROWSER VALIDATION MESSAGE (IP ADDRESS):", msg)

    # -------- PORT --------
    def test_26_edit_port_zero(self):
        device = "Controller_01"
        self.device.click(DeviceLocators.EDIT_BUTTON(device))

        self.device.wait.until(EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER))

        self.device.send_keys(DeviceLocators.POLL_INTERVAL_EDIT, "2000")
        self.device.send_keys(DeviceLocators.IP_ADDRESS_EDIT, "192.168.1.1")
        self.device.send_keys(DeviceLocators.PORT_EDIT, "0")

        self.device.click(DeviceLocators.SAVE_CHANGES)
        self.device.verify_toast_error(
            "Port must be between 1 and 65535")

    def test_27_edit_port_above_limit(self):
        device = "Controller_01"
        self.device.click(DeviceLocators.EDIT_BUTTON(device))

        self.device.wait.until(
            EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER))

        self.device.send_keys(DeviceLocators.POLL_INTERVAL_EDIT, "2000")
        self.device.send_keys(DeviceLocators.IP_ADDRESS_EDIT, "192.168.1.1")
        self.device.send_keys(DeviceLocators.PORT_EDIT, "70000")

        self.device.click(DeviceLocators.SAVE_CHANGES)
        self.device.verify_toast_error(
            "Port must be between 1 and 65535")

    # ---------------- SLAVE MANAGER ----------------

    # def test_28_open_slave_manager(self):
    #     device = "GasDetector-G7"

    #     # Click SLAVE button
    #     self.device.click(DeviceLocators.SLAVE_BUTTON)
        
    #     # Verify landing page
    #     title = self.driver.find_element(*DeviceLocators.SLAVE_MANAGER_TITLE)
    #     subtitle = self.driver.find_element(*DeviceLocators.SLAVE_MANAGER_SUBTITLE)

    #     self.assertTrue(title.is_displayed(), "Slave Manager title not visible")
    #     self.assertTrue(subtitle.is_displayed(), "Slave Manager subtitle not visible")


    def test_29_open_new_slave_page(self):
        device = "Controller_01"

        # Open Slave Manager
        self.device.click(DeviceLocators.SLAVE_BUTTON)

        # Click New Slave
        self.device.click(DeviceLocators.NEW_SLAVE_BUTTON)
        self.device.wait.until(EC.visibility_of_element_located(DeviceLocators.SLAVE_HEADER))

        header = self.driver.find_element(*DeviceLocators.SLAVE_HEADER)
        self.assertTrue(header.is_displayed(), "New Slave header not visible")


    def test_30_save_slave_without_register(self):
        device = "Controller_01"

        # Open New Slave
        self.device.click(DeviceLocators.SLAVE_BUTTON)
        self.device.click(DeviceLocators.NEW_SLAVE_BUTTON)

        # Click Save without registers
        self.device.click(DeviceLocators.SAVE_SLAVE_BTN)

        # Toast validation
        self.device.verify_toast_error("Cannot save slave with no registers")


    def test_31_open_add_register_popup(self):
        device = "Controller_01"

        # Open Add Register Popup
        self.device.click(DeviceLocators.SLAVE_BUTTON)
        self.device.click(DeviceLocators.NEW_SLAVE_BUTTON)

        self.device.click(DeviceLocators.ADD_REGISTER_BTN)
        popup = self.driver.find_element(*DeviceLocators.ADD_REG_POPUP)
        self.assertTrue(popup.is_displayed(), "Add Register popup not visible")


    def test_32_close_add_register_popup(self):
        device = "Controller_01"

        # Open and close popup
        self.device.click(DeviceLocators.SLAVE_BUTTON)
        self.device.click(DeviceLocators.NEW_SLAVE_BUTTON)

        self.device.click(DeviceLocators.ADD_REGISTER_BTN)
        self.device.click(DeviceLocators.CLOSE_POPUP)

        # Popup disappears
        self.device.wait.until(EC.invisibility_of_element_located(DeviceLocators.ADD_REG_POPUP))


    def test_33_add_register_success(self):
        device = "Controller_017"

    # Open New Slave
        self.device.click(DeviceLocators.SLAVE_BUTTON)
        self.device.click(DeviceLocators.NEW_SLAVE_BUTTON)

    # Open register popup
        self.device.click(DeviceLocators.ADD_REGISTER_BTN)

    # Save popup directly (default values already valid)
        self.device.click(DeviceLocators.POPUP_SAVE)

    # Verify toast only
        self.device.verify_toast_success("Register added locally")


    def test_34_cancel_register_popup(self):
        device = "Controller_01"

        # Open popup
        self.device.click(DeviceLocators.SLAVE_BUTTON)
        self.device.click(DeviceLocators.NEW_SLAVE_BUTTON)
        self.device.click(DeviceLocators.ADD_REGISTER_BTN)

        # Cancel popup
        self.device.click(DeviceLocators.POPUP_CANCEL)
        self.device.wait.until(EC.invisibility_of_element_located(DeviceLocators.ADD_REG_POPUP))


    def test_35_save_slave_after_register_add(self):
        device = "Controller_01"

        # Open new slave
        self.device.click(DeviceLocators.SLAVE_BUTTON)
        self.device.click(DeviceLocators.NEW_SLAVE_BUTTON)

        # Add 1 register
        self.device.click(DeviceLocators.ADD_REGISTER_BTN)
        self.device.click(DeviceLocators.POPUP_SAVE)
        self.device.verify_toast_success("Register added locally")

        # Save slave
        self.device.click(DeviceLocators.SAVE_SLAVE_BTN)

        # Final success toast
        self.device.verify_toast_success("Slave created on server")

    def test_36_bulk_device_upload(self):
    # 1. Open Bulk Upload modal
        self.device.click(DeviceLocators.IMPORT_BULK_BUTTON)
    # 2. Wait for upload card to be visible
        self.device.wait.until(EC.visibility_of_element_located(DeviceLocators.UPLOAD_CARD))
    # 3. Get hidden file input and send file
        file_input = self.device.get_hidden_element(DeviceLocators.FILE_INPUT)
        file_input.send_keys(r"C:\Users\Sakshi Gangurde\Downloads\devices_sample.xlsx")
    # 4. Wait for CSV ready message
        self.device.wait.until(EC.visibility_of_element_located(DeviceLocators.CSV_READY_MESSAGE))
    # 5. Click Save Devices
        self.device.click(DeviceLocators.SAVE_DEVICES_BUTTON)
    # 6. Verify toast
        self.device.verify_toast_success("10 devices uploaded successfully")

    # ---------------- CLEANUP ----------------
    def tearDown(self):
        self.quit_driver()

if __name__ == "__main__":
    unittest.main()
