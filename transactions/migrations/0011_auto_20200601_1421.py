# Generated by Django 3.0.6 on 2020-06-01 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0010_transaction_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('complete', 'complete'), ('failed', 'failed')], default='complete', max_length=200),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='to',
            field=models.CharField(max_length=250),
        ),
    ]