# Generated by Django 3.0 on 2019-06-24 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0036_auto_20190624_0503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='information',
            name='msg',
            field=models.CharField(max_length=500),
        ),
    ]
