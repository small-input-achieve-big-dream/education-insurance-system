# Generated by Django 2.2.2 on 2019-06-13 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0004_remove_trade_records_tradeid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade_records',
            name='tableID',
            field=models.CharField(max_length=30),
        ),
    ]
