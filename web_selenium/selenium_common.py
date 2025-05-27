from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as geckoOptions
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.mobile import Mobile

from time import sleep
import sys

web_driver = "chrome"


def gecko_setup():
    options = geckoOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    if sys.platform.startswith('linux'):  # any linux 64bit
        browser = webdriver.Firefox(
            executable_path="./drivers/linux/geckodriver", options=options)
    elif sys.platform.startswith('darwin'):  # any macos
        browser = webdriver.Firefox(
            executable_path="./drivers/macos/geckodriver", options=options)
    elif sys.platform.startswith('cygwin'):  # any windows 64bit
        browser = webdriver.Firefox(
            executable_path="./drivers/windows/geckodriver.exe", options=options)
    return browser


def chrome_setup():
    options = chromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    if sys.platform.startswith('linux'):  # any linux 64bit
        browser = webdriver.Chrome(
            executable_path="./drivers/linux/chromedriver", options=options)
    elif sys.platform.startswith('darwin'):  # any macos
        browser = webdriver.Chrome(
            executable_path="./drivers/macos/chromedriver", options=options)
    elif sys.platform.startswith('cygwin'):  # any windows 64bit
        browser = webdriver.Chrome(
            executable_path="./drivers/windows/chromedriver.exe", options=options)
    return browser


def init_selenium():
    if web_driver == "firefox":
        browser = gecko_setup()
    elif web_driver == "chrome":
        browser = chrome_setup()
    return browser

if __name__ == "__main__":
    init_selenium()
