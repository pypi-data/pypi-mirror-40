""" Generic view tile, uses a view name to render content
"""

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from zope import schema
from zope.component import queryMultiAdapter
from zope.interface import implements
import logging

logger = logging.getLogger('bise.diazotheme')


class ILiveTile(IPersistentCoverTile):

    title = schema.TextLine(
        title=u'Title',
        required=True,
    )

    view_name = schema.TextLine(
        title=u'View name',
        required=True,
    )


class LiveTile(PersistentCoverTile):
    """ Generic view tile
    """

    implements(ILiveTile)

    index = ViewPageTemplateFile('pt/live.pt')

    is_configurable = True
    is_editable = True
    is_droppable = False
    short_name = u'Live Tile'

    def is_empty(self):
        return False

    def render_inner_view(self):
        view_name = self.data.get('view_name')
        if not view_name:
            return ""

        view = queryMultiAdapter((self.context, self.request), name=view_name)
        if not view:
            view = self.context.aq_parent[view_name]
        return view and view() or ""
