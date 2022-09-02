from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from section.sectionable.models import SectionablePage

@receiver(pre_save)
def update_colour_pre_save(instance, sender, **kwargs):
    if issubclass(sender, SectionablePage):
        if instance.use_parent_colour:
            parent_page = instance.get_parent().specific

            if hasattr(parent_page,'colour'):
                instance.colour = parent_page.colour
    return