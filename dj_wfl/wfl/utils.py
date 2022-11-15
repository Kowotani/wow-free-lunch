from enum import Enum


'''
This enum represents the time left for auctions
'''
class AuctionTimeLeft(Enum):
    SHORT = 'SHORT'
    MEDIUM = 'MEDIUM'
    LONG = 'LONG'
    VERY_LONG = 'VERY_LONG'
    
    
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


'''
This enum represents the CLASSIC and RETAIL versions of WoW
'''
class GameVersion(Enum):
    CLASSIC = 'CLASSIC'
    RETAIL = 'RETAIL'
    
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
        

'''
This enum represents the item quality levels
'''
class ItemQuality(Enum):
    POOR = 'POOR'
    COMMON = 'COMMON'
    UNCOMMON = 'UNCOMMON'
    RARE = 'RARE'
    EPIC = 'EPIC'
    LEGENDARY = 'LEGENDARY'
    HEIRLOOM = 'HEIRLOOM'
    
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


'''
This enum represents the API namespace types
'''
class NamespaceType(Enum):
    DYNAMIC = 'dynamic'
    STATIC = 'static'

    
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
        

'''
This enum represents the realm categories
'''
class RealmCategory(Enum):
    BRAZIL = 'BRAZIL'
    CLASSIC = 'CLASSIC'
    LATIN_AMERICA = 'LATIN_AMERICA'
    OCEANIC = 'OCEANIC'
    UNITED_STATES = 'UNITED_STATES'
    US_EAST = 'US_EAST'
    US_WEST = 'US_WEST'
    

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]        
    
        
'''
This enum represents the realm population
'''
class RealmPopulation(Enum):
    NEW = 'NEW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    FULL = 'FULL'
    LOCKED = 'LOCKED'
    

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


'''
This enum represents the realm status
'''
class RealmStatus(Enum):
    UP = 'UP'
    

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


'''
This enum represents the realm types
'''
class RealmType(Enum):
    NORMAL = 'NORMAL'
    PVP = 'PVP'
    PVP_RP = 'PVP_RP'
    RP = 'RP'
    

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]