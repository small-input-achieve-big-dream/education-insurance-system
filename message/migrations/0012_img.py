# Generated by Django 2.2.2 on 2019-06-18 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0011_remove_user_login_userid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_url', models.ImageField(upload_to='static')),
            ],
        ),
    ]
