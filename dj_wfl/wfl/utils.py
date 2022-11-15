from enum import Enum


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
    LATIN_AMERICA = 'LATIN_AMERICA'
    OCEANIC = 'OCEANIC'
    UNITED_STATES = 'UNITED_STATES'
    US_EAST = 'US_EAST'
    US_WEST = 'US_WEST'
    

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
        

