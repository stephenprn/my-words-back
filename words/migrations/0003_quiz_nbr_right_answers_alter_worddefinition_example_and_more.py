# Generated by Django 4.2.7 on 2023-12-12 20:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0002_alter_worddefinition_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='nbr_right_answers',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='worddefinition',
            name='example',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='worddefinition',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]