"""
This module contains DuckDuckGoResultPage,
the page object for the DuckDuckGo search result page.
"""
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class DuckDuckGoResultPage:
    RESULT_LINKS = (By.CSS_SELECTOR, 'a.result__a')
    SEARCH_INPUT = (By.ID, 'search_form_input')

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def result_link_titles(self) -> List[str]:
        links = self.driver.find_elements(*self.RESULT_LINKS)
        return [link.text for link in links]

    def search_input_value(self) -> str:
        search_input = self.driver.find_element(*self.SEARCH_INPUT)
        return search_input.get_attribute('value')

    def title(self) -> str:
        return self.driver.title;