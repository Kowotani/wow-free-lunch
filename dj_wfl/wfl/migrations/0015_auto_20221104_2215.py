# Generated by Django 3.2.16 on 2022-11-04 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wfl', '0014_auto_20221104_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemclasshierarchy',
            name='class_name',
            field=models.CharField(default=None, max_length=256, verbose_name='item class name'),
        ),
        migrations.AddField(
            model_name='itemclasshierarchy',
            name='subclass_name',
            field=models.CharField(default=None, max_length=256, verbose_name='item subclass name'),
        ),
    ]
