from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from unittest import skip


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_item(self):

        # Edith connects to the application and accidentally enters an empty list item
        # but the application didn't save the empty item
        # and instead shows an error message informing her that an empty list item is not acceptable
        # and the application gives the handle to her to enter a new item

        # she enters a new item text
        # the item is correctly saved
        # the page refresh and the error message is no longer here

        # she now tries to deliberately enters an empty item
        # like before the page refreshes with the error message showing again
        # no empty message is saved
        # she tries again with an empty text, and again the page refresh with the error message
        # no empty item is saved

        self.fail('write me')