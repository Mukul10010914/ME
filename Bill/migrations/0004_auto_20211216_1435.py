# Generated by Django 3.2.8 on 2021-12-16 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0001_initial'),
        ('Bill', '0003_auto_20211216_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temp',
            name='elastic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Product.elastic'),
        ),
        migrations.AlterField(
            model_name='temp',
            name='velcro',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Product.velcro'),
        ),
    ]
