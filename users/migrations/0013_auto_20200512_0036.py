# Generated by Django 3.0.6 on 2020-05-11 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20200511_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.DecimalField(decimal_places=8, max_digits=50),
        ),
    ]
