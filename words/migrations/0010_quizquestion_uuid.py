# Generated by Django 4.2.7 on 2023-11-30 14:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0009_quizquestion_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizquestion',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]