import time

from .base import FunctionalTest

TEST_EMAIL = "kevin@mockmyid.com"

class LoginTest(FunctionalTest):

    def test_login_with_persona(self):
        # Kevin goes to the awesome superlists site
        # and notices a "Sign in" link for the first time

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
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)

        # Refreshing the page, he sees it's a real session login,
        # not just a one-off for that page
        self.browser.refresh()
        self.wait_to_be_logged_in(TEST_EMAIL)

        # Terrified of this new feature, he reflexively clicks "logout"
        time.sleep(3)
        self.browser.find_element_by_id('id_logout').click()
        time.sleep(3)
        self.wait_to_be_logged_out(TEST_EMAIL)

        # The "logged out" status also persists after a refresh
        self.browser.refresh()
        self.wait_to_be_logged_out(TEST_EMAIL)
