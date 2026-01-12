from selenium.webdriver.common.by import By

class LoginLocators:
    EMAIL_INPUT = (By.XPATH, "//input[@placeholder='Enter email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@placeholder='Enter password']")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Login']")
    ERROR_MSG = (By.XPATH, "//*[contains(@class,'text-red-500')]")
    PROFILE_ICON = (By.XPATH, "//button[./div[contains(@class,'bg-primary')]]")
    LOGOUT_BUTTON = (By.XPATH, "//div[@role='menuitem' and text()='Logout']")
    TOAST_ERROR = (By.CSS_SELECTOR, ".Toastify__toast--error")
    TOAST_SUCCESS = (By.CSS_SELECTOR, ".Toastify__toast--success")

class SignUpLocators:
    SIGN_UP_LINK = (By.XPATH, "//span[contains(text(),'Sign up')]")
    USERNAME_FIELD = (By.CSS_SELECTOR, "input[placeholder='Enter username']")
    EMAIL_FIELD = (By.CSS_SELECTOR, "input[placeholder='Enter email']")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "input[placeholder='Enter password']")
    CREATE_ACCOUNT_BUTTON = (By.XPATH, "//button[contains(text(),'Create Account')]")
    LOGIN_HERE_LINK = (By.XPATH, "//*[contains(text(),'Login here') and contains(@class,'cursor-pointer')]")
    ERROR_MESSAGES = (By.XPATH, "//*[contains(@class, 'text-red')]")
    SUCCESS_LOGIN_TEXT = (By.XPATH, "//*[contains(text(),'Registered successfully')]")
    INLINE_ERROR = (By.CSS_SELECTOR, "p.text-red-500")
    TOAST_ERROR = (By.CSS_SELECTOR, ".Toastify__toast--error")
    TOAST_SUCCESS = (By.CSS_SELECTOR, ".Toastify__toast--success")

class AssetLocators:
    ASSETS_MENU = (By.XPATH, "//span[text()='Assets']")
    ADD_ROOT_BTN = (By.XPATH, "//button[contains(.,'Add Root')]")
    SEARCH_INPUT = (By.XPATH, "//input[contains(@placeholder,'Search')]")

    ASSET_NAME_INPUT = (By.XPATH, "//input[@id='name' or contains(@placeholder,'Enter root asset')]")
    ADD_BTN = (By.XPATH, "//button[normalize-space()='Add']")

    CANCEL_BTN = (By.XPATH, "//button[normalize-space()='Cancel']")

    # ---------- Dynamic Locators ----------
    def ASSET_NAME_NODE(name):
        return (By.XPATH, f"//span[contains(@class,'text-sm') and contains(normalize-space(.),'{name}')]")

    @staticmethod
    def ASSET_ROW(name):
        return (
            By.XPATH,
            f"//span[text()='{name}']"
            "/ancestor::div[contains(@class,'hover:bg-accent')]")

    def ADD_CHILD_ICON(name):
        return (
        By.XPATH,
        f"//span[normalize-space(text())='{name}']"
        "/ancestor::div[contains(@class,'flex') and contains(@class,'items-center') and contains(@class,'justify-between')]"
        "//button[@id='add-subasset-btn']")

    def EDIT_ICON(name):
        return (
        By.XPATH,
        f"//span[normalize-space(text())='{name}']"
        "/ancestor::div[contains(@class,'flex') and contains(@class,'items-center') and contains(@class,'justify-between')]"
        "//button[@id='edit-asset-btn']")


    def DELETE_ICON(name):
        return (
        By.XPATH,
        f"//span[normalize-space(text())='{name}']"
        "/ancestor::div[contains(@class,'flex') and contains(@class,'items-center') and contains(@class,'justify-between')]"
        "//button[@id='delete-asset-btn']")

   # ---------- Add Sub-Asset Modal ----------
    SUB_ASSET_NAME_INPUT = (By.XPATH, "//input[@placeholder='Enter Asset Name' and @name='name']")

    SUB_ASSET_SAVE_BTN = (By.XPATH, "//button[normalize-space()='Save']")

    # ---------- Edit Modal ----------
    EDIT_INPUT = (By.XPATH, "//input[contains(@placeholder,'Enter new name')]")
    SAVE_CHANGES_BTN = (By.XPATH, "//button[normalize-space()='Save Changes']")

    # ---------- Delete Modal ----------
    CONFIRM_DELETE_BTN = (By.XPATH, "//button[normalize-space()='Delete']")

    def EXPAND_BTN(name):
        return (
        By.XPATH,
        f"//span[normalize-space(text())='{name}']"
        "/ancestor::div[contains(@class,'gap-2')]"
        "/button")

    NO_ASSET_SELECTED = (By.XPATH, "//*[text()='No Asset Selected']")

    # Asset in the list by name
    ASSET_BY_NAME = "//div[contains(@class,'tracking-tight') and contains(text(),'{asset_name}')]"

    # Asset detail fields
    TYPE_VALUE = (By.XPATH, "//p[text()='Type']/following-sibling::p")
    LEVEL_VALUE = (By.XPATH, "//p[text()='Level']/following-sibling::p")
    SUB_ASSETS = (By.XPATH, "//p[contains(text(),'Sub Assets:')]//span")


    # Configure Signals button (SVG) INSIDE specific asset
    CONFIGURE_SIGNALS_BTN = (
    By.XPATH,
    "(//div[.//text()[normalize-space()='Root_1_Child_Child_Child_Child']]//button[.//*[name()='svg' and contains(@class,'lucide-signal')]])[2]"
)


    AVAILABLE_SIGNALS_TABLE = (
        By.XPATH,
        "//p[text()='Available signals (click to add)']/following::table[1]")

    # Signal row by name
    SIGNAL_ROW = (
        By.XPATH,
        "//tr[td[normalize-space()='Voltage']]"
    )

    # Add button for specific signal
    ADD_SIGNAL_BTN = (
        By.XPATH,
        "//tr[td[normalize-space()='Voltage']]//button[normalize-space()='Add']"
    )

    RESET_STAGING_BTN = (By.XPATH, "//button[normalize-space()='Reset Staging']")
    SAVE_ALL_CHANGES_BTN = (By.XPATH, "//button[normalize-space()='Save all changes']")
    CANCEL_BTN = (By.XPATH, "//button[normalize-space()='Cancel']")

    SAVE_SUCCESS_TOAST = (By.XPATH, "//div[contains(text(),'Saved changes')]")
    MANAGE_CONNECTION_BTN = (By.XPATH, "//button[normalize-space()='Manage Connection']")

    MAP_BTN = (By.XPATH, "//button[normalize-space()='Map']")

    REGISTER_40001_CHECKBOX = (
    By.XPATH,
    "//div[@role='dialog']//div[.//div[text()='40001']]//button[@role='checkbox']"
)

    MAP_SELECTED_BTN = (By.XPATH, "//button[normalize-space()='Map Selected' and not(@disabled)]")
    MAP_DISABLED_BTN = (By.XPATH, "//button[normalize-space()='Map Selected' and @disabled]")


class DeviceLocators:
    SIDE_PANEL_DEVICES = (By.XPATH, "//a[.//span[text()='Devices']]")
    ADD_DEVICE_BUTTON = (By.XPATH, "//button[contains(text(), '+ Add Device')]")
    DEVICE_NAME_INPUT = (By.XPATH, "//input[@placeholder='Enter device name']")
    DEVICE_DESCRIPTION_INPUT = (By.XPATH, "//textarea[@placeholder='Enter description']")
    SAVE_DEVICE_BUTTON = (By.XPATH, "//button[@type='submit' and contains(text(),'Save Device')]")
    CANCEL_DEVICE_BUTTON = (By.XPATH, "//button[@type='button' and contains(text(),'Cancel')]")
    SEARCH_DEVICES_INPUT = (By.XPATH, "//input[@placeholder='Search devices...']")

    # ---------------- Dynamic locators ----------------
    @staticmethod
    def DEVICE_IN_TABLE(device_name):
        return (By.XPATH, f"//td[text()='{device_name}']")
    
    @staticmethod
    def DELETE_BUTTON(device_name):
        return (By.XPATH, f"//tr[.//td[contains(normalize-space(.), '{device_name}')]]//button[contains(., 'Delete')]")

    @staticmethod
    def EDIT_BUTTON(device_name):
        return (By.XPATH, f"//tr[.//td[contains(normalize-space(.), '{device_name}')]]//button[contains(., 'Edit')]")

    @staticmethod
    def CONFIG_BUTTON(device_name):
        return (By.XPATH, f"//tr[.//td[contains(normalize-space(.), '{device_name}')]]//button[contains(., 'Config')]")

    CONFIRM_DELETION_TITLE = (By.XPATH, "//h2[contains(text(), 'Confirm Deletion')]")
    DELETE_POPUP_DEVICE_NAME = (By.XPATH, "//p[contains(text(),'Are you sure')]/span")
    NO_KEEP_IT_BUTTON = (By.XPATH, "//button[contains(text(), 'No, Keep it')]")
    YES_DELETE_IT_BUTTON = (By.XPATH, "//button[contains(text(), 'Yes, Delete it')]")

    # Edit Page
    EDIT_HEADER = (By.XPATH, "//div[text()='Edit Device & Configuration']")
    
    DEVICE_NAME = (By.ID, "name")
    DEVICE_DESC = (By.ID, "description")
    PROTOCOL = (By.XPATH, "//button[@role='combobox']")

    CONFIG_NAME_EDIT = (By.ID, "configName")
    POLL_INTERVAL_EDIT = (By.ID, "pollInterval")
    IP_ADDRESS_EDIT = (By.NAME, "IpAddress")
    PORT_EDIT = (By.NAME, "Port")

    BACK_TO_DEVICES = (By.XPATH, "//button[normalize-space(.)='Back to Devices']")
    SAVE_CHANGES = (By.XPATH, "//button[@type='submit' and normalize-space(.)='Save Changes']")

    # Config Page
    CONFIG_HEADER = (By.XPATH, "//div[text()='Configure Device']")

    CONFIG_NAME = (By.ID, "configName")
    POLL_INTERVAL = (By.ID, "pollInterval")
    IP_ADDRESS = (By.ID, "IpAddress")
    PORT = (By.ID, "Port")

    BACK_CONFIG = (By.XPATH, "//button[normalize-space(.)='Back']")
    SAVE_CONFIG = (By.XPATH, "//button[@type='submit' and normalize-space(.)='Save Configuration']")


# slave

    @staticmethod
    def SLAVE_BUTTON(device_name):
        return (
        By.XPATH,
        f"//tr[td[normalize-space()='{device_name}']]"
        "//span[contains(@class,'slave-device-btn') and normalize-space()='Slave']/ancestor::button"
    )

    SLAVE_MANAGER_TITLE = (By.XPATH, "//h1[normalize-space()='Slave Manager']")
    SLAVE_MANAGER_SUBTITLE = (By.XPATH, "//p[normalize-space()='Modbus Slave / Registers Configuration']")

    NEW_SLAVE_BUTTON = (By.XPATH, "//button[.//text()[normalize-space()='New Slave']]")

    NO_SLAVES_TEXT = (By.XPATH, "//p[normalize-space()='No slaves yet']")

    SELECT_SLAVE_TEXT = (By.XPATH, "//p[normalize-space()='Select a Slave']")

    SLAVE_HEADER = (By.XPATH, "//h2[normalize-space()='Slave 1']")

    NO_REGISTERS_TEXT = (By.XPATH, "//p[normalize-space()='No registers configured']")

    STATUS_BADGE = (By.XPATH, "//div[contains(@class,'rounded-full') and normalize-space()='Healthy']")
    ADD_REGISTER_BTN = (By.XPATH, "//button[.//text()[normalize-space()='Add Register']]")
    SAVE_SLAVE_BTN = (By.XPATH, "//button[.//text()[normalize-space()='Save Slave']]")


    # Popup
    ADD_REG_POPUP = (By.XPATH, "//h3[normalize-space()='Add Register']")
    CLOSE_POPUP = (By.XPATH, "//h3[normalize-space()='Add Register']/ancestor::div//button[.//*[name()='svg' and contains(@class,'lucide-x')]]")

    # Fields
    REGISTER_TYPE = (By.XPATH, "//label[normalize-space()='Register Type']/following-sibling::button")
    SIGNAL_DROPDOWN = (By.XPATH, "//label[contains(normalize-space(),'Signal')]/following-sibling::button")
    DISPLAY_ADDRESS = (By.XPATH, "//label[contains(.,'Display Address')]/following-sibling::input")
    REG_LENGTH = (By.XPATH, "//label[normalize-space()='Register Length']/following-sibling::input")
    DATA_TYPE = (By.XPATH, "//label[normalize-space()='Data Type']/following-sibling::button")
    SCALE = (By.XPATH, "//label[normalize-space()='Scale Factor']/following-sibling::input")
    UNIT = (By.XPATH, "//label[normalize-space()='Unit']/following-sibling::button")
    BYTE_ORDER = (By.XPATH, "//label[contains(normalize-space(),'Byte Order')]/following-sibling::button")

    # Flags
    WORD_SWAP = (By.XPATH, "//label[normalize-space()='Word Swap']/preceding-sibling::button")
    HEALTHY_CHK = (By.XPATH, "//label[normalize-space()='Healthy']/preceding-sibling::button")

    # Popup buttons
    POPUP_SAVE = (By.XPATH, "//button[contains(.,'Add Register')]")
    POPUP_CANCEL = (By.XPATH, "//button[normalize-space()='Cancel']")

    SUBSCRIBE_BUTTON = (By.XPATH, "//button[normalize-space()='Subscribe']")

    IMPORT_BULK_BUTTON = (By.ID, "import-bulk-btn")
    UPLOAD_CARD = (By.XPATH, "//div[.//div[text()='Upload CSV / Excel']]")
    FILE_INPUT = (By.CSS_SELECTOR, "input[type='file']")
    CHOOSE_FILE_BUTTON = (By.XPATH, "//button[contains(text(),'Choose file')]")
    CLEAR_FILE_BUTTON = (By.XPATH, "//button[contains(text(),'Clear')]")
    SAVE_DEVICES_BUTTON = (By.XPATH, "//button[contains(text(),'Save Devices')]")
    CSV_READY_MESSAGE = (By.XPATH, "//div[contains(text(),'ready to upload')]")
    UPLOAD_SUCCESS_TOAST = (By.XPATH, "//div[contains(text(),'Device bulk upload completed')]")

class ManageUserLocators:
    # Sidebar link
    SIDE_PANEL_MANAGE_USER = (By.ID, "sidebar-manage-user")

    # Page header
    PAGE_HEADER = (By.XPATH, "//h1[text()='User Management']")
    PAGE_SUBHEADER = (By.XPATH, "//p[text()='Manage application users']")

    # Search input
    SEARCH_USER_INPUT = (By.XPATH, "//input[@placeholder='Search users...']")

    # Download CSV button
    DOWNLOAD_CSV_BUTTON = (By.XPATH, "//button[contains(text(), 'Download CSV')]")

    # User table
    USER_TABLE = (By.ID, "user-table")
    USER_TABLE_ROWS = (By.XPATH, "//table[contains(@class,'w-full')]/tbody/tr")

    # Table columns inside a row
    USERNAME_CELL = ".//td[1]"
    EMAIL_CELL = ".//td[2]"
    ROLE_DROPDOWN = ".//td[3]//select"
    ACTIONS_CELL = ".//td[4]"
    DELETE_USER_BUTTON = ".//td[4]//button[contains(text(),'Delete')]"

    # Delete confirmation modal
    DELETE_MODAL_HEADER = (By.XPATH, "//h2[contains(text(),'Confirm Delete')]")
    DELETE_MODAL_USERNAME = (By.XPATH, "//p[contains(text(),'Are you sure you want to delete')]/span")
    DELETE_MODAL_CANCEL_BUTTON = (By.XPATH, "//button[text()='Cancel']")
    DELETE_MODAL_CONFIRM_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Delete')]")

    PREVIOUS_PAGE_BUTTON = (By.XPATH, "//a[@aria-label='Go to previous page']")
    NEXT_PAGE_BUTTON = (By.XPATH, "//a[@aria-label='Go to next page']")
    CURRENT_PAGE = (By.XPATH, "//ul[contains(@class,'flex') and contains(@class,'gap')]//a[@aria-current='page']")
    PAGE_NUMBERS = (By.XPATH, "//ul[@class='flex flex-row items-center gap-1']//a[not(@aria-label)]")
    
    def page_number_locator(page_num):
        return (By.XPATH, f"//ul[@class='flex flex-row items-center gap-1']//a[text()='{page_num}']")






    

class SignalLocators:

    SIGNAL_MENU = (By.ID, "sidebar-signal")
    # Time Range dropdown
    TIME_RANGE_DROPDOWN = (
        By.XPATH,
        "//div[contains(@class,'tour-time-range')]//select"
    )

    # Main Asset dropdown
    MAIN_ASSET_DROPDOWN = (
        By.XPATH,
        "//select[contains(@class,'tour-main-asset-dropdown')]"
    )

    # Signals button
    SIGNALS_BUTTON = (
        By.XPATH,
        "//label[contains(text(),'Signals')]/following::button[1]"
    )

    # Assigned Device value text
    ASSIGNED_DEVICE_VALUE = (
        By.XPATH,
        "//label[contains(@class,'tour-main-device')]/following-sibling::p/span"
    )

    # Compare Asset dropdown
    COMPARE_ASSET_DROPDOWN = (
        By.XPATH,
        "//select[contains(@class,'tour-compare-dropdown')]"
    )

    # Signals graph empty state text
    GRAPH_NO_DATA_TEXT = (
        By.XPATH,
        "//div[contains(@class,'tour-graph-card')]//p[contains(text(),'No data available')]"
    )    


# User Guide / Dashboard Tour Locators
class TourLocators:
    # Start Tour button on any card
    START_TOUR_BTN = (By.XPATH, "//button[@title='Start Tour']")

    # Popover container
    POPOVER_CONTAINER = (By.XPATH, "//div[contains(@class,'driver-popover')]")

    # Popover title and description
    POPOVER_TITLE = (By.XPATH, "//header[@id='driver-popover-title']")
    POPOVER_DESCRIPTION = (By.XPATH, "//div[@id='driver-popover-description']")

    # Popover navigation buttons
    NEXT_BTN = (By.XPATH, "//button[contains(@class,'driver-popover-next-btn')]")
    PREV_BTN = (By.XPATH, "//button[contains(@class,'driver-popover-prev-btn')]")
    CLOSE_BTN = (By.XPATH, "//button[contains(@class,'driver-popover-close-btn')]")


class ReportsLocators:

    REPORTS_MENU = (By.ID, "sidebar-reports")