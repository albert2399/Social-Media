# Generated by Django 4.2 on 2023-06-09 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_remove_comment_post_id_comment_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='private',
            field=models.BooleanField(default=False),
        ),
    ]