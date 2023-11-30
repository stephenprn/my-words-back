# Generated by Django 4.2.7 on 2023-11-30 16:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0013_quiz_nbr_proposals_quiz_nbr_questions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='duration_limit',
            field=models.PositiveBigIntegerField(),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='nbr_proposals',
            field=models.IntegerField(default=4, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='nbr_questions',
            field=models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='quizquestion',
            name='response_duration',
            field=models.PositiveBigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='quizquestion',
            name='response_index',
            field=models.PositiveIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
