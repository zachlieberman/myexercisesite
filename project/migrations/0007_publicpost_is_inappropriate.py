# Generated by Django 3.1.5 on 2021-04-19 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_publicpost_is_highlighted'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicpost',
            name='is_inappropriate',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
