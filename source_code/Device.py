import os
import unittest
from Base import Base
from Page import LoginPage, DevicePage
from locators import SignUpLocators, DeviceLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys

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

    # ---------------- NAVIGATION ----------------
    def test_navigate_to_device_module(self):
        self.device.go_to_devices()
        btn = self.driver.find_element(*DeviceLocators.ADD_DEVICE_BUTTON)
        self.assertTrue(btn.is_displayed(), "Add Device button not visible")

    # ---------------- CREATE ----------------
    def test_add_device_success(self):
        self.device.click_add_device()
        self.device.enter_device_name(DEVICE_NAME)
        self.device.enter_device_description("Monitoring battery")
        self.device.save_device()
        self.device.verify_toast_success("created successfully")
        assert self.device.is_device_visible_in_table(DEVICE_NAME)

    def test_add_device_empty_name(self):
        self.device.click_add_device()
        self.device.enter_device_name("")
        self.device.enter_device_description("Some description")
        self.device.save_device()
        self.device.verify_toast_error("Device Name is required")

    def test_add_device_empty_description_allowed(self):
        self.device.click_add_device()
        self.device.enter_device_name("TyrePressureStation_01")
        self.device.enter_device_description("")
        self.device.save_device()
        self.device.verify_toast_success("created successfully")
        assert self.device.is_device_visible_in_table("TyrePressureStation_01")

    def test_device_name_special_car123(self):
        self.device.click_add_device()
        self.device.enter_device_name("Car@123")
        self.device.save_device()
        self.device.verify_toast_error("Device Name must")

    def test_device_name_special_symbols(self):
        self.device.click_add_device()
        self.device.enter_device_name("#@!*")
        self.device.save_device()
        self.device.verify_toast_error("Device Name must")

    def test_device_name_special_dash(self):
        self.device.click_add_device()
        self.device.enter_device_name("-Station01")
        self.device.save_device()
        self.device.verify_toast_error("Device Name must")

    def test_device_name_too_short(self):
        self.device.click_add_device()
        self.device.enter_device_name("AB")
        self.device.save_device()
        self.device.verify_toast_error("Device Name must")

    def test_device_name_too_long(self):
        self.device.click_add_device()
        self.device.enter_device_name("A"*101)
        self.device.save_device()
        self.device.verify_toast_error("Device Name must")

    def test_add_duplicate_device_name(self):
        duplicate_name = "TyrePressureStation_01"
        self.device.click_add_device()
        self.device.enter_device_name(duplicate_name)
        self.device.enter_device_description("Test")
        self.device.save_device()
        self.device.verify_toast_error("already exists")

    # ---------------- DELETE ----------------
    def test_delete_device(self):
        self.device.click_delete_button(DEVICE_NAME)
        popup_name = self.driver.find_element(
            *DeviceLocators.DELETE_POPUP_DEVICE_NAME
        ).text.replace('"', '').strip()
        assert popup_name == DEVICE_NAME
        self.device.confirm_delete()
        self.device.verify_toast_success("deleted successfully")
        assert not self.device.is_device_visible_in_table(DEVICE_NAME)

    def test_delete_device_cancel(self):
        device = "TyrePressureStation_01"
        self.device.click_delete_button(device)
        self.device.cancel_delete()
        assert self.device.is_device_visible_in_table(device)

    # ---------------- EDIT ----------------
    def test_edit_device_name_success(self):
        old_name = "TyrePressureStation_01"
        new_name = "TyrePressureStation_01_updated"
        self.device.click(DeviceLocators.EDIT_BUTTON(old_name))
        self.device.wait.until(EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER))
        self.device.send_keys(DeviceLocators.DEVICE_NAME, new_name)
        self.device.click(DeviceLocators.SAVE_CHANGES)
        self.device.verify_toast_success("updated successfully")
        assert self.device.is_device_visible_in_table(new_name)

    def test_edit_device_without_name(self):
        device = "TyrePressureStation_01_updated"
        self.device.click(DeviceLocators.EDIT_BUTTON(device))
        self.device.wait.until(EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER))
        self.device.send_keys(DeviceLocators.DEVICE_NAME, "")
        self.device.click(DeviceLocators.SAVE_CHANGES)
        msg = self.device.get_browser_validation_message(DeviceLocators.DEVICE_NAME)
        assert "fill" in msg.lower()

    # ---------------- SEARCH ----------------
    def test_search_device(self):
        existing_device = "TyrePressureStation_01_updated"
        self.device.search_device(existing_device)
        assert self.device.is_device_visible_in_table(existing_device)

    def test_search_non_existing_device(self):
        self.device.search_device("INVALID_DEVICE_999")
        assert not self.device.is_device_visible_in_table("INVALID_DEVICE_999")

    # ---------------- CONFIG ----------------

    def test_open_device_config_page(self):
        device = "PaintBoothPLC_01"

    # Click CONFIG button
        self.device.click(DeviceLocators.CONFIG_BUTTON(device))

    # Wait for config page header
        self.device.wait.until(
            EC.visibility_of_element_located(DeviceLocators.CONFIG_HEADER)
    )

    # Verify header displayed
        header = self.driver.find_element(*DeviceLocators.CONFIG_HEADER)
        self.assertTrue(header.is_displayed(), "Config header not visible")


    def test_save_device_configuration(self):
        device = "PaintBoothPLC_01"

    # Open config page
        self.device.click(DeviceLocators.CONFIG_BUTTON(device))

        self.device.wait.until(
            EC.visibility_of_element_located(DeviceLocators.CONFIG_HEADER)
        )

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
    def test_edit_poll_interval_below_min(self):
        device = "PaintBoothPLC_01"
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


    def test_edit_poll_interval_above_max(self):
        device = "PaintBoothPLC_01"
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


    def test_edit_poll_interval_empty(self):
        device = "PaintBoothPLC_01"
        self.device.click(DeviceLocators.EDIT_BUTTON(device))

        self.device.wait.until(
            EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER))

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
        msg = self.device.get_browser_validation_message(
            DeviceLocators.POLL_INTERVAL_EDIT
        )
        print("\nBROWSER VALIDATION MESSAGE (POLL INTERVAL):", msg)


    # -------- IP ADDRESS --------
    def test_edit_ip_random_text(self):
        device = "PaintBoothPLC_01"
        self.device.click(DeviceLocators.EDIT_BUTTON(device))

        self.device.wait.until(
            EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER)
        )

        self.device.send_keys(DeviceLocators.POLL_INTERVAL_EDIT, "2000")
        self.device.send_keys(DeviceLocators.IP_ADDRESS_EDIT, "abcdxyz")
        self.device.send_keys(DeviceLocators.PORT_EDIT, "502")

        self.device.click(DeviceLocators.SAVE_CHANGES)
        self.device.verify_toast_error(
            "Invalid IP Address"
        )


    def test_edit_ip_wrong_format(self):
        device = "PaintBoothPLC_01"
        self.device.click(DeviceLocators.EDIT_BUTTON(device))

        self.device.wait.until(
            EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER)
        )

        self.device.send_keys(DeviceLocators.POLL_INTERVAL_EDIT, "2000")
        self.device.send_keys(DeviceLocators.IP_ADDRESS_EDIT, "300.200.1")
        self.device.send_keys(DeviceLocators.PORT_EDIT, "502")

        self.device.click(DeviceLocators.SAVE_CHANGES)
        self.device.verify_toast_error(
            "Invalid IP Address"
        )


    def test_edit_ip_letters_only(self):
        device = "PaintBoothPLC_01"
        self.device.click(DeviceLocators.EDIT_BUTTON(device))

        self.device.wait.until(
            EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER)
        )

        self.device.send_keys(DeviceLocators.POLL_INTERVAL_EDIT, "2000")
        self.device.send_keys(DeviceLocators.IP_ADDRESS_EDIT, "abcdefgh")
        self.device.send_keys(DeviceLocators.PORT_EDIT, "502")

        self.device.click(DeviceLocators.SAVE_CHANGES)
        self.device.verify_toast_error(
            "Invalid IP Address"
        )


    def test_edit_ip_empty(self):
        device = "PaintBoothPLC_01"
        self.device.click(DeviceLocators.EDIT_BUTTON(device))

        self.device.wait.until(
            EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER)
        )

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
            DeviceLocators.IP_ADDRESS_EDIT
        )
        print("\nBROWSER VALIDATION MESSAGE (IP ADDRESS):", msg)

    # -------- PORT --------
    def test_edit_port_zero(self):
        device = "PaintBoothPLC_01"
        self.device.click(DeviceLocators.EDIT_BUTTON(device))

        self.device.wait.until(
            EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER)
        )

        self.device.send_keys(DeviceLocators.POLL_INTERVAL_EDIT, "2000")
        self.device.send_keys(DeviceLocators.IP_ADDRESS_EDIT, "192.168.1.1")
        self.device.send_keys(DeviceLocators.PORT_EDIT, "0")

        self.device.click(DeviceLocators.SAVE_CHANGES)
        self.device.verify_toast_error(
            "Port must be between 1 and 65535"
        )

    def test_edit_port_above_limit(self):
        device = "PaintBoothPLC_01"
        self.device.click(DeviceLocators.EDIT_BUTTON(device))

        self.device.wait.until(
            EC.visibility_of_element_located(DeviceLocators.EDIT_HEADER)
        )

        self.device.send_keys(DeviceLocators.POLL_INTERVAL_EDIT, "2000")
        self.device.send_keys(DeviceLocators.IP_ADDRESS_EDIT, "192.168.1.1")
        self.device.send_keys(DeviceLocators.PORT_EDIT, "70000")

        self.device.click(DeviceLocators.SAVE_CHANGES)
        self.device.verify_toast_error(
            "Port must be between 1 and 65535"
        )



    # ---------------- SLAVE MANAGER ----------------

    def test_open_slave_manager(self):
        device = "PaintBoothPLC_01"

        # Click SLAVE button
        self.device.click(DeviceLocators.SLAVE_BUTTON)
        
        # Verify landing page
        title = self.driver.find_element(*DeviceLocators.SLAVE_MANAGER_TITLE)
        subtitle = self.driver.find_element(*DeviceLocators.SLAVE_MANAGER_SUBTITLE)

        self.assertTrue(title.is_displayed(), "Slave Manager title not visible")
        self.assertTrue(subtitle.is_displayed(), "Slave Manager subtitle not visible")



    def test_open_new_slave_page(self):
        device = "PaintBoothPLC_01"

        # Open Slave Manager
        self.device.click(DeviceLocators.SLAVE_BUTTON)

        # Click New Slave
        self.device.click(DeviceLocators.NEW_SLAVE_BUTTON)
        self.device.wait.until(EC.visibility_of_element_located(DeviceLocators.SLAVE_HEADER))

        header = self.driver.find_element(*DeviceLocators.SLAVE_HEADER)
        self.assertTrue(header.is_displayed(), "New Slave header not visible")



    def test_save_slave_without_register(self):
        device = "PaintBoothPLC_01"

        # Open New Slave
        self.device.click(DeviceLocators.SLAVE_BUTTON)
        self.device.click(DeviceLocators.NEW_SLAVE_BUTTON)

        # Click Save without registers
        self.device.click(DeviceLocators.SAVE_SLAVE_BTN)

        # Toast validation
        self.device.verify_toast_error("Cannot save slave with no registers")



    def test_open_add_register_popup(self):
        device = "PaintBoothPLC_01"

        # Open Add Register Popup
        self.device.click(DeviceLocators.SLAVE_BUTTON)
        self.device.click(DeviceLocators.NEW_SLAVE_BUTTON)

        self.device.click(DeviceLocators.ADD_REGISTER_BTN)
        popup = self.driver.find_element(*DeviceLocators.ADD_REG_POPUP)
        self.assertTrue(popup.is_displayed(), "Add Register popup not visible")



    def test_close_add_register_popup(self):
        device = "PaintBoothPLC_01"

        # Open and close popup
        self.device.click(DeviceLocators.SLAVE_BUTTON)
        self.device.click(DeviceLocators.NEW_SLAVE_BUTTON)

        self.device.click(DeviceLocators.ADD_REGISTER_BTN)
        self.device.click(DeviceLocators.CLOSE_POPUP)

        # Popup disappears
        self.device.wait.until(EC.invisibility_of_element_located(DeviceLocators.ADD_REG_POPUP))



    def test_add_register_success(self):
        device = "PaintBoothPLC_01"

    # Open New Slave
        self.device.click(DeviceLocators.SLAVE_BUTTON)
        self.device.click(DeviceLocators.NEW_SLAVE_BUTTON)

    # Open register popup
        self.device.click(DeviceLocators.ADD_REGISTER_BTN)

    # Save popup directly (default values already valid)
        self.device.click(DeviceLocators.POPUP_SAVE)

    # Verify toast only
        self.device.verify_toast_success("Register added locally")



    def test_cancel_register_popup(self):
        device = "PaintBoothPLC_01"

        # Open popup
        self.device.click(DeviceLocators.SLAVE_BUTTON)
        self.device.click(DeviceLocators.NEW_SLAVE_BUTTON)
        self.device.click(DeviceLocators.ADD_REGISTER_BTN)

        # Cancel popup
        self.device.click(DeviceLocators.POPUP_CANCEL)
        self.device.wait.until(EC.invisibility_of_element_located(DeviceLocators.ADD_REG_POPUP))



    def test_save_slave_after_register_add(self):
        device = "PaintBoothPLC_01"

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


    # ---------------- CLEANUP ----------------
    def tearDown(self):
        self.quit_driver()



if __name__ == "__main__":
    unittest.main()
