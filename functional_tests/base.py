from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import os

MAX_WAIT = 10

def waiting_decorator(fun):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return_value = fun(*args, **kwargs)
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
        return return_value

    return wrapper

class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        path = "C:\\ProgramData\\Anaconda3-5.2.0\\BrowersDriver\\chromedriver.exe"
        self.browser = webdriver.Chrome(path)

        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://'+staging_server


    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)


