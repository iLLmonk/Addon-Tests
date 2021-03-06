#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest

from unittestzero import Assert

from pages.desktop.home import Home
from pages.desktop.details import Details


class TestPaypal:

    addon_name = 'Firebug'

    @pytest.mark.login
    def test_that_user_can_contribute_to_an_addon(self, mozwebqa):
        """Test that checks the Contribute button for an add-on using PayPal."""

        addon_page = Home(mozwebqa)

        addon_page.login()
        Assert.true(addon_page.is_the_current_page)
        Assert.true(addon_page.header.is_user_logged_in)

        addon_page = Details(mozwebqa, self.addon_name)

        contribution_snippet = addon_page.click_contribute_button()
        paypal_frame = contribution_snippet.click_make_contribution_button()
        Assert.true(addon_page.is_paypal_login_dialog_visible)

        payment_popup = paypal_frame.login_to_paypal(user="paypal")
        Assert.true(payment_popup.is_user_logged_into_paypal)
        payment_popup.click_pay()
        Assert.true(payment_popup.is_payment_successful)
        payment_popup.close_paypal_popup()
        Assert.true(addon_page.is_the_current_page)

    def test_that_user_can_make_a_contribution_without_logging_into_amo(self, mozwebqa):
        """Test that checks if the user is able to make a contribution without logging in to AMO."""
        addon_page = Details(mozwebqa, self.addon_name)
        Assert.false(addon_page.header.is_user_logged_in)

        contribution_snippet = addon_page.click_contribute_button()
        paypal_frame = contribution_snippet.click_make_contribution_button()
        Assert.true(addon_page.is_paypal_login_dialog_visible)

        payment_popup = paypal_frame.login_to_paypal(user="paypal")
        Assert.true(payment_popup.is_user_logged_into_paypal)
        payment_popup.click_pay()
        Assert.true(payment_popup.is_payment_successful)
        payment_popup.close_paypal_popup()
        Assert.true(addon_page.is_the_current_page)

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_that_make_contribution_button_is_clickable_and_loads_paypal_frame_while_user_is_logged_out(self, mozwebqa):
        addon_page = Details(mozwebqa, self.addon_name)
        Assert.false(addon_page.header.is_user_logged_in)

        contribution_snippet = addon_page.click_contribute_button()

        Assert.true(contribution_snippet.is_make_contribution_button_visible)
        Assert.equal("Make Contribution", contribution_snippet.make_contribution_button_name)

        contribution_snippet.click_make_contribution_button()
        Assert.true(addon_page.is_paypal_login_dialog_visible)

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    @pytest.mark.login
    def test_that_make_contribution_button_is_clickable_and_loads_paypal_frame_while_user_is_logged_in(self, mozwebqa):
        addon_page = Details(mozwebqa, self.addon_name)
        addon_page.login()
        Assert.true(addon_page.is_the_current_page)
        Assert.true(addon_page.header.is_user_logged_in)

        contribution_snippet = addon_page.click_contribute_button()

        Assert.true(contribution_snippet.is_make_contribution_button_visible)
        Assert.equal("Make Contribution", contribution_snippet.make_contribution_button_name)

        contribution_snippet.click_make_contribution_button()
        Assert.true(addon_page.is_paypal_login_dialog_visible)
