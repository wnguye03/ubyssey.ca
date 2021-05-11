"""
Blocks used on special landing pages of the site (such as the guide landing page, or else a magazine landing page)
"""
from . import validators
from wagtail.core import blocks
from django import forms
from dispatch.models import Article

# class ArticleChooserBlock(blocks.ChooserBlock):
#     # based off code from:
#     # https://groups.google.com/g/wagtail/c/S26h5GP9_Fk?pli=1
#     # maybe move to a different namespace
#     template = "specialfeatureslanding/article-box.html"    


class DispatchArticleBlock(blocks.StructBlock):

    article_slug = blocks.CharBlock(
        help_text="Type the SLUG of an article to be included here",
        validators=[validators.validate_published_article],
        required=True,
    )

    def get_context(self, value, parent_context):
        context = super().get_context(value, parent_context=parent_context)
        # article = Article.objects.get(is_published=1, slug=value.article_slug)
        # context['KeeganTest'] = article
        return context

    class Meta:
        template = "specialfeatureslanding/blocks/article-box.html"


class DispatchArticleChooserBlock(blocks.ChooserBlock):
    target_model = Article
    widget = forms.Select 

    class Meta:
        template = "specialfeatureslanding/blocks/article-box.html"
