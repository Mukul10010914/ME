# Generated by Django 3.2.8 on 2021-12-13 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Elastic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('WOVEN NARROW FAB', 'WOVEN NARROW FAB'), ('KNITTED NARROW FAB', 'KNITTED NARROW FAB')], default='WOVEN NARROW FAB', max_length=50)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Velcro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('WOVEN NARROW FAB', 'WOVEN NARROW FAB'), ('KNITTED NARROW FAB', 'KNITTED NARROW FAB')], default='WOVEN NARROW FAB', max_length=50)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
    ]
