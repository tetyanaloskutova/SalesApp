# Generated by Django 2.0 on 2017-12-08 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('risktypes', '0013_auto_20171208_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riskfield',
            name='parent_risktype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='risktypes.RiskType'),
        ),
    ]
