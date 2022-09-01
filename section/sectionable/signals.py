from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from section.sectionable.models import SectionablePage

@receiver(pre_save, SectionablePage)
def update_children_colour_pre_save(instance,  **kwargs):
    if instance.apply_colour_to_subtree_when_saved:
        instance._apply_colour_to_subtree_when_saved = instance.apply_colour_to_subtree_when_saved
    instance.apply_colour_to_subtree_when_saved = False
    return

@receiver(post_save, SectionablePage)
def update_children_colour_post_save(instance,  **kwargs):
       
    if instance._apply_colour_to_subtree_when_saved:
        try:
            children_qs = instance.get_children().specific()
            for child in children_qs:
                if not child.lock_colour:
                    child.apply_colour_to_subtree_when_saved = True
                    child.colour = instance.colour
                    child.save()
        except Exception as e:
            raise TypeError('Unexpected class of child page!')
    return
