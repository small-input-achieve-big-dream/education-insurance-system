# Generated by Django 3.0 on 2019-06-24 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0034_information_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='productID',
            field=models.IntegerField(max_length=10),
        ),
    ]
