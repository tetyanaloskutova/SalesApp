# Generated by Django 2.0 on 2017-12-08 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('risktypes', '0017_auto_20171208_1445'),
    ]

    operations = [
        migrations.RenameField(
            model_name='riskfield',
            old_name='user',
            new_name='user_riskfield',
        ),
        migrations.RenameField(
            model_name='risktype',
            old_name='user',
            new_name='user_risktype',
        ),
    ]