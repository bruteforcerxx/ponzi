# Generated by Django 3.0.6 on 2020-05-11 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20200511_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=245, null=True, unique=True),
        ),
    ]
