from selenium import webdriver
from selenium.webdriver.chrome.service import Service

CHROMEDRIVER_PATH = './chromedriver/chromedriver.exe'

def load_selenium_driver():
    """Load and return the Selenium driver"""
    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH))
    return driver
