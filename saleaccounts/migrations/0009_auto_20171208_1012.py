# Generated by Django 2.0 on 2017-12-08 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('risktypes', '0008_auto_20171208_0822'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='riskfield',
            name='user',
        ),
        migrations.RemoveField(
            model_name='risktype',
            name='user',
        ),
    ]
