# Generated by Django 5.1.3 on 2024-11-18 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("planetarium", "0002_astronomyshow_show_theme_reservation_ticket"),
    ]

    operations = [
        migrations.RenameField(
            model_name="astronomyshow",
            old_name="show_theme",
            new_name="show_themes",
        ),
    ]
