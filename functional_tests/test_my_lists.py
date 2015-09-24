from django.conf import settings
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session

TEST_EMAIL = 'edith@mockmyid.com'

class MyListsTest(FunctionalTest):

    # n.b. - dead code until the login / session issue is pinned down...
    def create_pre_authenticated_session(self, email):
        if self.against_staging:
            session_key = create_session_on_server(self.server_host, email)
        else:
            session_key = create_pre_authenticated_session(email)
        self.browser.get(self.server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name = settings.SESSION_COOKIE_NAME,
            value = session_key,
            path='/',
            )
        )

    def get_list_name(self, input):
        return " ".join(input.split(" ")[0:5]).strip() + "..."

    def test_logged_in_users_lists_are_saved_as_my_lists(self):

        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_login').click()

        # A persona login box appears
        self.switch_to_new_window('Mozilla Persona')

        # Kevin logins in with his email address
        ## Use mockmyid.com for test email
        self.browser.find_element_by_id(
                'authentication_email'
        ).send_keys(TEST_EMAIL)
        self.browser.find_element_by_tag_name('button').click()

        # The persona window closes
        self.switch_to_new_window('Quotable')

        # He can see that he is logged in
        self.wait_for_element_with_id('id_logout')

        # edith is a logged-in user
        #self.create_pre_authenticated_session(email)

        # she goes to the home page and starts a list
        self.browser.get(self.server_url)
        first_input = "To be or not to be\n"
        second_input = "That is the question\n"
        self.get_item_input_box().send_keys(first_input)
        self.get_item_input_box().send_keys(second_input)
        first_list_url = self.browser.current_url

        # she notices a "My lists" link, for the first time.
        self.browser.find_element_by_link_text('My Lists').click()

        # she sees that her list is in there, named according to its 
        # first list item
        self.browser.find_element_by_link_text(
                self.get_list_name(first_input)
        ).click()
        self.assertEqual(self.browser.current_url, first_list_url)

        # she decides to start another list, to see what happens
        self.browser.get(self.server_url)
        third_input = "tis blah blah blah\n"
        self.get_item_input_box().send_keys(third_input)
        second_list_url = self.browser.current_url

        # under "my lists" her new list appears
        self.browser.find_element_by_link_text('My Lists').click()
        self.browser.find_element_by_link_text(
                self.get_list_name(third_input)
        ).click()
        self.assertEqual(self.browser.current_url, second_list_url)

        # she logs out. The "My lists" option disappears
        self.browser.find_element_by_id('id_logout').click()
        self.assertEqual(
                self.browser.find_elements_by_link_text('My lists'),
                []
        )
