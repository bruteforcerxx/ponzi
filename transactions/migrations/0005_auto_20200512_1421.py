# Generated by Django 3.0.6 on 2020-05-12 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_auto_20200512_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='tx_hash',
            field=models.CharField(max_length=400, unique=True),
        ),
    ]
