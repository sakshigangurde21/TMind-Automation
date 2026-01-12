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
    @classmethod
    def setUpClass(cls):
        cls.driver = cls.start_driver()
        login = LoginPage(cls.driver)
        login.enter_email(os.environ.get("USER_EMAIL"))
        login.enter_password(os.environ.get("PASSWORD"))
        login.click_login()
        assert login.is_dashboard_displayed(), "Login failed"

        cls.device = DevicePage(cls.driver)
        cls.device.go_to_devices()

    def setUp(self):
        # Optional: ensure Devices page is still open
        self.driver = self.__class__.driver
        self.device = self.__class__.device

        self.device.close_any_device_modal_if_open()

    @allure.title("Verify Devices module opens successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_01_Verify_devices_module_navigation(self):
        try:
            assert self.device.is_visible(DeviceLocators.ADD_DEVICE_BUTTON), "Add Device button not visible"
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify user can create a device with valid data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_02_Verify_create_device_successfully(self):
        self.device.click(DeviceLocators.ADD_DEVICE_BUTTON)
        self.device.send_keys(DeviceLocators.DEVICE_NAME_INPUT, DEVICE_NAME)
        self.device.send_keys(DeviceLocators.DEVICE_DESCRIPTION_INPUT, "Battery monitoring")
        self.device.click(DeviceLocators.SAVE_DEVICE_BUTTON)
        time.sleep(1)
        try:
            assert self.device.is_visible(SignUpLocators.TOAST_SUCCESS), "Success toast not displayed"
        except AssertionError:
            self.attach_screenshot("_failure")
            raise AssertionError("Device not created")

    @allure.title("Verify error when creating device without name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_03_Verify_error_for_empty_device_name(self):
        self.device.click(DeviceLocators.ADD_DEVICE_BUTTON)
        self.device.click(DeviceLocators.SAVE_DEVICE_BUTTON)
        time.sleep(1)
        try:
            self.device.verify_toast_error("Device Name is required.")
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify device creation succeeds with empty description")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_04_Verify_add_device_with_empty_description_allowed(self):
        self.device.click(DeviceLocators.ADD_DEVICE_BUTTON)
        self.device.send_keys(DeviceLocators.DEVICE_NAME_INPUT, "TyrePressureStation_01")
        self.device.send_keys(DeviceLocators.DEVICE_DESCRIPTION_INPUT, "")
        self.device.click(DeviceLocators.SAVE_DEVICE_BUTTON)
        time.sleep(1)
        try:
            assert self.device.is_visible(SignUpLocators.TOAST_SUCCESS), "Success toast not displayed"
            # assert self.device.is_device_visible_in_table("TyrePressureStation_01")
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify inline error for device name with special characters")
    @allure.severity(allure.severity_level.NORMAL)
    def test_05_Verify_error_for_device_name_special_characters(self):
        self.device.click(DeviceLocators.ADD_DEVICE_BUTTON)
        self.device.send_keys(DeviceLocators.DEVICE_NAME_INPUT, "Car@123")
        self.device.click(DeviceLocators.SAVE_DEVICE_BUTTON)
        time.sleep(1)
        try:
            self.device.verify_toast_error("Device Name must")
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify inline error for device name with only special symbols")
    @allure.severity(allure.severity_level.NORMAL)
    def test_06_Verify_error_for_device_name_only_special_symbols(self):
        self.device.wait_for_toast_disappear()
        self.device.click(DeviceLocators.ADD_DEVICE_BUTTON)
        self.device.send_keys(DeviceLocators.DEVICE_NAME_INPUT, "#@!*")
        self.device.click(DeviceLocators.SAVE_DEVICE_BUTTON)
        time.sleep(1)
        try:
            self.device.verify_toast_error("Device Name must")
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify inline error for device name starting with dash")
    @allure.severity(allure.severity_level.NORMAL)
    def test_07_Verify_error_for_device_name_starting_with_dash(self):
        self.device.wait_for_toast_to_disappear()
        self.device.click(DeviceLocators.ADD_DEVICE_BUTTON)
        self.device.send_keys(DeviceLocators.DEVICE_NAME_INPUT, "-Station01")
        self.device.click(DeviceLocators.SAVE_DEVICE_BUTTON)
        time.sleep(1)
        try:
            self.device.verify_toast_error("Device Name must")
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify inline error for device name shorter than minimum length")
    @allure.severity(allure.severity_level.NORMAL)
    def test_08_Verify_error_for_device_name_too_short(self):
        self.device.wait_for_toast_to_disappear()
        self.device.click(DeviceLocators.ADD_DEVICE_BUTTON)
        self.device.send_keys(DeviceLocators.DEVICE_NAME_INPUT, "AB")
        self.device.click(DeviceLocators.SAVE_DEVICE_BUTTON)
        time.sleep(1)
        try:
            self.device.verify_toast_error("Device Name must")
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify inline error for device name exceeding maximum length")
    @allure.severity(allure.severity_level.NORMAL)
    def test_09_Verify_error_for_device_name_too_long(self):
        self.device.wait_for_toast_to_disappear()
        self.device.click(DeviceLocators.ADD_DEVICE_BUTTON)
        self.device.send_keys(DeviceLocators.DEVICE_NAME_INPUT, "A" * 101)
        self.device.click(DeviceLocators.SAVE_DEVICE_BUTTON)
        time.sleep(1)
        try:
            self.device.verify_toast_error("Device Name must")
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify error for duplicate device name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_10_Verify_error_for_duplicate_device(self):
        self.device.wait_for_toast_to_disappear()
        duplicate_name = "TyrePressureStation_01"
        self.device.click(DeviceLocators.ADD_DEVICE_BUTTON)
        self.device.send_keys(DeviceLocators.DEVICE_NAME_INPUT, duplicate_name)
        self.device.send_keys(DeviceLocators.DEVICE_DESCRIPTION_INPUT, "Duplicate test")
        self.device.click(DeviceLocators.SAVE_DEVICE_BUTTON)
        time.sleep(1)
        try:
            assert self.device.is_visible(SignUpLocators.TOAST_ERROR), "Duplicate device error toast not shown"
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
            assert self.device.is_device_visible_in_table(device), "Device should remain after cancel delete"
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

    # @allure.title("Verify error when editing device without name")
    # @allure.severity(allure.severity_level.NORMAL)
    # def test_14_edit_device_without_name(self):
    #     device = "TyrePressureStation_01_updated"
    #     self.device.click(DeviceLocators.EDIT_BUTTON(device))
    #     self.device.wait.until(EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER))
    #     self.device.send_keys(DeviceLocators.DEVICE_NAME, "")
    #     self.device.click(DeviceLocators.SAVE_CHANGES)
    #     try:
    #         msg = self.device.get_browser_validation_message(DeviceLocators.DEVICE_NAME_INPUT)
    #         assert "fill" in msg.lower(), "Validation message not shown"
    #     except AssertionError:
    #         self.attach_screenshot("_failure")
    #         raise

    @allure.title("Verify search returns existing device")
    @allure.severity(allure.severity_level.NORMAL)
    def test_15_search_device(self):
        existing_device = "TyrePressureStation_01_updated"
        self.device.send_keys(DeviceLocators.SEARCH_DEVICES_INPUT, existing_device)
        try:
            assert self.device.is_device_visible_in_table(existing_device)
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify search returns no results for invalid device")
    @allure.severity(allure.severity_level.NORMAL)
    def test_16_search_non_existing_device(self):
        invalid_device = "INVALID_DEVICE_999"
        self.device.send_keys(DeviceLocators.SEARCH_DEVICES_INPUT, invalid_device)
        try:
            assert not self.device.is_device_visible_in_table(invalid_device)
        except AssertionError:
            self.attach_screenshot("_failure")
            raise

#     # ---------------- CONFIG ----------------

# ---------------- CONFIG ----------------

    @allure.title("Verify device config page opens successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_17_open_device_config_page(self):
        device = "PressureSensor"
        self.device.reset_search()
        try:
            self.device.click(DeviceLocators.CONFIG_BUTTON(device))
            self.device.wait.until(
                EC.visibility_of_element_located(DeviceLocators.CONFIG_HEADER)
            )
            header = self.driver.find_element(*DeviceLocators.CONFIG_HEADER)
            assert header.is_displayed(), "Config header not visible"
        except Exception:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify user can save device configuration")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_18_save_device_configuration(self):
        device = "PressureSensor"
        try:
            self.device.click(DeviceLocators.CONFIG_BUTTON(device))
            self.device.wait.until(EC.visibility_of_element_located(DeviceLocators.CONFIG_HEADER)
            )

            self.device.send_keys(DeviceLocators.CONFIG_NAME, "Default Config")
            self.device.send_keys(DeviceLocators.POLL_INTERVAL, "2000")
            self.device.send_keys(DeviceLocators.IP_ADDRESS, "192.168.1.1")
            self.device.send_keys(DeviceLocators.PORT, "502")

            self.device.click(DeviceLocators.SAVE_CONFIG)
            self.device.verify_toast_success("updated successfully")
        except Exception:
            self.attach_screenshot("_failure")
            raise

# ---------------- EDIT - CONFIG VALIDATIONS ----------------

    @allure.title("Verify error when poll interval is below minimum")
    @allure.severity(allure.severity_level.NORMAL)
    def test_19_edit_poll_interval_below_min(self):
        device = "Controller_01"
        try:
            self.device.click(DeviceLocators.EDIT_BUTTON(device))
            self.device.wait.until(
                EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER)
            )

            self.device.send_keys(DeviceLocators.POLL_INTERVAL_EDIT, "99")
            self.device.send_keys(DeviceLocators.IP_ADDRESS_EDIT, "192.168.1.1")
            self.device.send_keys(DeviceLocators.PORT_EDIT, "502")

            self.device.click(DeviceLocators.SAVE_CHANGES)
            self.device.verify_toast_error(
                "Poll interval must be between 100 and 300000 milliseconds."
            )
        except Exception:
            self.attach_screenshot("_failure")
            raise


    @allure.title("Verify error when poll interval exceeds maximum")
    @allure.severity(allure.severity_level.NORMAL)
    def test_20_edit_poll_interval_above_max(self):
        device = "Controller_01"
        try:
            self.device.click(DeviceLocators.EDIT_BUTTON(device))
            self.device.wait.until(
                EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER)
            )

            self.device.send_keys(DeviceLocators.POLL_INTERVAL_EDIT, "300001")
            self.device.send_keys(DeviceLocators.IP_ADDRESS_EDIT, "192.168.1.1")
            self.device.send_keys(DeviceLocators.PORT_EDIT, "502")

            self.device.click(DeviceLocators.SAVE_CHANGES)
            self.device.verify_toast_error(
            "Poll interval must be between 100 and 300000 milliseconds."
        )
        except Exception:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify browser validation when poll interval is empty")
    @allure.severity(allure.severity_level.NORMAL)
    def test_21_edit_poll_interval_empty(self):
        device = "Controller_01"
        try:
            self.device.click(DeviceLocators.EDIT_BUTTON(device))
            self.device.wait.until(
            EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER)
        )

            poll_field = self.device.get_element(DeviceLocators.POLL_INTERVAL_EDIT)
            poll_field.send_keys(Keys.CONTROL, "a")
            poll_field.send_keys(Keys.DELETE)

            self.device.send_keys(DeviceLocators.IP_ADDRESS_EDIT, "192.168.1.1")
            self.device.send_keys(DeviceLocators.PORT_EDIT, "502")
            self.device.click(DeviceLocators.SAVE_CHANGES)

            msg = self.device.get_browser_validation_message(
            DeviceLocators.POLL_INTERVAL_EDIT
        )
            print("\nBROWSER VALIDATION MESSAGE (POLL INTERVAL):", msg)
        except Exception:
            self.attach_screenshot("_failure")
            raise


# -------- IP ADDRESS --------

    @allure.title("Verify error for random text in IP address")
    @allure.severity(allure.severity_level.NORMAL)
    def test_22_edit_ip_random_text(self):
        device = "Controller_01"
        try:
            self.device.click(DeviceLocators.EDIT_BUTTON(device))
            self.device.wait.until(EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER))

            self.device.send_keys(DeviceLocators.POLL_INTERVAL_EDIT, "2000")
            self.device.send_keys(DeviceLocators.IP_ADDRESS_EDIT, "abcdxyz")
            self.device.send_keys(DeviceLocators.PORT_EDIT, "502")

            self.device.click(DeviceLocators.SAVE_CHANGES)
            self.device.verify_toast_error("Invalid IP Address")
        except Exception:
            self.attach_screenshot("_failure")
            raise


    @allure.title("Verify error for invalid IP format")
    @allure.severity(allure.severity_level.NORMAL)
    def test_23_edit_ip_wrong_format(self):
        device = "Controller_01"
        try:
            self.device.click(DeviceLocators.EDIT_BUTTON(device))
            self.device.wait.until(EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER))

            self.device.send_keys(DeviceLocators.POLL_INTERVAL_EDIT, "2000")
            self.device.send_keys(DeviceLocators.IP_ADDRESS_EDIT, "300.200.1")
            self.device.send_keys(DeviceLocators.PORT_EDIT, "502")

            self.device.click(DeviceLocators.SAVE_CHANGES)
            self.device.verify_toast_error("Invalid IP Address")
        except Exception:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify error for letters-only IP address")
    @allure.severity(allure.severity_level.NORMAL)
    def test_24_edit_ip_letters_only(self):
        device = "Controller_01"
        try:
            self.device.click(DeviceLocators.EDIT_BUTTON(device))
            self.device.wait.until(EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER))

            self.device.send_keys(DeviceLocators.POLL_INTERVAL_EDIT, "2000")
            self.device.send_keys(DeviceLocators.IP_ADDRESS_EDIT, "abcdefgh")
            self.device.send_keys(DeviceLocators.PORT_EDIT, "502")

            self.device.click(DeviceLocators.SAVE_CHANGES)
            self.device.verify_toast_error("Invalid IP Address")
        except Exception:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify browser validation when IP address is empty")
    @allure.severity(allure.severity_level.NORMAL)
    def test_25_edit_ip_empty(self):
        device = "Controller_01"
        try:
            self.device.click(DeviceLocators.EDIT_BUTTON(device))
            self.device.wait.until(EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER))

            self.device.send_keys(DeviceLocators.POLL_INTERVAL_EDIT, "2000")

            ip_field = self.device.get_element(DeviceLocators.IP_ADDRESS_EDIT)
            ip_field.send_keys(Keys.CONTROL, "a")
            ip_field.send_keys(Keys.DELETE)

            self.device.send_keys(DeviceLocators.PORT_EDIT, "502")
            self.device.click(DeviceLocators.SAVE_CHANGES)

            msg = self.device.get_browser_validation_message(
            DeviceLocators.IP_ADDRESS_EDIT
        )
            print("\nBROWSER VALIDATION MESSAGE (IP ADDRESS):", msg)
        except Exception:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify error when port is zero")
    @allure.severity(allure.severity_level.NORMAL)
    def test_26_edit_port_zero(self):
        device = "Controller_01"
        try:
            self.device.click(DeviceLocators.EDIT_BUTTON(device))
            self.device.wait.until(EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER))

            self.device.send_keys(DeviceLocators.POLL_INTERVAL_EDIT, "2000")
            self.device.send_keys(DeviceLocators.IP_ADDRESS_EDIT, "192.168.1.1")
            self.device.send_keys(DeviceLocators.PORT_EDIT, "0")

            self.device.click(DeviceLocators.SAVE_CHANGES)
            self.device.verify_toast_error("Port must be between 1 and 65535")
        except Exception:
            self.attach_screenshot("_failure")
            
    @allure.title("Verify error when port exceeds limit")
    @allure.severity(allure.severity_level.NORMAL)
    def test_27_edit_port_above_limit(self):
        device = "Controller_01"
        try:
            self.device.click(DeviceLocators.EDIT_BUTTON(device))
            self.device.wait.until(EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER))

            self.device.send_keys(DeviceLocators.POLL_INTERVAL_EDIT, "2000")
            self.device.send_keys(DeviceLocators.IP_ADDRESS_EDIT, "192.168.1.1")
            self.device.send_keys(DeviceLocators.PORT_EDIT, "70000")

            self.device.click(DeviceLocators.SAVE_CHANGES)
            self.device.verify_toast_error("Port must be between 1 and 65535")
        except Exception:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify new slave page opens successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_29_open_new_slave_page(self):
        try:
            self.device.click(DeviceLocators.SLAVE_BUTTON("Controller_01"))
            self.device.click(DeviceLocators.NEW_SLAVE_BUTTON)
            self.device.wait.until(
            EC.visibility_of_element_located(DeviceLocators.SLAVE_HEADER)
        )
            header = self.driver.find_element(*DeviceLocators.SLAVE_HEADER)
            assert header.is_displayed(), "New Slave header not visible"
        except Exception:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify error when saving slave without registers")
    @allure.severity(allure.severity_level.NORMAL)
    def test_30_save_slave_without_register(self):
        try:
            self.device.click(DeviceLocators.SAVE_SLAVE_BTN)
            self.device.verify_toast_error("Cannot save slave with no registers")
        except Exception:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify add register popup opens")
    @allure.severity(allure.severity_level.NORMAL)
    def test_31_open_add_register_popup(self):
        try:
            self.device.click(DeviceLocators.ADD_REGISTER_BTN)

            popup = self.driver.find_element(*DeviceLocators.ADD_REG_POPUP)
            assert popup.is_displayed(), "Add Register popup not visible"
        except Exception:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify add register popup can be closed")
    @allure.severity(allure.severity_level.NORMAL)
    def test_32_close_add_register_popup(self):
        try:
            self.device.click(DeviceLocators.CLOSE_POPUP)
            self.device.wait.until(
            EC.invisibility_of_element_located(DeviceLocators.ADD_REG_POPUP)
        )
        except Exception:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify register can be added successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_33_add_register_success(self):
        try:
            self.device.click(DeviceLocators.ADD_REGISTER_BTN)
            self.device.click(DeviceLocators.POPUP_SAVE)

            self.device.verify_toast_success("Register added locally")
        except Exception:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify slave can be saved after adding register")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_34_save_slave_after_register_add(self):
        try:
            self.device.click(DeviceLocators.SAVE_SLAVE_BTN)
            self.device.verify_toast_success("Slave created on server")
        except Exception:
            self.attach_screenshot("_failure")
            raise

    @allure.title("Verify bulk device upload functionality")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_35_bulk_device_upload(self):
        try:
            self.device.click(DeviceLocators.SIDE_PANEL_DEVICES)
            self.device.click(DeviceLocators.IMPORT_BULK_BUTTON)
            self.device.wait.until(
            EC.visibility_of_element_located(DeviceLocators.UPLOAD_CARD))

            file_input = self.device.get_hidden_element(DeviceLocators.FILE_INPUT)
            file_input.send_keys(
            r"C:\Users\Sakshi Gangurde\Downloads\devices_sample.xlsx")

            self.device.wait.until(
            EC.visibility_of_element_located(DeviceLocators.CSV_READY_MESSAGE))
            self.device.click(DeviceLocators.SAVE_DEVICES_BUTTON)
            self.device.verify_toast_success("Device bulk upload completed")
        except Exception:
            self.attach_screenshot("_failure")
            raise

    @classmethod
    def tearDownClass(cls):
        cls.quit_driver()

if __name__ == "__main__":
    unittest.main()
