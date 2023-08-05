"""
Createable pages used in Django COS.
"""
from modelcluster.fields import ParentalKey
from django_cos.forms import DjangoCOSFormField
from django_cos.models import (
    DjangoCOSArticlePage,
    DjangoCOSArticleIndexPage,
    DjangoCOSEmail,
    DjangoCOSFormPage,
    DjangoCOSWebPage
)


class ArticlePage(DjangoCOSArticlePage):
    """
    Article, suitable for news or blog content.
    """
    class Meta:
        verbose_name = 'Article'

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ['website.ArticleIndexPage']

    template = 'django_cos/pages/article_page.html'
    amp_template = 'django_cos/pages/article_page.amp.html'
    search_template = 'django_cos/pages/article_page.search.html'


class ArticleIndexPage(DjangoCOSArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """
    class Meta:
        verbose_name = 'Article Landing Page'

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'website.ArticlePage'

    # Only allow ArticlePages beneath this page.
    subpage_types = ['website.ArticlePage']

    template = 'django_cos/pages/article_index_page.html'


class FormPage(DjangoCOSFormPage):
    """
    A page with an html <form>.
    """
    class Meta:
        verbose_name = 'Form'

    template = 'django_cos/pages/form_page.html'


class FormPageField(DjangoCOSFormField):
    """
    A field that links to a FormPage.
    """
    page = ParentalKey('FormPage', related_name='form_fields')

class FormConfirmEmail(DjangoCOSEmail):
    """
    Sends a confirmation email after submitting a FormPage.
    """
    page = ParentalKey('FormPage', related_name='confirmation_emails')


class WebPage(DjangoCOSWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    Template renders all Navbar and Footer snippets in existance.
    """
    class Meta:
        verbose_name = 'Web Page'

    template = 'django_cos/pages/web_page.html'
