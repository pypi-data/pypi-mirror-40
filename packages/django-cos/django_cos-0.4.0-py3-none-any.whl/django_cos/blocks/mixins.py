# Django Imports
from django.utils.translation import ugettext_lazy as _
# Wagtail Imports
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
# Django COS Imports
from django_cos.settings import cr_settings
from django_cos.blocks.base_blocks import BaseLinkBlock


__all__ = [
    'ButtonMixin',
    'MediaMixin',
    'ImageMediaMixin',
    'VideoMediaMixin',
]

class ButtonMixin(blocks.StructBlock):
    """
    Standard style and size options for buttons.
    """
    button_title = blocks.CharBlock(
        max_length=255,
        required=True,
        label=_('Button Title'),
    )
    button_style = blocks.ChoiceBlock(
        choices=cr_settings['FRONTEND_BTN_STYLE_CHOICES'],
        default=cr_settings['FRONTEND_BTN_STYLE_DEFAULT'],
        required=False,
        label=_('Button Style'),
    )
    button_size = blocks.ChoiceBlock(
        choices=cr_settings['FRONTEND_BTN_SIZE_CHOICES'],
        default=cr_settings['FRONTEND_BTN_SIZE_DEFAULT'],
        required=False,
        label=_('Button Size'),
    )

class LazyLoadMixin(blocks.StructBlock):

    lazy_load = blocks.BooleanBlock(
        default=True,
        required=False,
        label=_("Lazy Load"),
        help_text=_('The content will be asynchronously loaded on the page.'))

class MediaMixin(LazyLoadMixin, BaseLinkBlock):

    title = blocks.CharBlock(
        required=False,
        label=_('Title'))
    caption = blocks.RawHTMLBlock(
        required=False,
        label=_('Caption'))

class BaseImageMixin(blocks.StructBlock):

	image = ImageChooserBlock(
        label=_('Image'),
        required=False,
    )
	alt_text = blocks.CharBlock(
        label=_('Alt Text'),
        max_length=255,
        required=False,
        help_text=_('Alternate text to show if the image doesn’t load'),
    )

class ImageMixin(BaseImageMixin, MediaMixin):
    pass

class BackgroundImageMixin(LazyLoadMixin, BaseImageMixin):
    pass

class BaseVideoMixin(BaseImageMixin):

    # TODO: Make the media document blocks for VTT, Track, Audio, Video
	video = None

class VideoMixin(BaseVideoMixin):
    pass

class BackgroundVideoMixin(BaseVideoMixin):
    pass
