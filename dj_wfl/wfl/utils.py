from django.db import connection
from enum import Enum

'''
This class manages custom SQL queries to the database
'''
class QueryManager:
    
    
    '''
    DESC
        Returns the queryset from the input SQL with the given params 
        
    INPUT
        - SQL query to execute
        - [OPTIONAL] params for the SQL query
        
    RETURN
        List of dicts where each dict is a row of the queryset
    '''   
    def query(self, sql, params=[]):
        
        # establish connection
        with connection.cursor() as cursor:
            
            # execute query
            if len(params) > 0:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            
            # get column names
            columns = [col[0] for col in cursor.description]
            
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
            
        raise Exception('Error in query: {} with params: {}'.format(sql, params))


'''
This enum represents the auction house factions
'''
class AuctionHouseFaction(Enum):
    ALLIANCE = 2
    HORDE = 6
    BLACKWATER = 7
    
    
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


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
This enum represents the WoW factions
'''
class Faction(Enum):
    ALLIANCE = 'ALLIANCE'
    HORDE = 'HORDE'
    BLACKWATER = 'BLACKWATER'
    
    
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
This enum represents the crafting professions
'''
class CraftingProfession(Enum):
    ALCHEMY = 'Alchemy'
    BLACKSMITHING = 'Blacksmithing'
    COOKING = 'Cooking'
    ENGINEERING = 'Engineering'
    INSCRIPTION = 'Inscription'
    JEWELCRAFTING = 'Jewelcrafting'
    LEATHERWORKING = 'Leatherworking'
    TAILORING = 'Tailoring'


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
    RECOMMENDED = 'RECOMMENDED'
    LOW = 'LOW'
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
        
        
'''
This enum represents the realms for which to populate auction_listing
'''
class AuctionListingRealm(Enum):
    # CLASSIC
    ANGERFORGE = 'Angerforge'
    BENEDICTION = 'Benediction'
    SKYFURY = 'Skyfury'
    

'''
This enum represents the factions for which to populate auction_listing
'''
class AuctionListingFaction(Enum):
    ALLIANCE = 'Alliance'
    HORDE = 'Horde'