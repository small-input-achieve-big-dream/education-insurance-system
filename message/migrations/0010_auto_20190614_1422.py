# Generated by Django 3.0 on 2019-06-14 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0009_remove_products_productsid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='group',
        ),
        migrations.AddField(
            model_name='products',
            name='age_range',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='products',
            name='date',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='products',
            name='recognizee_age_range',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
    ]