# Functional tests and user story for a simple "hello world" 
# to-do app created with Django

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
        
    def test_can_start_a_list_and_retrieve_it_later(self): 
        # Ted visits the to-do app         
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        
        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )

        
        # He types "eat Twizlers" and presses enter
        first_input = 'eat Twizlers'
        inputbox.send_keys(first_input)
        inputbox.send_keys(Keys.ENTER)

        
        # When Ted hits enter, he is taken to a new URL
        # Now the page lists:
        # "1: eat twizlers"
        # as an item in a to-do list table
        gawkdar_list_url = self.browser.current_url
        self.assertRegex(gawkdar_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: '+ first_input)
        
        
        # There is still a text box inviting him to enter another item
        # He types "dispose of packaging responsibly" and presses enter
        inputbox = self.browser.find_element_by_id('id_new_item')
        second_input = 'dispose of packaging responsibly'
        inputbox.send_keys(second_input)
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: ' + first_input)
        self.check_for_row_in_list_table('2: ' + second_input)

        # Ted quits, and goes to work
        self.browser.quit()

        # Ted tells Alice about the app. She opens up her browser...
        self.browser = webdriver.Firefox()

       
        # Alice visits the app. She doesn't see Ted's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(first_input, page_text)
        self.assertNotIn(second_input, page_text)

       
        # Alice starts a to do list of her own
        inputbox = self.browser.find_element_by_id('id_new_item')
        third_input = 'Go for a jog'
        inputbox.send_keys(third_input)
        inputbox.send_keys(Keys.ENTER)


        # Alice sees that she's been given her own URL for her new list
        tommy_list_url = self.browser.current_url
        self.assertRegex(tommy_list_url, '/lists/.+')
        self.assertNotEqual(tommy_list_url, gawkdar_list_url)

       
        # And that there is no trace of ted's list to be found
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(first_input, page_text)
        self.assertIn(third_input, page_text)

    def test_layout_and_styling(self):

        # Ted navigates to the front page of his favorite to-do list app
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # He sees that the input box is nicely centered, indicating the 
        # stylesheets are still loading correctly, and all is as it should be
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
                inputbox.location['x'] + inputbox.size['width'] / 2,
                512,
                delta=5
        )

        # Ted wonders, if he adds an item, will the 
        # new item page page also display properly?
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
                inputbox.location['x'] + inputbox.size['width'] / 2,
                512,
                delta=5
        )
