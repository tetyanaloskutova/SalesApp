# Generated by Django 2.0 on 2017-12-08 12:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('risktypes', '0014_auto_20171208_1348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='riskfield',
            name='description',
        ),
        migrations.RemoveField(
            model_name='riskfield',
            name='enumlist',
        ),
        migrations.RemoveField(
            model_name='riskfield',
            name='len_decim',
        ),
        migrations.RemoveField(
            model_name='riskfield',
            name='length',
        ),
        migrations.RemoveField(
            model_name='riskfield',
            name='name',
        ),
        migrations.RemoveField(
            model_name='riskfield',
            name='parent_risktype',
        ),
        migrations.RemoveField(
            model_name='riskfield',
            name='type',
        ),
        migrations.RemoveField(
            model_name='risktype',
            name='description',
        ),
        migrations.RemoveField(
            model_name='risktype',
            name='name',
        ),
        migrations.AddField(
            model_name='riskfield',
            name='risktype',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='risktype_riskfield', to='risktypes.RiskType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='riskfield',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='risktype',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_risktype', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]