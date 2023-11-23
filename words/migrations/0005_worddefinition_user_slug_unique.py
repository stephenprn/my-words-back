# Generated by Django 4.2.7 on 2023-11-22 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0004_worddefinition_user'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='worddefinition',
            constraint=models.UniqueConstraint(fields=('user', 'slug'), name='user_slug_unique'),
        ),
    ]
