# Generated by Django 3.2.8 on 2021-12-29 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bill', '0012_bill_details_total_quantity'),
    ]

    operations = [
        migrations.DeleteModel(
            name='bill_file',
        ),
        migrations.AddField(
            model_name='formatt',
            name='stamp',
            field=models.ImageField(blank=True, upload_to='pics'),
        ),
    ]