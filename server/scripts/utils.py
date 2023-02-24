from enum import Enum


'''
This enum represents the realms for which to load auctions
'''
class AuctionRealm(Enum):
    # CLASSIC
    # AZURESONG = 4376
    ARUGAL = 4669
    # ATIESH = 4372
    BENEDICTION = 4728
    # ERANIKUS = 4800
    FAERLINA = 4408
    GROBBULUS = 4647
    MANKRIK = 4384
    # MYZRAEL = 4373
    PAGLE = 4385
    SKYFURY = 4725
    WHITEMANE = 4395
    # WINDSEEKER = 4727
    

'''
This enum represents the factions for which to load auctions
'''
class AuctionFaction(Enum):
    ALLIANCE = 2
    HORDE = 6