"""
This module contains shared fixtures.
"""

import json
import pytest
import selenium.webdriver


BROWSERS = ['Firefox', 'Chrome', 'Headless Chrome']


@pytest.fixture(scope='session')
def config():
    with open('config.json') as config_file:
        config = json.load(config_file)

    assert config['browser'] in BROWSERS
    assert isinstance(config['implicit_wait'], int)
    assert config['implicit_wait'] > 0

    return config


@pytest.fixture
def driver(config):
    browser = config['browser']
    if browser == 'Firefox':
        d = selenium.webdriver.Firefox()
    elif browser == 'Chrome':
        d = selenium.webdriver.Chrome()
    elif browser == 'Headless Chrome':
        opts = selenium.webdriver.ChromeOptions()
        opts.add_argument('headless')
        d = selenium.webdriver.Chrome(options=opts)
    else:
        raise Exception(f'Browser {browser} is not supported')

    d.implicitly_wait(config['implicit_wait'])

    yield d

    d.quit()