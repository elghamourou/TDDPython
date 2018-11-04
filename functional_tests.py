from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        path = "C:\\ProgramData\\Anaconda3-5.2.0\\BrowersDriver\\chromedriver.exe"
        self.browser = webdriver.Chrome(path)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith had heard of  a new todo-list online app,
        # she goes to check it out
        # at the home page link
        self.browser.get("http://localhost:8000")

        # she notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test')

        # she is invited to enter a to-do item straight away

        # she types Buy peacock feathers into a text box

        # when she hits enter, know the page updates and
        # it shows now
        # 1: Buy peacock feathers

        # there is still a text box inviting her to enter
        # another item

        # she enters Use peacock feathers to make a fly

        # the page updates again and the page shows both items now

        # than she sees that the site generated a unique url for her

        # she visits the url and at her joy, she finds out that
        # the site is in fact remembering all her to-do list

        # satisfied, she goes to sleep


if __name__ == '__main__':
    unittest.main()
