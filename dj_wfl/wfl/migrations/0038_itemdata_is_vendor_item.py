# Generated by Django 3.2.16 on 2022-12-06 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wfl', '0037_alter_auction_bid_unit_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemdata',
            name='is_vendor_item',
            field=models.BooleanField(default=False, verbose_name='TRUE if this item is sold by vendors'),
        ),
    ]
