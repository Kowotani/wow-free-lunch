# Generated by Django 3.2.16 on 2023-01-15 03:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wfl', '0042_auto_20230113_1922'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='auction_house',
        ),
        migrations.DeleteModel(
            name='Auction',
        ),
        migrations.DeleteModel(
            name='AuctionListing',
        ),
    ]
