# Generated by Django 3.2.16 on 2022-11-07 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wfl', '0017_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='media_file_data_id',
            field=models.IntegerField(null=True, verbose_name='ID provided by Battle.net endpoints'),
        ),
        migrations.AddField(
            model_name='item',
            name='media_url',
            field=models.CharField(max_length=512, null=True, unique=True, verbose_name='URL of the media asset'),
        ),
        migrations.AlterField(
            model_name='profession',
            name='media_url',
            field=models.CharField(max_length=512, null=True, unique=True, verbose_name='URL of the media asset'),
        ),
    ]
