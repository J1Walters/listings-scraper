from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

CHROMEDRIVER_PATH = './chromedriver/chromedriver.exe'
options = Options()
options.add_argument('--headless')

def load_selenium_driver():
    """Load and return the Selenium driver"""
    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
    return driver
