# Generated by Django 3.0 on 2019-06-23 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0028_auto_20190623_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='accident_application',
            name='image_src',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
