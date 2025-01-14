# Generated by Django 3.2.16 on 2022-11-16 00:33

from django.db import migrations, models
import wfl.utils


class Migration(migrations.Migration):

    dependencies = [
        ('wfl', '0032_auto_20221116_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectedrealm',
            name='population',
            field=models.CharField(choices=[('NEW', 'NEW'), ('LOW', 'LOW'), ('MEDIUM', 'MEDIUM'), ('HIGH', 'HIGH'), ('FULL', 'FULL'), ('LOCKED', 'LOCKED')], default=wfl.utils.RealmPopulation['NEW'], max_length=256, verbose_name='NEW / MEDIUM / HIGH / FULL / LOCKED'),
        ),
    ]
