# Generated by Django 3.2.8 on 2021-12-25 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bill', '0010_auto_20211221_1346'),
    ]

    operations = [
        migrations.CreateModel(
            name='bill_file',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel', models.FileField(max_length=254, upload_to=None)),
            ],
        ),
    ]