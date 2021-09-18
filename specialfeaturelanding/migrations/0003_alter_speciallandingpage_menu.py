# Generated by Django 3.2.5 on 2021-08-20 23:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailmenus', '0023_remove_use_specific'),
        ('specialfeaturelanding', '0002_speciallandingpage_menu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speciallandingpage',
            name='menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailmenus.flatmenu'),
        ),
    ]