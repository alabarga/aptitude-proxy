# Generated by Django 2.2.5 on 2020-01-26 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_auto_20191005_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cargo',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='profile',
            name='lugar_trabajo',
            field=models.CharField(default='', max_length=255),
        ),
    ]
