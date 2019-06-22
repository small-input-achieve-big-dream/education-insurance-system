# Generated by Django 3.0 on 2019-06-22 14:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('message', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='accident_Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicationID', models.IntegerField()),
                ('tableID', models.IntegerField()),
                ('accident_verify', models.CharField(max_length=200)),
                ('state', models.BooleanField()),
                ('compensation_money', models.IntegerField()),
            ],
            options={
                'db_table': 'accident_Application',
            },
        ),
        migrations.CreateModel(
            name='applicant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('idcard', models.CharField(max_length=30, unique=True)),
                ('style', models.IntegerField()),
                ('address', models.CharField(max_length=200)),
                ('score', models.IntegerField()),
            ],
            options={
                'db_table': 'applicant',
            },
        ),
        migrations.CreateModel(
            name='applicant_real',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.CharField(max_length=30, unique=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'applicant_real',
            },
        ),
        migrations.CreateModel(
            name='compensate_Records',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compensateID', models.IntegerField()),
                ('tableID', models.IntegerField()),
                ('startTime', models.DateTimeField(default=datetime.datetime.now)),
                ('changeTime', models.DateTimeField(auto_now=True)),
                ('changerID', models.IntegerField()),
                ('content', models.CharField(max_length=60)),
                ('count', models.IntegerField()),
            ],
            options={
                'db_table': 'compensate_Records',
            },
        ),
        migrations.CreateModel(
            name='complainInfor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_ID', models.CharField(max_length=30)),
                ('reason', models.CharField(max_length=30)),
                ('content', models.CharField(max_length=300)),
                ('state', models.BooleanField()),
                ('changerID', models.CharField(max_length=30)),
                ('Return', models.CharField(max_length=60)),
                ('startTime', models.DateTimeField(default=datetime.datetime.now)),
                ('changeTime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'complainInfor',
            },
        ),
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_url', models.ImageField(upload_to='static')),
            ],
        ),
        migrations.CreateModel(
            name='information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=30)),
                ('style', models.CharField(max_length=20)),
                ('msg', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=30)),
                ('createTime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'information',
            },
        ),
        migrations.CreateModel(
            name='products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productsName', models.CharField(max_length=30)),
                ('productsStyle', models.CharField(max_length=30)),
                ('productsDes', models.CharField(max_length=60)),
                ('age_range', models.CharField(max_length=60)),
                ('recognizee_age_range', models.CharField(max_length=60)),
                ('date', models.CharField(max_length=60)),
                ('dealCount', models.IntegerField()),
            ],
            options={
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='profit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productsID', models.IntegerField()),
                ('deadline', models.CharField(max_length=30)),
                ('oneReturen', models.IntegerField()),
                ('weekReturen', models.IntegerField()),
                ('monthReturn', models.IntegerField()),
            ],
            options={
                'db_table': 'profit',
            },
        ),
        migrations.CreateModel(
            name='realtionship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.CharField(max_length=30)),
                ('recognizee_ID', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'realtionship',
            },
        ),
        migrations.CreateModel(
            name='recognizee_Infor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.CharField(max_length=30, unique=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'recognizee_Infor',
            },
        ),
        migrations.CreateModel(
            name='table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productsID', models.IntegerField()),
                ('userID', models.CharField(max_length=30)),
                ('recognizee_name', models.CharField(max_length=30)),
                ('recognizee_ID', models.CharField(max_length=30)),
                ('effectDate', models.DateTimeField(auto_now=True)),
                ('loseDate', models.DateTimeField(default=datetime.datetime.now)),
                ('payCycle', models.CharField(max_length=30)),
                ('money', models.IntegerField()),
                ('state', models.BooleanField()),
            ],
            options={
                'db_table': 'table',
            },
        ),
        migrations.CreateModel(
            name='trade_records',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.CharField(max_length=30)),
                ('tableID', models.CharField(max_length=30, unique=True)),
                ('trade_money', models.CharField(max_length=30)),
                ('startTime', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'trade_records',
            },
        ),
        migrations.CreateModel(
            name='user_login',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telephone', models.CharField(max_length=15, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=60)),
                ('power', models.IntegerField()),
                ('changeTime', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'user_login',
            },
        ),
    ]
