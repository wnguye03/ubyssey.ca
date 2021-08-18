from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import ArticlePage


@receiver(pre_save, sender=ArticlePage)
def update_timeline_on_article_alteration(instance, **kwargs):
    """
    Examines the "timeline" field before an article is saved, and ensures it is updated when the article is saved.

    If it has been changed, forces an update to the before and after timeline.
    """
    if instance.id is None:
        # We do not get a "created" variable when using a pre-save signal, unlike post-save.
        # Checking if instance.id is None is a workaround. It is true when and only when the model instance has never been written to the DB
        if instance.timeline:
            instance.timeline.save()
            return
    # previous_article represents the article as it currently exists in the database
    # current_article represents the article as it WILL BE when save is actually hit
    previous_article = ArticlePage.objects.get(id=instance.id)
    current_article = instance # for readability

    if previous_article.timeline:
        # If the article used to have a timeline, we save it to keep its data updated.
        previous_article.timeline.save()

    if current_article.timeline:
        # If the article currently has a timeline...
        if current_article.timeline != previous_article.timeline:
            # ...and that timeline isn't the exact same one we just updated above,
            current_article.timeline.save()
            return    
    return

@receiver(post_delete, sender=ArticlePage)
def update_timeline_on_article_deletion(instance, **kwargs):
    """
    Forces update to timeline upon article deletion
    """
    if instance.timeline:
        instance.timeline.save()
