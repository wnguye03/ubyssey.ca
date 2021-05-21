from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

@register_snippet
class SportsTournamentSnippet(models.Model):
    tournament_name = models.TextField(blank=True, null=False, default='')
    slug = models.SlugField(
        primary_key=True,
        unique=True,
        blank=False,
        null=False,
        max_length=255,
    )

    panels = [
        MultiFieldPanel(
            [
                InlinePanel("tournament_team", min_num=1, max_num=20, label="Tournament Team"),
            ],
            heading="Tournament Teams"
        ),
    ]

    def __str__(self):
        return self.tournament_name

class SportsTeamOrderable(ClusterableModel, Orderable):
    """
    Based on individual team nodes
    """
    team_name = models.TextField(blank=True, null=False, default='')
    ## we probably need to install https://pypi.org/project/django-colorfield/ for a more robust version of this
    team_color = models.CharField(
        null=False,
        blank=False,
        max_length=7,
        default='#FF0000',
    )
    team_logo = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    # TODO: representation of location and of stats
    panels = [

        MultiFieldPanel(
            [
                InlinePanel("players_to_watch", min_num=1, max_num=1, label="Player to watch"),
            ],
            heading="Player to Watch"
        ),
    ]

class SportsPlayerProfileOrderable(Orderable):
    full_name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    profile_text = models.CharField(
        max_length=1500,
        blank=True,
        null=False,
    )
    player_photo = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    players_team = ParentalKey(
        "SportsTeamOrderable",
        related_name="players_to_watch",
    )
    panels = [
        FieldPanel('full_name'),
        FieldPanel('profile_text'),
        ImageChooserPanel('players_photo'),
    ]

    def __str__(self):
        return self.full_name
