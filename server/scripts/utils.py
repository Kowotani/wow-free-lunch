from enum import Enum


'''
This enum represents the realms for which to load auctions
'''
class AuctionRealm(Enum):
    # CLASSIC
    BENEDICTION = 4728
    SKYFURY = 4725
    

'''
This enum represents the factions for which to load auctions
'''
class AuctionFaction(Enum):
    ALLIANCE = 2
    HORDE = 6