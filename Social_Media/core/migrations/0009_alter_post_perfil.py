# Generated by Django 4.2 on 2023-05-12 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_post_perfil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='perfil',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.profile'),
        ),
    ]
