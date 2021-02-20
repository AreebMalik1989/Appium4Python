"""
This module contains DuckDuckGoSearchPage,
the page object for the DuckDuckGo search page.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class DuckDuckGoSearchPage:
    URL = 'https://www.duckduckgo.com'
    SEARCH_INPUT = (By.ID, 'search_form_input_homepage')

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def load(self) -> None:
        self.driver.get(self.URL)

    def search(self, phrase) -> None:
        search_input: WebElement = self.driver.find_element(*self.SEARCH_INPUT)
        search_input.send_keys(phrase + Keys.RETURN)
