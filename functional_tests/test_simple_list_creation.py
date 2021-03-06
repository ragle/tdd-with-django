# Functional tests and user story for a simple "hello world" 
# to-do app created with Django

from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self): 
        # Ted visits the quotes app         
        self.browser.get(self.server_url)

        # He notices the page title and header are related to quotes
        self.assertIn('Quotable', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Quotes', header_text)

        
        # He is invited to enter a quote straight away
        inputbox = self.get_item_input_box()
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Add your quote here...'
        )

        
        # He types "To be or not to be" and presses enter
        first_input = 'To be or not to be'
        inputbox.send_keys(first_input)
        inputbox.send_keys(Keys.ENTER)

        
        # When Ted hits enter, he is taken to a new URL
        # Now the page lists:
        # "1: To be or not to be"
        # as a quote in the quotes table
        gawkdar_list_url = self.browser.current_url
        self.assertRegex(gawkdar_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: '+ first_input)
        
        
        # There is still a text box inviting him to enter another quote
        # He types "that is the question"
        inputbox = self.get_item_input_box()
        second_input = 'that is the question'
        inputbox.send_keys(second_input)
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: ' + first_input)
        self.check_for_row_in_list_table('2: ' + second_input)

        # Ted quits, and goes to work
        self.browser.quit()

        # Ted tells Alice about the app. She opens up her browser...
        self.browser = webdriver.Firefox()

       
        # Alice visits the app. She doesn't see Ted's quotes
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(first_input, page_text)
        self.assertNotIn(second_input, page_text)

       
        # Alice starts a list of quotes of her own
        inputbox = self.get_item_input_box()
        third_input = 'Go Yankees'
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

