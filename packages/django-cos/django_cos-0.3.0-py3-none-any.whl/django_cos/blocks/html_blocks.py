"""
HTML blocks are simple blocks used to represent common HTML elements,
with additional styling and attributes.
"""
# Django Imports
from django.utils.translation import ugettext_lazy as _
# Wagtail Imports
from wagtail.core import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock as WagtailTableBlock
# Django COS Imports
from django_cos.blocks import mixins
from django_cos.blocks.base_blocks import (
    BaseBlock, BaseLinkBlock,
    DjangoCOSAdvTrackingSettings, LinkStructValue
)

class ButtonBlock(mixins.ButtonMixin, BaseLinkBlock):
    """
    A link styled as a button.
    """
    class Meta:
        template = 'django_cos/blocks/button_block.html'
        icon = 'fa-hand-pointer-o'
        label = _('Button Link')
        value_class = LinkStructValue


class DownloadBlock(mixins.ButtonMixin, BaseBlock):
    """
    Link to a file that can be downloaded.
    """
    automatic_download = blocks.BooleanBlock(
        required=False,
        label=_('Auto download'),
    )
    downloadable_file = DocumentChooserBlock(
        required=False,
        label=_('Document link'),
    )

    advsettings_class = DjangoCOSAdvTrackingSettings

    class Meta:
        template = 'django_cos/blocks/download_block.html'
        icon = 'download'
        label = _('Download')


class EmbedGoogleMapBlock(BaseBlock):
    """
    An embedded Google map in an <iframe>.
    """
    search = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Search query'),
        help_text=_('Address or search term used to find your location on the map.'),
    )
    place_id = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Google place ID'),
        help_text=_('Requires API key to use place ID.')
    )
    map_zoom_level = blocks.IntegerBlock(
        required=False,
        default=14,
        label=_('Map zoom level'),
        help_text=_('Requires API key to use zoom. 1: World, 5: Landmass/continent, 10: City, 15: Streets, 20: Buildings')
    )

    class Meta:
        template = 'django_cos/blocks/google_map.html'
        icon = 'fa-map'
        label = _('Google Map')


class EmbedVideoBlock(BaseBlock):
    """
    Emedded media using stock wagtail functionality.
    """
    url = EmbedBlock(
        required=True,
        label=_('URL'),
        help_text=_('Link to a YouTube/Vimeo video, tweet, facebook post, etc.')
    )

    class Meta:
        template = 'django_cos/blocks/embed_video_block.html'
        icon = 'media'
        label = _('Embed Media')


class H1Block(BaseBlock):
    """
    An <h1> heading.
    """
    text = blocks.CharBlock(
        max_length=255,
        label=_('Text'),
    )

    class Meta:
        template = 'django_cos/blocks/h1_block.html'
        icon = 'fa-header'
        label = _('Heading 1')


class H2Block(BaseBlock):
    """
    An <h2> heading.
    """
    text = blocks.CharBlock(
        max_length=255,
        label=_('Text'),
    )

    class Meta:
        template = 'django_cos/blocks/h2_block.html'
        icon = 'fa-header'
        label = _('Heading 2')


class H3Block(BaseBlock):
    """
    An <h3> heading.
    """
    text = blocks.CharBlock(
        max_length=255,
        label=_('Text'),
    )

    class Meta:
        template = 'django_cos/blocks/h3_block.html'
        icon = 'fa-header'
        label = _('Heading 3')


class TableBlock(BaseBlock):
    table = WagtailTableBlock()

    class Meta:
        template = 'django_cos/blocks/table_block.html'
        icon = 'fa-table'
        label = 'Table'

class ImageBlock(mixins.ImageMixin):
    """
    An <img>, by default styled responsively to fill its container.
    """
    class Meta:
        template = 'django_cos/blocks/image/base.html'
        icon = 'image'
        label = _('Image')
        value_class = LinkStructValue

class BackgroundImageBlock(mixins.BackgroundImageMixin):
    """
    An image to be supplied to the background CSS attribute or 
    lazily loaded through lazysizes.
    """

class ImageGalleryBlock(BaseBlock):
    """
    Show a collection of images with interactive previews that expand to
    full size images in a modal.
    """
    images = blocks.ListBlock(
        blocks.StructBlock([
            ('image', ImageBlock()),
            ('text', blocks.TextBlock(required=False)),
        ])
    )

    class Meta:
        template = 'django_cos/blocks/gallery/image.html'
        icon = 'image'
        label = _('Image Gallery')

class QuoteBlock(BaseBlock):
    """
    A <blockquote>.
    """
    text = blocks.TextBlock(
        required=True,
        rows=4,
        label=_('Quote Text'),
    )
    citation = blocks.URLBlock(
        required=False,
        max_length=2000,
        label=_('Citation'),
        help_text=_('The URI of this quotation.')
    )
    author = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Author'),
    )

    class Meta:
        template = 'django_cos/blocks/quote_block.html'
        icon = 'openquote'
        label = _('Quote')
