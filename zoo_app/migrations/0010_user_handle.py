# Generated by Django 2.2 on 2021-06-09 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zoo_app', '0009_auto_20210606_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='handle',
            field=models.CharField(default='The Raj', max_length=40),
            preserve_default=False,
        ),
    ]