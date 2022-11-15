# Generated by Django 3.2.16 on 2022-11-15 05:47

from django.db import migrations, models
import django.db.models.deletion
import wfl.utils


class Migration(migrations.Migration):

    dependencies = [
        ('wfl', '0030_realm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realm',
            name='realm_category',
            field=models.CharField(choices=[('BRAZIL', 'BRAZIL'), ('CLASSIC', 'CLASSIC'), ('LATIN_AMERICA', 'LATIN_AMERICA'), ('OCEANIC', 'OCEANIC'), ('UNITED_STATES', 'UNITED_STATES'), ('US_EAST', 'US_EAST'), ('US_WEST', 'US_WEST')], default=wfl.utils.RealmCategory['UNITED_STATES'], max_length=256, verbose_name='geographic region'),
        ),
        migrations.CreateModel(
            name='ConnectedRealm',
            fields=[
                ('name', models.CharField(max_length=256, verbose_name='object name')),
                ('connected_realm_id', models.SmallIntegerField(primary_key=True, serialize=False, verbose_name='connected realm ID')),
                ('status', models.CharField(choices=[('UP', 'UP')], default=wfl.utils.RealmStatus['UP'], max_length=256, verbose_name='Seems to just be UP')),
                ('population', models.CharField(choices=[('FULL', 'FULL'), ('HIGH', 'HIGH'), ('LOCKED', 'LOCKED'), ('MEDIUM', 'MEDIUM'), ('NEW', 'NEW')], default=wfl.utils.RealmPopulation['NEW'], max_length=256, verbose_name='NEW / MEDIUM / HIGH / FULL / LOCKED')),
                ('realm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wfl.realm')),
            ],
            options={
                'db_table': 'connected_realm',
            },
        ),
    ]
