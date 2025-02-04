# Generated by Django 3.2.16 on 2022-11-16 00:02

from django.db import migrations, models
import django.db.models.deletion
import wfl.utils


class Migration(migrations.Migration):

    dependencies = [
        ('wfl', '0031_auto_20221115_0547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='connectedrealm',
            name='realm',
        ),
        migrations.AlterField(
            model_name='connectedrealm',
            name='population',
            field=models.CharField(choices=[('NEW', 'NEW'), ('MEDIUM', 'MEDIUM'), ('HIGH', 'HIGH'), ('FULL', 'FULL'), ('LOCKED', 'LOCKED')], default=wfl.utils.RealmPopulation['NEW'], max_length=256, verbose_name='NEW / MEDIUM / HIGH / FULL / LOCKED'),
        ),
        migrations.CreateModel(
            name='RealmConnection',
            fields=[
                ('name', models.CharField(max_length=256, verbose_name='object name')),
                ('realm_connection_id', models.CharField(max_length=256, primary_key=True, serialize=False, verbose_name='concat connected_realm_id and realm_id as dummy PK')),
                ('connected_realm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wfl.connectedrealm')),
                ('realm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wfl.realm')),
            ],
            options={
                'db_table': 'realm_connection',
            },
        ),
    ]
