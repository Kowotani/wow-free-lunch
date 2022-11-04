# Generated by Django 3.2.16 on 2022-11-04 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wfl', '0011_alter_stgrecipeitem_stg_recipe_item_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemClass',
            fields=[
                ('name', models.CharField(max_length=256, verbose_name='object name')),
                ('item_class_id', models.SmallIntegerField(primary_key=True, serialize=False, verbose_name='item class ID')),
            ],
            options={
                'db_table': 'item_class',
            },
        ),
    ]
