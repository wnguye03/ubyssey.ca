# Generated by Django 3.2.11 on 2022-09-01 21:16

from django.db import migrations, models
import wagtail_color_panel.fields


class Migration(migrations.Migration):

    dependencies = [
        ('section', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sectionpage',
            name='apply_colour_to_subtree_when_saved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sectionpage',
            name='colour',
            field=wagtail_color_panel.fields.ColorField(default='#3490d6', max_length=7),
        ),
        migrations.AddField(
            model_name='sectionpage',
            name='lock_colour',
            field=models.BooleanField(default=False),
        ),
    ]