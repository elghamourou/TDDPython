from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from unittest import skip


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_item(self):

        # Edith connects to the application and accidentally enters an empty list item
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        # but the application didn't save the empty item
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertNotIn("1: ", [row.text for row in rows])
        # and instead shows an error message informing her that an empty list item is not acceptable

        self.wait_for(lambda:self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text,
                         "You can't have an empty list item"))
        # and the application gives the handle to her to enter a new item
        input_box = self.browser.find_element_by_id('id_new_item')



        # she enters a new item text
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Correct not empty text')
        inputbox.send_keys(Keys.ENTER)
        # the item is correctly saved
        self.wait_for_row_in_list_table('1: Correct not empty text')
        # the page refresh and the error message is no longer here

        # she now tries to deliberately enters an empty item
        # like before the page refreshes with the error message showing again
        # no empty message is saved
        # she tries again with an empty text, and again the page refresh with the error message
        # no empty item is saved

        # she enters a text into the input box and it is saved correctly now
