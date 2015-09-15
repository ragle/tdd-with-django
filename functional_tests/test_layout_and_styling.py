# Functional tests and user story for a simple "hello world" 
# to-do app created with Django
from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):

        # Ted navigates to the front page of his favorite quotes app
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # He sees that the input box is nicely centered, indicating the 
        # stylesheets are still loading correctly, and all is as it should be
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
                inputbox.location['x'] + inputbox.size['width'] / 2,
                512,
                delta=5
        )

        # Ted wonders, if he adds an item, will the 
        # new item page page also display properly?
        inputbox.send_keys('testing\n')
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
                inputbox.location['x'] + inputbox.size['width'] / 2,
                512,
                delta=5
        )
