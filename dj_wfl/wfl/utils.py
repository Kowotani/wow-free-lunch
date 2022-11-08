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