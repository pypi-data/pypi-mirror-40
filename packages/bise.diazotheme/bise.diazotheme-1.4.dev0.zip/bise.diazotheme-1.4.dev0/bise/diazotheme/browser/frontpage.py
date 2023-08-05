""" Views and utilities for frontpage
"""

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class NewsListing(BrowserView):
    """ News listing for frontpage"""

    listing_template = ViewPageTemplateFile("pt/simplified-listing.pt")


    def render_listing(self, collection):
        """ Render summary box

        @return: Resulting HTML code as Python string
        """
        return self.listing_template(collection=collection)

    def provider(self, listobj):
        return listobj.Subject
