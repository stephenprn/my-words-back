# Generated by Django 4.2.7 on 2023-12-26 22:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0009_remove_worddefinition_user_slug_unique_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='collection',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='quizes', to='words.collection'),
            preserve_default=False,
        ),
    ]