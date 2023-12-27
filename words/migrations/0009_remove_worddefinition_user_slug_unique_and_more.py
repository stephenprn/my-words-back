# Generated by Django 4.2.7 on 2023-12-26 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0008_remove_worddefinition_user_slug_unique_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='worddefinition',
            name='user_slug_unique',
        ),
        migrations.AddConstraint(
            model_name='worddefinition',
            constraint=models.UniqueConstraint(fields=('user', 'slug', 'collection'), name='user_slug_collection_id_unique'),
        ),
    ]