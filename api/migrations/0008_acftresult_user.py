# Generated by Django 4.0.6 on 2022-08-14 08:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_acftresult_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='acftresult',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='acft_results', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
