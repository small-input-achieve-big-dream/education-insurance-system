# Generated by Django 3.0 on 2019-06-14 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0007_auto_20190614_0434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table',
            name='tableID',
        ),
    ]
