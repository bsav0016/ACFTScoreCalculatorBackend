# Generated by Django 4.0.6 on 2022-08-14 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_user_paid_fee_alter_acftresult_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='acftresult',
            name='user',
        ),
    ]
