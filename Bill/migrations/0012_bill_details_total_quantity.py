# Generated by Django 3.2.8 on 2021-12-29 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bill', '0011_bill_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill_details',
            name='total_quantity',
            field=models.CharField(default='0', max_length=100),
        ),
    ]