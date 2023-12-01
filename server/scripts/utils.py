from enum import Enum


'''
This enum represents the CLASSIC realms for which to load auctions
'''
class ClassicAuctionRealm(Enum):
    
    # -- CLASSIC --
    
    # AZURESONG = 4376
    # ARUGAL = 4669
    # ATIESH = 4372
    BENEDICTION = 4728
    # ERANIKUS = 4800
    FAERLINA = 4408
    GROBBULUS = 4647
    # MANKRIK = 4384
    # MYZRAEL = 4373
    # PAGLE = 4385
    # SKYFURY = 4725
    # WHITEMANE = 4395
    # WINDSEEKER = 4727
    
    
'''
This enum represents the ERA realms for which to load auctions
'''
class EraAuctionRealm(Enum):
    
    CRUSADER_STRIKE = 5816
    CHAOS_BOLT = 5820
    LONE_WOLF = 5814
    WILD_GROWTH = 5813
    

'''
This enum represents the factions for which to load auctions
'''
class AuctionFaction(Enum):
    ALLIANCE = 2
    HORDE = 6