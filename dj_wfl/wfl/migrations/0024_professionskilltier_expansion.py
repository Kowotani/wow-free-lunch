# Generated by Django 3.2.16 on 2022-11-10 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wfl', '0023_auto_20221110_0439'),
    ]

    operations = [
        migrations.AddField(
            model_name='professionskilltier',
            name='expansion',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='wfl.expansion'),
        ),
    ]
