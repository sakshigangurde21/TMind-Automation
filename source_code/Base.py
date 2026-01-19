import os
import unittest
from selenium import webdriver
from dotenv import load_dotenv
import allure
from datetime import datetime

load_dotenv()

class Base(unittest.TestCase):
    driver = None
    screenshot_path = None

    @classmethod
    def start_driver(cls):
        download_path = os.path.join(os.getcwd(), "Downloads")

        cls.screenshot_path = os.path.join(os.getcwd(), "Screenshots")
        os.makedirs(cls.screenshot_path, exist_ok=True)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = "/usr/bin/chromium"
        chrome_options.add_argument("--headless=new")
        prefs = {"download.default_directory": download_path}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        cls.driver = webdriver.Chrome(options=chrome_options)
        # cls.driver.maximize_window()
        # cls.driver.get(os.environ.get("BASE_URL"))
        return cls.driver

    def attach_screenshot(self, suffix=""):
        try:
            driver = self.__class__.driver
            if driver and driver.session_id:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                test_name = self._testMethodName
                screenshot_name = f"{test_name}{suffix}_{timestamp}.png"
                screenshot_file = os.path.join(
                    self.__class__.screenshot_path, screenshot_name)

                driver.save_screenshot(screenshot_file)
                allure.attach.file(
                    screenshot_file,
                    name=screenshot_name,
                    attachment_type=allure.attachment_type.PNG
                )
                return screenshot_file
        except Exception as e:
            print(f"Screenshot capture failed: {e}")
        return None

    @classmethod
    def quit_driver(cls):
        if cls.driver:
            try:
                cls.driver.quit()
                cls.driver = None
            except Exception as e:
                print(f"Error quitting driver: {e}")
