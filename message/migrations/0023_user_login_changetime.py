# Generated by Django 3.0 on 2019-06-21 17:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0022_auto_20190621_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_login',
            name='changeTime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
