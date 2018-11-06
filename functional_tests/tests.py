from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
#import unittest

from django.test import LiveServerTestCase

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        path = "C:\\ProgramData\\Anaconda3-5.2.0\\BrowersDriver\\chromedriver.exe"
        self.browser = webdriver.Chrome(path)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows],
                      f"{row_text} didnt't apears in table. Ccontent were:\n{table.text}"
                      )
    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith had heard of  a new todo-list online app,
        # she goes to check it out
        # at the home page link
        self.browser.get(self.live_server_url)

        # she notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # she is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # she types Buy peacock feathers into a text box
        inputbox.send_keys('Buy peacock feathers')

        # when she hits enter, know the page updates and
        # it shows now
        # 1: Buy peacock feathers
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_table('1: Buy peacock feathers')

        # there is still a text box inviting her to enter
        # another item


        # she enters Use peacock feathers to make a fly
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)


        # the page updates again and the page shows both items now
        self.check_for_row_in_table('1: Buy peacock feathers')
        self.check_for_row_in_table('2: Use peacock feathers to make a fly')
        self.fail('Finish the test moran!!!')
        # than she sees that the site generated a unique url for her

        # she visits the url and at her joy, she finds out that
        # the site is in fact remembering all her to-do list

        # satisfied, she goes to sleep

