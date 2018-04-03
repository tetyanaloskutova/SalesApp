# Generated by Django 2.0 on 2017-12-08 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('risktypes', '0010_auto_20171208_1046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='riskfield',
            name='risktype',
        ),
        migrations.AddField(
            model_name='riskfield',
            name='parent_risktype',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='risktype_riskfield', to='risktypes.RiskType'),
            preserve_default=False,
        ),
    ]
