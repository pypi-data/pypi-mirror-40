from ZODB.POSException import ConflictError
from ZPublisher.interfaces import IPubAfterTraversal
from plone.transformchain.interfaces import DISABLE_TRANSFORM_REQUEST_KEY
from zope.component import adapter
import logging

logger = logging.getLogger('bise.diazotheme')


@adapter(IPubAfterTraversal)
def disable_diazo_for_templates(event):
    """ Code modeled after plone.app.caching.hooks.intercept
    """
    try:
        request = event.request
        if not ("/cat-client/template" in request.getURL()):
            return

        if DISABLE_TRANSFORM_REQUEST_KEY not in request.environ:
            request.environ[DISABLE_TRANSFORM_REQUEST_KEY] = True

    except ConflictError:
        raise
    except:
        logging.exception(
            "Swallowed exception in bise.diazotheme "
            "IPubAfterTraversal event handler")
