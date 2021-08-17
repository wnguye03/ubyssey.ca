from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import ArticlePage


@receiver(pre_save, sender=ArticlePage)
def update_timeline_on_article_alteration(sender, instance, **kwargs):
    """
    Examines the "timeline" field before an article is saved.

    If it has been changed, then 
    """

    if instance.id is None:
        # We do not get a "created" variable when using a pre-save signal, unlike post-save.
        # Checking if instance.id is None is a workaround. It is true when and only when the model instance has never been written to the DB
        pass

    # previous_article represents the article as it currently exists in the database
    # current_article represents the article as it WILL BE when save is actually hit
    previous_article = ArticlePage.objects.get(id=instance.id)
    current_article = instance

    print(previous_article.title)
    print(current_article.title)

    print(previous_article.timeline != current_article.timeline)