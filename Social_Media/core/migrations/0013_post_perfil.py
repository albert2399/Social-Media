# Generated by Django 4.2 on 2023-05-12 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='perfil',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.profile'),
            preserve_default=False,
        ),
    ]
