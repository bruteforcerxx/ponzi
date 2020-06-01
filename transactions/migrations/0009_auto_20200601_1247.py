# Generated by Django 3.0.6 on 2020-06-01 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0008_auto_20200512_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('complete', 'successful'), ('failed', 'failed')], default='complete', max_length=200),
        ),
    ]
