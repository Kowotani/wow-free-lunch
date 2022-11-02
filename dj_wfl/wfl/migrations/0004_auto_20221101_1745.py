# Generated by Django 3.2.16 on 2022-11-01 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wfl', '0003_auto_20221031_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='professionskilltier',
            name='max_total_skill_level',
            field=models.SmallIntegerField(default=0, verbose_name='maximum total skill level (eg. 375 for Burning Crusade)'),
        ),
        migrations.AddField(
            model_name='professionskilltier',
            name='min_total_skill_level',
            field=models.SmallIntegerField(default=0, verbose_name='minimum total skill level (eg. 301 for Burning Crusade)'),
        ),
        migrations.AlterField(
            model_name='professionskilltier',
            name='max_skill_level',
            field=models.SmallIntegerField(default=0, verbose_name='maximum skill level for this tier (eg. 75 for Burning Crusade)'),
        ),
        migrations.AlterField(
            model_name='professionskilltier',
            name='min_skill_level',
            field=models.SmallIntegerField(default=0, verbose_name='minimum skill level for this tier (eg. 1 for Burning Crusade)'),
        ),
    ]