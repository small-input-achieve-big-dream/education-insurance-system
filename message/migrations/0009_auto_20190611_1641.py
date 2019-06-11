# Generated by Django 3.0 on 2019-06-11 08:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0008_auto_20190611_1632'),
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
        ),
        migrations.CreateModel(
            name='apllicant_real',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ID', models.IntegerField()),
                ('sex', models.BooleanField()),
                ('age', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='applicant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.IntegerField()),
                ('company', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=30)),
                ('ID', models.IntegerField()),
                ('style', models.IntegerField()),
                ('birth', models.DateTimeField(auto_now=True, verbose_name='生日')),
                ('sex', models.BooleanField()),
                ('telephone', models.IntegerField()),
                ('address', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='compensate_Records',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compensateID', models.IntegerField()),
                ('tableID', models.IntegerField()),
                ('startTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('changeTime', models.DateTimeField(auto_now=True)),
                ('changerID', models.IntegerField()),
                ('content', models.CharField(max_length=60)),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='complainInfor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_ID', models.IntegerField()),
                ('content', models.CharField(max_length=300)),
                ('state', models.BooleanField()),
                ('changerID', models.IntegerField()),
                ('Return', models.CharField(max_length=60)),
                ('startTime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='保存日期')),
                ('changeTime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
        ),
        migrations.CreateModel(
            name='products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productsID', models.IntegerField()),
                ('productsName', models.CharField(max_length=30)),
                ('productsStyle', models.CharField(max_length=30)),
                ('productsDes', models.CharField(max_length=60)),
                ('group', models.IntegerField()),
                ('dealCount', models.IntegerField()),
            ],
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
        ),
        migrations.CreateModel(
            name='realtionship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ID', models.IntegerField()),
                ('recognizee_ID', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='recognizee_Infor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ID', models.IntegerField()),
                ('sex', models.BooleanField()),
                ('age', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tableID', models.IntegerField()),
                ('productsID', models.IntegerField()),
                ('userID', models.IntegerField()),
                ('recognizee_name', models.CharField(max_length=30)),
                ('recognizee_ID', models.IntegerField()),
                ('effectDate', models.DateTimeField(auto_now=True, verbose_name='生效日期')),
                ('loseDate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='失效日期')),
                ('payCycle', models.CharField(max_length=30)),
                ('money', models.IntegerField()),
                ('relationship', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='trade_Records',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tradeID', models.IntegerField()),
                ('tableID', models.IntegerField()),
                ('trade_money', models.IntegerField()),
                ('startTime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='保存日期')),
                ('changeTime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('changerID', models.IntegerField()),
                ('content', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='use_login',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telephone', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=60)),
                ('power', models.IntegerField()),
                ('userID', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Temp',
        ),
    ]
