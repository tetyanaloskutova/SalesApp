# Generated by Django 2.0.5 on 2018-05-07 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salesaccounts', '0009_auto_20180504_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleslead',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='salesaccounts.Account'),
        ),
    ]
