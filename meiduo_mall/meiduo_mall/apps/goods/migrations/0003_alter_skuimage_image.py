# Generated by Django 3.2.16 on 2022-11-07 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20221031_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skuimage',
            name='image',
            field=models.ImageField(default='', upload_to='', verbose_name='图片'),
        ),
    ]
