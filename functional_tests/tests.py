from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException

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

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        path = "C:\\ProgramData\\Anaconda3-5.2.0\\BrowersDriver\\chromedriver.exe"
        self.browser = webdriver.Chrome(path)

    def tearDown(self):
        self.browser.quit()

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


    def check_for_row_in_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows],
                      f"{row_text} didnt't apears in table. Ccontent were:\n{table.text}"
                      )
    def test_can_start_a_list_for_one_user(self):
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

        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        #self.check_for_row_in_table('1: Buy peacock feathers')

        # there is still a text box inviting her to enter
        # another item


        # she enters Use peacock feathers to make a fly
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # the page updates again and the page shows both items now
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')


    def test_multiple_users_can_start_different_lists_at_different_urls(self):
        # Edith has heard about a cool new online To-Do app. She goes
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # then she sees that the site generated a unique url for her
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Now a new user , Francis, comes along to the site.

        ## we use a new browser session to ensure that no information
        ## of Edith's is comming through from cockies, etc...
        self.browser.quit()
        path = "C:\\ProgramData\\Anaconda3-5.2.0\\BrowersDriver\\chromedriver.exe"
        self.browser = webdriver.Chrome(path)

        #Francis visits the homepage, there is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        #Francis starts a new list by entring a new Item
        # he is less interresting than Edith
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        #Francis gets his own unique url
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        #again there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.asserttIn('Buy milk', page_text)


        # satisfied, they both goes to sleep
