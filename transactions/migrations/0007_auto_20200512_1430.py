# Generated by Django 3.0.6 on 2020-05-12 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_auto_20200512_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=8, max_digits=50),
        ),
    ]
