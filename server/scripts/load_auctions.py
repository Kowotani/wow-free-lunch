# setup Django for standalone use
# also set DJANGO_SETTINGS_MODULE='dj_wfl.settings' in ~/.bashrc
import django
django.setup()

import datetime as dt
# add '/home/ec2-user/environment/wow-free-lunch/dj_wfl' to PYTHONPATH
from wfl.utils import GameVersion
# add '/home/ec2-user/environment/wow-free-lunch/server' to PYTHONPATH
from bnet_api_interface.bnet_data_manager import AuctionDataManager
from scripts.utils import AuctionFaction, AuctionRealm 


def main():
    # get date and hour variables
    ts = dt.datetime.now()
    date = ts.strftime('%Y-%m-%d')
    hour = ts.hour
    print('Initializing auction data load for {}_{}'.format(
        date, hour))
    
    # load auction data for the realms and factions
    adm = AuctionDataManager()
    for realm in AuctionRealm:
        for faction in AuctionFaction:
            print('Loading auctions for: {}({})_{}({})'.format(
                realm.name, realm.value, 
                faction.name, faction.value))
            adm.load_auction(GameVersion.CLASSIC, 
                realm.value, faction.value)
    
    # load auction_summary
    print('Updating auction_summary for {}_{}'.format(
        date, hour))
    adm.load_auction_summary(date, hour)
    
    # load auction_summary_latest
    print('Updating auction_summary_latest for {}_{}'.format(
        date, hour))
    adm.load_auction_summary_latest(date, hour)

if __name__ == "__main__":
    main()