from lxml.html import fromstring

from Products.Five import BrowserView


class DetectImageLinks(BrowserView):
    """ Detect outgoing images in website
    """

    def _has_http_images(self, text):
        e = fromstring(text)
        imgs = e.xpath('//img/@src')

        for img in imgs:
            if 'http://' in img:
                if self.request.base not in img:
                    print(img)

                    return True

        return False

    def __call__(self):
        catalog = self.context.portal_catalog

        brains = catalog.searchResults(portal_type="FolderishPage")

        broken = []

        for brain in brains:

            obj = brain.getObject()

            if not obj.text:
                continue

            text = obj.text.output

            if self._has_http_images(text):
                broken.append(brain.getURL())

        return "\n".join(broken)
