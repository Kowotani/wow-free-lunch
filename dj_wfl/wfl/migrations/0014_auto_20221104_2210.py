# Generated by Django 3.2.16 on 2022-11-04 22:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wfl', '0013_itemsubclass'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemClassHierarchy',
            fields=[
                ('name', models.CharField(max_length=256, verbose_name='object name')),
                ('item_class_hierarchy_id', models.SmallIntegerField(primary_key=True, serialize=False, verbose_name='unique identifier for item_class and item_subclass IDs')),
                ('item_subclass_id', models.SmallIntegerField(default=0, verbose_name='item subclass ID')),
                ('item_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wfl.itemclass')),
            ],
            options={
                'db_table': 'item_class_hierarchy',
            },
        ),
        migrations.DeleteModel(
            name='ItemSubclass',
        ),
    ]
