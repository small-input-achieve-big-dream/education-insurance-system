# Generated by Django 3.0 on 2019-06-11 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0007_delete_compensate_records'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.DeleteModel(
            name='accident_Application',
        ),
    ]
