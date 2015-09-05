# Functional tests and user story for a simple "hello world" 
# to-do app created with Django

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class NewVisitorTest(LiveServerTestCase):

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
        # GAWKDAR, the 11-dimensional ET from the number 25 has telepathically 
        # become aware of a cool new online to do app. THIS PLEASES GAWKDAR.
        # GAWKDAR navigates to the app's home page.
        self.browser.get(self.live_server_url)

        # GAWKDAR notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        
        # GAWKDAR is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )

        
        # GAWKDAR types "INSTALL DELICIOUS EARTH TWIZLERS IN GAWKDAR HYPERSTOMACH"
        # and presses enter.
        first_input = 'INSTALL DELICIOUS EARTH TWIZLERS IN GAWKDAR HYPERSTOMACH'
        inputbox.send_keys(first_input)
        inputbox.send_keys(Keys.ENTER)

        
        # When GAWKDAR  hits enter, GAWKDAR is taken to a new url. 
        # Now the page lists:
        # "1: INSTALL DELICIOUS EARTH TWIZLERS IN GAWKDAR HYPERSTOMACH"
        # as an item in a to-do list table
        gawkdar_list_url = self.browser.current_url
        self.assertRegex(gawkdar_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: '+ first_input)
        
        
        # There is still a text box inviting GAWKDAR to add another item.
        # GAWKDAR enters "DISPOSE OF EARTH SNACK PACKAGING IN GAWKDAR-APPROVED 
        # RECEPTICLE" 
        inputbox = self.browser.find_element_by_id('id_new_item')
        second_input = 'DISPOSE OF EARTH SNACK PACKAGING IN GAWKDAR-APPROVED'+\
                       ' RECEPTICLE'
        inputbox.send_keys(second_input)
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: ' + first_input)
        self.check_for_row_in_list_table('2: ' + second_input)

        
        # The page updates again and now shows both items on GAWKDAR'S list
        # GAWKDAR IS SUDDENLY CURIOUS!
        # If a HU-MAN goes to the website, will the HU-MAN be able to view
        # GAWKDAR's list? 
        # GAWKDAR reaches out into the ether, assumes control of a HU-MAN's 
        # body, and returns to the page
        self.browser.quit()
        self.browser = webdriver.Firefox()

        
        # The HU-MAN host Tommy visits the page. There is no sign of GAWKDAR's
        # plans to consume delicious earth snacks and dispose of waste 
        # responsibly.
        # THIS PLEASES GAWKDAR!
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(first_input, page_text)
        self.assertNotIn(second_input, page_text)

        
        # GAWKDAR senses that his HU-MAN host requires additional fiber in his
        # diet. GAWKDAR is not a monster. GAWKDAR helps the meat puppet create a
        # helpful to-do list of his own:
        inputbox = self.browser.find_element_by_id('id_new_item')
        third_input = 'Buy Rasin Bran'
        inputbox.send_keys(third_input)
        inputbox.send_keys(Keys.ENTER)


        # GAWKDAR sees that the HU-MAN has received his own URL
        tommy_list_url = self.browser.current_url
        self.assertRegest(francis_list_url, '/lists/.+')
        self.assertNotEqual(tommy_list_url, gawkdar_list_url)

        
        # and that there is no trace of GAWKDAR's list in the HU-MAN's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(first_input, page_text)
        self.assertIn(third_input, page_text)


        # Satisfied, GAWKDAR separates from the HU-MAN host and returns to a 
        # state of profound inner peace, in perfect harmony with the true nature 
        # of unconditioned reality.
        assert 1 == 1
