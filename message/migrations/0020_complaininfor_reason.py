# Generated by Django 2.2.2 on 2019-06-21 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0019_auto_20190621_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaininfor',
            name='reason',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
    ]
