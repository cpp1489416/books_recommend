# Generated by Django 2.1.5 on 2019-01-16 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]