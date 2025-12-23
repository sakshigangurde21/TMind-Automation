import os
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv  

load_dotenv()  

class Base(unittest.TestCase):
    driver = None
    
    def start_driver(self):
        # Create Downloads folder path inside project
        download_path = os.path.join(os.getcwd(), "Downloads")
        chrome_options = webdriver.ChromeOptions()

        prefs = {"download.default_directory": download_path}
        chrome_options.add_experimental_option("prefs", prefs)

        # chrome_options.add_argument("--headless=new")   # headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        self.driver = webdriver.Chrome(options=chrome_options)     # Initialize Chrome
        self.driver.maximize_window()

        return self.driver

    def quit_driver(self):
        if self.driver:
            self.driver.quit()
