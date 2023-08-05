"""
Layout blocks are essentially a wrapper around content.
e.g. rows, columns, hero units, etc.
"""
# Django Imports
from django.utils.translation import ugettext_lazy as _
# Wagtail Imports
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
# Django COS Imports
from django_cos.settings import cr_settings
from django_cos.blocks.html_blocks import BackgroundImageBlock, ImageBlock
from django_cos.blocks.base_blocks import BaseLayoutBlock, DjangoCOSAdvColumnSettings

### Level 1 layout blocks


class ColumnBlock(BaseLayoutBlock):
    """
    Renders content in a column.
    """
    column_size = blocks.ChoiceBlock(
        choices=cr_settings['FRONTEND_COL_SIZE_CHOICES'],
        default=cr_settings['FRONTEND_COL_SIZE_DEFAULT'],
        required=False,
        label=_('Column size'),
    )

    advsettings_class = DjangoCOSAdvColumnSettings

    class Meta:
        template = 'django_cos/blocks/column_block.html'
        icon = 'placeholder'
        label = 'Column'


class GridBlock(BaseLayoutBlock):
    """
    Renders a row of columns.
    """
    fluid = blocks.BooleanBlock(
        required=False,
        label=_('Full width'),
    )

    class Meta:
        template = 'django_cos/blocks/grid_block.html'
        icon = 'fa-columns'
        label = _('Responsive Grid Row')

    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(
            local_blocks = [
                ('content', ColumnBlock(local_blocks))
            ]
        )


class CardGridBlock(BaseLayoutBlock):
    """
    Renders a row of cards.
    """
    fluid = blocks.BooleanBlock(
        required=False,
        label=_('Full width'),
    )

    class Meta:
        template = 'django_cos/blocks/cardgrid_deck.html'
        icon = 'fa-th-large'
        label = _('Card Grid')


class HeroBlock(BaseLayoutBlock):
    """
    Wrapper with color and image background options.
    """
    full_width = blocks.BooleanBlock(
        required=False,
        default=True,
        label=_('Full width'),
    )
    full_height = blocks.BooleanBlock(
        required=False,
        default=True,
        label=_('Full height')
    )
    is_parallax = blocks.BooleanBlock(
        required=False,
        label=_('Parallax Effect'),
        help_text=_('Background images scroll slower than foreground images, creating an illusion of depth.'),
    )
    background_image = BackgroundImageBlock(required=False)
    tile_image = blocks.BooleanBlock(
        required=False,
        default=False,
        label=_('Tile background image'),
    )
    background_color = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Background Color'),
        help_text=_('Hexadecimal, rgba, or CSS color notation (e.g. #ff0011)')
    )
    layer_color = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Layer Color'),
        help_text=_('Hexadecimal, rgba, or CSS color notation (e.g. #ff0011)'),
    )
    foreground_color = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Foreground Color'),
        help_text=_('Hexadecimal, rgba, or CSS color notation (e.g. #ff0011)'),
    )

    class Meta:
        template = 'django_cos/blocks/hero_block.html'
        icon = 'fa-newspaper-o'
        label = 'Hero Unit'
