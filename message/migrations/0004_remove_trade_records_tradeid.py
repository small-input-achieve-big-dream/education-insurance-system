# Generated by Django 2.2.2 on 2019-06-13 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0003_auto_20190613_1658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trade_records',
            name='tradeID',
        ),
    ]
