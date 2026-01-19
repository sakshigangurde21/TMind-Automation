from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from locators import LoginLocators, SignUpLocators, AssetLocators, DeviceLocators, ManageUserLocators, SignalLocators, TourLocators
import os
import time
import unittest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

class BasePage:
    """Reusable methods for all pages"""
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def send_keys(self, locator, text):
        elem = self.wait.until(EC.visibility_of_element_located(locator))
        elem.clear()
        elem.send_keys(text)

    def get_text(self, locator) -> str:
        element = self.driver.find_element(*locator)
        return element.text
    
    def reset_search(self):
        search = self.wait.until(
        EC.visibility_of_element_located(DeviceLocators.SEARCH_DEVICES_INPUT))
        search.click()
        search.send_keys(Keys.CONTROL, "a")
        search.send_keys(Keys.DELETE)
        search.send_keys(Keys.SPACE)
        search.send_keys(Keys.BACKSPACE)

    def get_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    def is_visible(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator))
            return True
        except:
            return False    

    def get_attr(self, locator, attribute):
        return self.get_element(locator).get_attribute(attribute)

    def get_browser_validation_message(self, locator):
        return self.get_element(locator).get_attribute("validationMessage")

    def wait_for_toast(self, timeout=10):
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".Toastify__toast")))

    def get_toast_message(self, timeout=5):
        try:
            toast = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".Toastify__toast")))
            return toast.text.strip()
        except:
            return None

    def wait_for_toast_to_disappear(self, timeout=10):
        """Wait for toast to appear (if any) and disappear."""
        try:
            WebDriverWait(self.driver, timeout/2).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "Toastify__toast")))
        except:
            pass
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "Toastify__toast")))
        except:
            pass

    def verify_toast_error(self, locator, expected_text):
        toast = self.wait.until(
            EC.visibility_of_element_located(locator))
        assert expected_text in toast.text, f"Expected '{expected_text}', got '{toast.text}'"

    def wait_for_toast_disappear(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(SignUpLocators.TOAST_ERROR))
        except:
            pass


    # def verify_inline_error(self, locator):
    #     self.wait.until(
    #         EC.visibility_of_element_located(locator))
        
    def verify_inline_error(self, locator=SignUpLocators.INLINE_ERROR):
        self.wait.until(EC.visibility_of_element_located(locator))

    # def clear_search(self):
    #     search = self.wait.until(
    #         EC.visibility_of_element_located(AssetLocators.SEARCH_INPUT))
    #     search.clear()

    def clear_search(self):
        search = self.get_element(AssetLocators.SEARCH_INPUT)
    
    # Clear input via JS and trigger input event
        self.driver.execute_script("""
            arguments[0].value = '';
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        """, search)
    # Wait until the search input is truly empty
        WebDriverWait(self.driver, 5).until(lambda d: search.get_attribute("value") == '')
    # Wait until at least one asset is visible (or your "no assets" message disappears)
        WebDriverWait(self.driver, 5).until(
            lambda d: len(d.find_elements(By.XPATH, "//span[contains(@class,'text-sm')]")) > 0)
        
        
    def search_asset(self, term):
        search = self.get_element(AssetLocators.SEARCH_INPUT)
        search.clear()
        search.send_keys(term)

    # Wait until at least one matching asset appears
        WebDriverWait(self.driver, 5).until(
            lambda d: len(d.find_elements(*AssetLocators.ASSET_NAME_NODE(term))) > 0)

# ------------------------- LOGIN PAGE -------------------------
class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        url = os.environ.get("BASE_URL")  # Load URL from .env
        self.driver.get(url)
    
        print("OPENING URL:", url)
        self.username = os.environ.get("USER_EMAIL")
        self.password = os.environ.get("PASSWORD")

    def enter_email(self, email):
        self.send_keys(LoginLocators.EMAIL_INPUT, email)

    def enter_password(self, password):
        self.send_keys(LoginLocators.PASSWORD_INPUT, password)

    def click_login(self):
        self.click(LoginLocators.LOGIN_BUTTON)

    def is_dashboard_displayed(self):
        self.wait.until(EC.url_contains("/dashboard"))
        return "/dashboard" in self.driver.current_url

# ========================= SIGN UP PAGE =========================
class SignUpPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        url = os.environ.get("BASE_URL")
        self.driver.get(url)

    def navigate_to_signup(self):
        self.driver.delete_all_cookies()
        self.driver.refresh()
        self.click(SignUpLocators.SIGN_UP_LINK)
        self.wait.until(EC.visibility_of_element_located(SignUpLocators.USERNAME_FIELD))

    def password_type(self):
        return self.get_attr(SignUpLocators.PASSWORD_FIELD, "type")

    def is_success_text_visible(self):
        try:
            self.wait.until(
                EC.visibility_of_element_located(SignUpLocators.SUCCESS_LOGIN_TEXT))
            return True
        except:
            return False
  
    def is_error_message_displayed(self):
        return len(self.driver.find_elements(*SignUpLocators.ERROR_MESSAGES)) > 0

    def get_validation_message(self):
        return (
            self.get_browser_validation_message(SignUpLocators.USERNAME_FIELD)
            or self.get_browser_validation_message(SignUpLocators.EMAIL_FIELD)
            or self.get_browser_validation_message(SignUpLocators.PASSWORD_FIELD))

    def is_error_displayed(self):
        return (
            self.is_error_message_displayed()
            or bool(self.get_toast_message())
            or bool(self.get_validation_message()))

    def get_toast_error(self):
        return self.get_toast_message()

# ========================= ASSET PAGE =========================
class AssetPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def select_asset(self, name): 
        self.click(AssetLocators.ASSET_NAME_NODE(name))

    def can_add_child(self, asset_name): 
        try: 
            self.wait.until( EC.visibility_of_element_located( AssetLocators.ADD_CHILD_ICON(asset_name) ) ) 
            return True 
        except: 
            return False
        
    def reset_search(self):
        search = self.wait.until(
        EC.visibility_of_element_located(AssetLocators.SEARCH_INPUT))
        search.click()
        search.send_keys(Keys.CONTROL, "a")
        search.send_keys(Keys.DELETE)
        search.send_keys(Keys.SPACE)
        search.send_keys(Keys.BACKSPACE)

    def reset_add_asset(self):
        search = self.wait.until(
        EC.visibility_of_element_located(AssetLocators.ASSET_NAME_INPUT))
        search.click()
        search.send_keys(Keys.CONTROL, "a")
        search.send_keys(Keys.DELETE)
        search.send_keys(Keys.SPACE)
        search.send_keys(Keys.BACKSPACE)
    # ---------- INTERNAL COMMON HELPERS ----------
    def _hover_asset_row(self, name):
        """Hover full asset ROW (not only the text span)"""
        asset_row = self.wait.until(
            EC.visibility_of_element_located(
                AssetLocators.ASSET_ROW(name)))

    # Scroll
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});",asset_row)
        time.sleep(0.3)

    # Hover row so icons appear
        ActionChains(self.driver) \
            .move_to_element(asset_row) \
            .pause(0.5) \
            .perform()

        return asset_row

    # ---------- TREE CONTROL ----------
    def expand_asset(self, name):
        self.driver.execute_script(
            "arguments[0].click();",
            self.get_element(AssetLocators.EXPAND_BTN(name)))
        time.sleep(0.3)

    def expand_path(self, path_list):
        """
        Expand all nodes in the path to ensure the target node is visible.
        path_list: ['Root_1', 'Root_1_Child', ...]
        """
        for node in path_list:
            try:
                self.expand_asset(node)
            except Exception:
                pass
    

class DevicePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
    
    # ---------------- Navigation ----------------
    def go_to_devices(self):
        self.wait.until(EC.element_to_be_clickable(DeviceLocators.SIDE_PANEL_DEVICES)).click()
        self.wait.until(EC.visibility_of_element_located(DeviceLocators.ADD_DEVICE_BUTTON))
   
    def close_any_device_modal_if_open(self):
        try:
        # 1️⃣ Add Device modal
            if self.is_visible(DeviceLocators.CANCEL_DEVICE_BUTTON, timeout=2):
                self.click(DeviceLocators.CANCEL_DEVICE_BUTTON)
                self.wait.until(
                    EC.invisibility_of_element_located(
                        DeviceLocators.CANCEL_DEVICE_BUTTON
                )
            )

        # 2️⃣ Edit Device modal
            elif self.is_visible(DeviceLocators.BACK_TO_DEVICES, timeout=2):
                self.click(DeviceLocators.BACK_TO_DEVICES)
                self.wait.until(
                    EC.invisibility_of_element_located(
                    DeviceLocators.BACK_TO_DEVICES
                )
            )

        # 3️⃣ Config page
            elif self.is_visible(DeviceLocators.BACK_CONFIG, timeout=2):
                self.click(DeviceLocators.BACK_CONFIG)
                self.wait.until(
                    EC.invisibility_of_element_located(
                        DeviceLocators.BACK_CONFIG
                )
            )
        except Exception:
            pass  # Safe state → nothing open


    # ---------------- Toast Verifications ----------------
    def verify_toast_success(self, expected_text):
        self.wait.until(EC.text_to_be_present_in_element(SignUpLocators.TOAST_SUCCESS, expected_text))
        toast = self.driver.find_element(*SignUpLocators.TOAST_SUCCESS)
        print("SUCCESS TOAST:", toast.text.strip())
        self.wait.until(EC.invisibility_of_element_located(SignUpLocators.TOAST_SUCCESS))

    def verify_toast_error(self, expected_text):
        toast = self.wait.until(EC.visibility_of_element_located(SignUpLocators.TOAST_ERROR))
        actual = toast.text.strip()
        print("ERROR TOAST:", actual)
        assert expected_text in actual

    def get_hidden_element(self, locator):
        return self.driver.find_element(*locator)

    # ---------------- Device Search ----------------
    def search_device(self, device_name):
        search_box = self.wait.until(EC.visibility_of_element_located(DeviceLocators.SEARCH_DEVICES_INPUT))
        search_box.clear()
        search_box.send_keys(device_name)

    def is_device_visible_in_table(self, name):
        try:
            self.driver.find_element(*DeviceLocators.DEVICE_IN_TABLE(name))
            return True
        except:
            return False

    def verify_register_row_visible(self, address):
        """Verify register appears in table after popup save."""
        row = (By.XPATH, f"//td[normalize-space()='{address}']")
        self.wait.until(EC.visibility_of_element_located(row))




class ManageUserPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    # ---------------- Navigation ----------------
    def go_to_manage_user(self):
        self.click(ManageUserLocators.SIDE_PANEL_MANAGE_USER)
        self.wait.until(EC.visibility_of_element_located(ManageUserLocators.PAGE_HEADER))

    # ---------------- Search ----------------
    def search_user(self, username):
        self.send_keys(ManageUserLocators.SEARCH_USER_INPUT, username)

    # ---------------- Role Change ----------------
    def change_user_role(self, row_element, new_role):
        dropdown = row_element.find_element(By.XPATH, ManageUserLocators.ROLE_DROPDOWN)
        select = Select(dropdown)
        select.select_by_visible_text(new_role)

    def get_user_role(self, row_element):
        dropdown = row_element.find_element(By.XPATH, ManageUserLocators.ROLE_DROPDOWN)
        select = Select(dropdown)
        return select.first_selected_option.text.strip()

    def reset_search(self):
        search = self.wait.until(
        EC.visibility_of_element_located(ManageUserLocators.SEARCH_USER_INPUT))
        search.click()
        search.send_keys(Keys.CONTROL, "a")
        search.send_keys(Keys.DELETE)
        search.send_keys(Keys.SPACE)
        search.send_keys(Keys.BACKSPACE)

    # ---------------- Table Rows ----------------
    def get_all_user_rows(self):
        """Return all row elements in the user table, ignoring 'No users found' row."""
        rows = self.driver.find_elements(*ManageUserLocators.USER_TABLE_ROWS)
        # filter out the "No users found" row
        filtered = [row for row in rows if "No users found" not in row.text]
        return filtered

    def get_user_row_by_username(self, username):
        """Return the row element for a given username"""
        rows = self.get_all_user_rows()
        for row in rows:
            uname = row.find_element(By.XPATH, ManageUserLocators.USERNAME_CELL).text.strip()
            if uname == username:
                return row
        return None

    # ---------------- Delete User ----------------
    def click_delete_user(self, username):
        row = self.get_user_row_by_username(username)
        if not row:
            raise Exception(f"User '{username}' not found in table")
    
    # scroll into view
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", row)
    
        delete_btn = row.find_element(By.XPATH, ManageUserLocators.DELETE_USER_BUTTON)
    # JS click instead of normal click
        self.driver.execute_script("arguments[0].click();", delete_btn)
    
        self.wait.until(EC.visibility_of_element_located(ManageUserLocators.DELETE_MODAL_HEADER))

    def confirm_delete(self):
        btn = self.get_element(ManageUserLocators.DELETE_MODAL_CONFIRM_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.invisibility_of_element_located(ManageUserLocators.DELETE_MODAL_HEADER))

    def cancel_delete(self):
        btn = self.get_element(ManageUserLocators.DELETE_MODAL_CANCEL_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.invisibility_of_element_located(ManageUserLocators.DELETE_MODAL_HEADER))

    # ---------------- CSV Download ----------------
    def download_csv(self):
        """Click Download CSV button"""
        self.click(ManageUserLocators.DOWNLOAD_CSV_BUTTON)
        # Optional: wait for download toast if implemented
        time.sleep(1)

    # ---------------- Verifications ----------------
    def is_user_in_table(self, username):
        """Check if user exists in table"""
        return self.get_user_row_by_username(username) is not None

    def get_all_usernames(self):
        """Return a list of all usernames visible in table"""
        rows = self.get_all_user_rows()
        return [row.find_element(By.XPATH, ManageUserLocators.USERNAME_CELL).text.strip() for row in rows]


# ---------------- Pagination ----------------
    def click_previous_page(self):
        try:
            btn = self.get_element(ManageUserLocators.PREVIOUS_PAGE_BUTTON)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(1)  # optional wait for page refresh
        except:
            raise Exception("Previous page button not found or disabled")

    def click_next_page(self):
        """Click the 'Next' pagination button"""
        try:
            btn = self.get_element(ManageUserLocators.NEXT_PAGE_BUTTON)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(1)  # optional wait for page refresh
        except:
            raise Exception("Next page button not found or disabled")

    def get_current_page_number(self):
        current = self.get_element(ManageUserLocators.CURRENT_PAGE)
        return int(current.text.strip())

    def go_to_page(self, page_num):
        """Click a specific page number in pagination"""
        page_locator = (By.XPATH, f"//ul[@class='flex flex-row items-center gap-1']//a[text()='{page_num}']")
        try:
            btn = self.wait.until(EC.element_to_be_clickable(page_locator))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(1)  # optional wait for page refresh
        except:
            raise Exception(f"Page number {page_num} not found in pagination")

    def get_all_page_numbers(self):
        """Return list of all visible page numbers as int"""
        elements = self.driver.find_elements(*ManageUserLocators.PAGE_NUMBERS)
        return [int(el.text.strip()) for el in elements if el.text.strip().isdigit()]





class SignalPage(BasePage):


    def open_signal_page(self):
        signal_menu = self.wait.until(
            EC.element_to_be_clickable(SignalLocators.SIGNAL_MENU))
        signal_menu.click()

        self.wait.until(
            EC.visibility_of_element_located(SignalLocators.SIGNAL_GRAPH_CARD))

    # ---------------- Asset Selection ----------------
    def select_main_asset(self, asset_name):
        dropdown_element = self.get_element(SignalLocators.MAIN_ASSET_DROPDOWN)
        dropdown = Select(dropdown_element)
        dropdown.select_by_visible_text(asset_name)
        time.sleep(1)  # allow graph & signals to refresh

    def select_compare_asset(self, asset_name):
        dropdown = Select(self.get_element(SignalLocators.COMPARE_ASSET_DROPDOWN))
        dropdown.select_by_visible_text(asset_name)
        time.sleep(1)


    # ---------------- Getters ----------------
    def get_assigned_device_name(self):
        return self.get_element(SignalLocators.ASSIGNED_DEVICE_BADGE).text.strip()

    def get_signals_text(self):
        return self.get_element(SignalLocators.MAIN_SIGNALS_CONTAINER).text.strip()

    # ---------------- Validations ----------------
    def is_no_signals_displayed(self):
        try:
            return self.get_element(SignalLocators.NO_SIGNALS_TEXT).is_displayed()
        except:
            return False

    def is_graph_empty(self):
        try:
            return self.get_element(SignalLocators.GRAPH_NO_DATA_TEXT).is_displayed()
        except:
            return False

    def is_graph_visible(self):
        try:
            return self.get_element(SignalLocators.SIGNAL_GRAPH_CARD).is_displayed()
        except:
            return False

    # ---------------- Refresh / Switching ----------------
    def switch_assets(self, asset1, asset2):
        self.select_main_asset(asset1)
        self.select_main_asset(asset2)

    # ---------------- High-Value Assertions ----------------
    def verify_device_and_signal_consistency(self):
        device = self.get_assigned_device_name()
        signals = self.get_signals_text()

        if device.lower() in ["not assigned", "none"]:
            assert "no signals" in signals.lower(), \
                "Signals shown without device!"




class TourPage(BasePage):

    # ---------------- Tour Actions ----------------
    def start_tour(self):
    # IMPORTANT: wait for login success toast to go away
        self.wait_for_toast_to_disappear()

        start_btn = self.wait.until(
            EC.element_to_be_clickable(TourLocators.START_TOUR_BTN))
        start_btn.click()
        self.wait_for_popover()


    def click_next(self):
        """Click the 'Next' button in the tour popover."""
        self.get_element(TourLocators.NEXT_BTN).click()
        self.wait_for_popover()

    def click_prev(self):
        """Click the 'Previous' button in the tour popover."""
        self.get_element(TourLocators.PREV_BTN).click()
        self.wait_for_popover()

    def close_tour(self):
        """Click the 'Close' button in the tour popover."""
        self.get_element(TourLocators.CLOSE_BTN).click()
        self.wait_until_popover_disappears()

    # ---------------- Getters ----------------
    def get_popover_title(self):
        """Return the text of the current popover title."""
        return self.get_element(TourLocators.POPOVER_TITLE).text.strip()

    def get_popover_description(self):
        """Return the text of the current popover description."""
        return self.get_element(TourLocators.POPOVER_DESCRIPTION).text.strip()

    # ---------------- Validations ----------------
    def is_popover_visible(self):
        """Check if the popover is currently visible."""
        try:
            return self.get_element(TourLocators.POPOVER_CONTAINER).is_displayed()
        except:
            return False

    def wait_for_popover(self, timeout=5):
        """Wait until the popover container is visible."""
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(TourLocators.POPOVER_CONTAINER)
        )

    def wait_until_popover_disappears(self, timeout=5):
        """Wait until the popover container disappears."""
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(TourLocators.POPOVER_CONTAINER))

    # ---------------- Full Tour Flow ----------------
    def complete_tour(self):
        """Iterate through the tour until completion and close it."""
        self.start_tour()
        while self.is_popover_visible():
            try:
                self.click_next()
            except:
                break
        self.close_tour()
