# Generated by Django 3.0.6 on 2020-06-01 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_auto_20200601_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='referral_code',
            field=models.CharField(default='hushzeqi', max_length=100, unique=True),
        ),
    ]
