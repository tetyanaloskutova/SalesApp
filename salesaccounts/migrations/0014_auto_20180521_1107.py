# Generated by Django 2.0.5 on 2018-05-21 09:07

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salesaccounts', '0013_auto_20180519_1153'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'ordering': ['name'], 'verbose_name': 'Account', 'verbose_name_plural': 'Accounts'},
        ),
        migrations.AlterField(
            model_name='historicalsaleslead',
            name='probability',
            field=models.IntegerField(default=50, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='saleslead',
            name='owning_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='salesaccounts.CREmployee', verbose_name='Lead Owner'),
        ),
        migrations.AlterField(
            model_name='saleslead',
            name='probability',
            field=models.IntegerField(default=50, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
        ),
    ]
