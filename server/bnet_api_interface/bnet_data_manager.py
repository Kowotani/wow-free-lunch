from .bnet_api_utils import BNetAPIUtil, GameVersion
from collections import defaultdict
from dataclasses import dataclass
from django.apps import apps
from django.db.models import Q
import datetime as dt
from enum import Enum
from urllib.parse import urlparse
# add '/home/ec2-user/environment/wow-free-lunch/dj_wfl' to PYTHONPATH
from wfl.models import (Auction, AuctionHouse, AuctionSummary, 
    ConnectedRealm,  Expansion, Item, ItemClass, ItemClassHierarchy, ItemData, 
    Profession, ProfessionSkillTier, Reagent, Realm, RealmConnection, Recipe, 
    Region, StgRecipeItem)
# enums
from wfl.utils import (AuctionHouseFaction, AuctionTimeLeft, Faction, 
    GameVersion, ItemQuality, NamespaceType, QueryManager, RealmCategory, 
    RealmPopulation, RealmStatus, RealmType)


'''
=================
Bulk Loading Util
=================
'''


'''
This class handles bulk loading of data for generic model objects. It checks for 
object existence as the queues are being populated. Everything in the queue will
be added.
'''

class BulkObjectLoader:
    
    
    '''
    ===============
    Class Variables
    ===============
    '''
    
    # stores the objects to create
    _create_queues = defaultdict(list)
    
    # threshold of objects to create in bulk
    chunk_size = 0
    
    
    '''
    DESC
        Class constructor
        
    INPUT
        Chunk size to indicate how many objects to create in bulk
        
    RETURN
    '''
    def __init__(self, chunk_size=100) -> None:
        self.chunk_size = chunk_size
        
    
    '''
    DESC
        Bulk create the objects for a given model_class
        
    INPUT
        - Name of the model class to bulk create
        - [OPTIONAL] Whether to ignore insert conflicts
        
    RETURN
    '''
    def _commit(self, model_class, ignore_conflicts=False) -> None:
        model_key = model_class._meta.label
        model_class.objects.bulk_create(
            self._create_queues[model_key], ignore_conflicts=ignore_conflicts)
        print('{} model - created {} objects'.format(
            model_key, len(self._create_queues[model_key])))
        self._create_queues[model_key].clear()
        
    
    '''
    DESC
        Add the passed object to its queue if it doesn't already exist
        
    INPUT
        - Model object to queue up for bulk creation
        - [OPTIONAL] Auto-commit objects if chunk_size threshold is met
        - [OPTIONAL] Force add the object (eg. skip existence check as it will
          be performed before calling this function)
        - [OPTIONAL] Whether to ignore insert conflicts
        
    RETURN
    '''
    def add(self, obj, auto_commit=True, force_add=False, ignore_conflicts=False) -> None:
        
        model_class = type(obj)
        model_key = model_class._meta.label
        
        # maybe check existence of obj
        if not force_add:
            if model_class.objects.filter(pk=obj.pk).exists():
                return
        
        # add to respective queue
        self._create_queues[model_key].append(obj)
        print('{} queue - added pk={}'.format(model_key, obj.pk))
    
        # bulk create if threshold has been met and auto_commit enabled
        if (len(self._create_queues[model_key]) >= self.chunk_size
            and auto_commit):
            self._commit(model_class, ignore_conflicts)
                
                
    '''
    DESC
        Bulk create any remaining model objects
        
    INPUT
        - [OPTIONAL] List of model classes to commit in specified order
        - [OPTIONAL] Whether to ignore insert conflicts
        
    RETURN
    '''
    def commit_remaining(self, ordered_model_classes=[], ignore_conflicts=False) -> None:  
        
        # commit objects in specified order
        if len(ordered_model_classes) > 0:
            for model_class in ordered_model_classes:
                self._commit(model_class, ignore_conflicts)
            
        # commit objects in any order
        else:
            for model_name, objs in self._create_queues.items():
                if len(objs) > 0:
                    self._commit(apps.get_model(model_name), ignore_conflicts)


'''
===============
Profession Data 
===============
'''


'''
This class manages data for the following models
- Profession
- ProfessionSkillTier
- StgRecipeItem
- Recipe
- Reagent
'''

class ProfessionDataManager:


    '''
    ===============
    Class Variables
    ===============
    '''
    
    _bnet_api_util = None
    _obj_loader = None
    

    '''
    This dataclass stores the minimum and maximum total skill levels for each of
    the expansion professions
    '''
    @dataclass
    class ProfessionSkillTierLevels:
        min_level: int     # Eg. 350 for Northrend
        max_level: int     # Eg. 450 for Northrend
        level_range: int   # Eg. 100 for Northrend
        is_legacy_tier: bool   # TRUE if the tier required previous tiers to unlock
    
    
    '''
    This dict maps the expansion names to their ProfessionLevels
    '''
    profession_levels = {
        'Classic': ProfessionSkillTierLevels(1, 300, 299, True),
        'Outland': ProfessionSkillTierLevels(275, 375, 100, True),
        'Northrend': ProfessionSkillTierLevels(350, 450, 100, True),
        'Cataclysm': ProfessionSkillTierLevels(425, 525, 100, True),
        'Pandaria': ProfessionSkillTierLevels(500, 600, 100, True),
        'Draenor': ProfessionSkillTierLevels(600, 700, 100, True),
        'Legion': ProfessionSkillTierLevels(700, 800, 100, True),
        'Zandalari': ProfessionSkillTierLevels(0, 0, 175, False),
        'Shadowlands': ProfessionSkillTierLevels(0, 0, 175, False),
        'Dragon Isles': ProfessionSkillTierLevels(0, 0, 175, False),
        }
    
    
    '''
    This list contains all professions that craft items. Note that Enchanting
    is not a crafting profession since it produces spells and not items
    '''
    crafting_professions = ['Alchemy', 'Blacksmithing', 'Cooking', 
        'Engineering', 'Jewelcrafting', 'Inscription', 'Leatherworking',
        'Tailoring']


    '''
    =============
    Class Methods
    =============
    '''
    
    
    '''
    DESC
        Class constructor
        
    INPUT
        
    RETURN
        Empty state object
    '''    
    def __init__(self):
        self._bnet_api_util = BNetAPIUtil()
        self._obj_loader = BulkObjectLoader()

    
    '''
    --------------
    Helper Methods
    --------------
    '''
    
    
    '''
    DESC
        Determines which skill tier levels match the given skill tier name. The
        names requires some matching since they look like 'Legion Blacksmithing'
        and 'Kul Tiran Tailoring / Zandalari Tailoring'
        
    INPUT
        Skill tier name (eg. 'Classic Leatherworking')
        
    RETURN
        ProfessionSkillTierLevels dataclass. Return an empty state object if
        there is no match
    '''    
    def _get_skill_tier_levels(self, skill_tier_name):
        for expansion, skill_tier_levels in self.profession_levels.items():
            if skill_tier_name.find(expansion) >= 0:
                return skill_tier_levels
        return self.ProfessionSkillTierLevels(0, 0, 0, False)
    
    
    '''
    DESC
        Determines if the profession is a crafting profession (ie. it creates
        items)
        
    INPUT
        Profession name
        
    RETURN
        TRUE if the profession creates items, FALSE otherwise
    '''    
    def _is_crafting_profession(self, profession_name):
        return profession_name in self.crafting_professions
    

    '''
    DESC
        Determines to which Expansion the given Skill Tier belongs
        
    INPUT
        Skill Tier name
        
    RETURN
        Expansion object
    '''    
    def _get_expansion_from_skill_tier(self, skill_tier_name):
        for expansion in Expansion.objects.all():
            if skill_tier_name.find(expansion.skill_tier_prefix) >= 0:
                return expansion
        return None
    
    '''
    --------------
    Loader Methods
    --------------
    '''
    
    
    '''
    DESC
        Loads the `profession` table
        
    INPUT
        
    RETURN
    '''    
    def load_profession(self) -> None:
        
        # call the /profession/index endpoint
        index_r = self._bnet_api_util.get_profession_index()
        
        if index_r is None:
            raise Exception('Error: get_profession_index() in bnet_data_loader.load_profession()')
            
        # iterate through professions
        for profession in index_r['professions']:
            
            # get profession media
            media_r = self._bnet_api_util.get_profession_media_metadata(profession['id'])
            
            if media_r is None:
                raise Exception('Error: get_profession_metadata() in bnet_data_loader.load_profession()')
            
            # get profession metadata
            pid_r = self._bnet_api_util.get_profession_metadata(profession['id'])
            
            if pid_r is None:
                raise Exception('Error: get_profession_metadata() in bnet_data_loader.load_profession()')
                
            # enqueue Profession object for loading
            profession_obj = Profession(
                profession_id=profession['id'], 
                name=profession['name'],
                media_url=media_r['assets'][0]['value'],
                media_file_data_id=media_r['assets'][0]['file_data_id'],
                is_primary=(pid_r['type']['type'] == 'PRIMARY'),
                is_crafting=self._is_crafting_profession(profession['name'])
                )
            self._obj_loader.add(profession_obj)
            
        # load any remaining objects
        self._obj_loader.commit_remaining()
       

    '''
    DESC
        Loads the `profession_skill_tier` table
        
    INPUT
        
    RETURN
    '''    
    def load_profession_skill_tier(self) -> None:
        
        # query profession table
        professions = Profession.objects.all()
        
        # get Profession object
        for profession in professions:
        
            # call the /profession/{professionId} endpoint
            pid_r = self._bnet_api_util.get_profession_metadata(
                profession.profession_id)
                
            if pid_r is None:
                raise Exception('Error: get_profession_metadata() in bnet_data_loader.load_profession_skill_tier()')
            
            # check if profession has skill tiers
            if 'skill_tiers' not in pid_r:
                continue
            
            # iterate through skill tiers
            for skill_tier in pid_r['skill_tiers']:
                
                skill_tier_levels = self._get_skill_tier_levels(skill_tier['name'])
            
                # call the /profession/{professionID}/skill-tier/{skillTierID} endpoint
                sid_r = self._bnet_api_util.get_profession_skill_tier_metadata(
                    profession.profession_id, skill_tier['id'])
                    
                if sid_r is None:   
                    raise Exception('Error: get_profession_skill_tier_metadata() in bnet_data_loader.load_profession_skill_tier()')                    
                
                # get expansion for skill tier
                expansion = self._get_expansion_from_skill_tier(skill_tier['name'])
                
                # enqueue ProfessionSkillTier object for loading
                obj = ProfessionSkillTier(
                    skill_tier_id=skill_tier['id'],
                    profession=profession, 
                    name=skill_tier['name'],
                    min_skill_level=sid_r['minimum_skill_level'],
                    max_skill_level=sid_r['maximum_skill_level'],
                    min_total_skill_level=skill_tier_levels.min_level,
                    max_total_skill_level=skill_tier_levels.max_level,
                    is_legacy_tier=skill_tier_levels.is_legacy_tier,
                    expansion=expansion,
                    )
                self._obj_loader.add(obj)
        
        # load any remaining objects
        self._obj_loader.commit_remaining()
            
            
    '''
    DESC
        Loads the all data to their respective tables
        
    INPUT
        
    RETURN
    '''    
    def load_all(self) -> None:
        self.load_profession()
        self.load_profession_skill_tier()
        

'''
=========
Item Data 
=========
'''


'''
This class manages data for the following models
- ItemClass
- ItemSubclass
- Item
- ItemData
'''


class ItemDataManager:
    
    
    '''
    ===============
    Class Variables
    ===============
    '''
    
    _bnet_api_util = None
    _obj_loader = None
    chunk_size = 100
    
    # vendor items used in crafting recipes, keyed by item_id
    vendor_items = {
        159: 'Refreshing Spring Water',
        2320: 'Coarse Thread',
        2321: 'Fine Thread',
        2324: 'Bleach',
        2325: 'Black Dye',
        2604: 'Red Dye',
        2605: 'Green Dye',
        2678: 'Mild Spices',
        2880: 'Weak Flux',
        2901: 'Mining Pick',
        3371: 'Empty Vial',
        3372: 'Leaded Vial',
        3466: 'Strong Flux',
        3857: 'Coal',
        4289: 'Salt',
        4291: 'Silken Thread',
        4340: 'Gray Dye',
        4341: 'Yellow Dye',
        4342: 'Purple Dye',
        4357: 'Rough Blasting Powder',
        4361: 'Copper Tube',
        4363: 'Copper Modulator',
        4364: 'Coarse Blasting Powder',
        4371: 'Bronze Tube',
        4382: 'Bronze Framework',
        4389: 'Gyrochronatom',
        4399: 'Wooden Stock',
        4400: 'Heavy Stock',
        4404: 'Silver Contact',
        4470: 'Simple Wood',
        5565: 'Infernal Stone',
        6217: 'Copper Rod',
        6260: 'Blue Dye',
        6261: 'Orange Dye',
        8343: 'Heavy Silken Thread',
        8925: 'Crystal Vial',
        10290: 'Pink Dye',
        10647: "Engineer's Ink",
        10648: 'Common Parchment',
        11291: 'Star Wood',
        14341: 'Rune Thread',
        16583: 'Demonic Figurine',
        17020: 'Arcane Powder',
        17021: 'Wild Berries',
        17026: 'Wild Thornroot',
        17028: 'Holy Candle',
        17029: 'Sacred Candle',
        17030: 'Ankh',
        17031: 'Rune of Teleportation',
        17032: 'Rune of Portals',
        17033: 'Symbol of Divinity',
        17037: 'Hornbeam Seed',
        17038: 'Ironwood Seed',
        18256: 'Imbued Vial',
        18567: 'Elemental Flux',
        20815: "Jeweler's Kit",
        20824: 'Simple Grinder',
        21177: 'Symbol of Kings',
        22147: 'Flintweed Seed',
        22148: 'Wild Quillvine',
        30817: 'Simple Flour',
        37201: 'Corpse Dust',
        38426: 'Eternium Thread',
        39354: 'Light Parchment',
        39501: 'Heavy Parchment',
        39502: 'Resilient Parchment',
        39505: 'Virtuoso Inking Set',
        39684: 'Hair Trigger',
        40411: 'Enchanted Vial',
        40533: 'Walnut Stock',
        43007: 'Northern Spices',
        44605: 'Wild Spineleaf',
        44614: 'Starleaf Seed',
        44615: 'Devout Candle',
    }
    
    '''
    =============
    Class Methods
    =============
    '''
    
    
    '''
    DESC
        Class constructor
        
    INPUT
        
    RETURN
        Empty state object
    '''    
    def __init__(self):
        self._bnet_api_util = BNetAPIUtil()
        self._obj_loader = BulkObjectLoader(self.chunk_size)


    '''
    --------------
    Helper Methods
    --------------
    '''


    '''
    DESC
         Get the ItemClassHierarchy for the given inputs
        
    INPUT
        - item_class_name of the item
        - item_subclass_name of the item
        
    RETURN
        ItemClassHierarchy for the given inputs
    '''    
    def _get_item_class_hierarchy(self, item_class_name, item_subclass_name) -> ItemClassHierarchy:
        return ItemClassHierarchy.objects.get(class_name=item_class_name, 
            subclass_name=item_subclass_name)


    '''
    DESC
         Create the ItemData object for the given inputs. Returns None if the
         object isn't created
        
    INPUT
        - item_id of the item
        - GameVersion of the item to create
        
    RETURN
        - ItemData object, or None if it can't be created
        - item_name, or None if it can't be parsed
        - item_class_hierarchy, or None of it can't be parsed
    '''    
    def _get_item_data_object(self, item_id, game_version) -> (ItemData, str, ItemClassHierarchy):
        
        # TODO: figure out a better way to handle 404 errors for non-existent
        # item_ids (eg. 107976)
        try:

            # call the /item/{itemId} endpoint
            iid_r = self._bnet_api_util.get_item_metadata(item_id, game_version)
            if iid_r is None:
                raise Exception(
                    'Error: [{}] get_item_metadata() in bnet_data_loader._get_item_data_object()'.format(game_version.value)) 
                
            # get item media
            media_r = self._bnet_api_util.get_item_media_metadata(item_id, game_version)
            if media_r is None:
                raise Exception(
                    'Error: [{}] get_item_media_metadata() in bnet_data_loader._get_item_data_object()'.format(game_version.value))

                
            # enqueue ItemData object for loading 
            obj = ItemData(
                item_data_id='{}_{}'.format(game_version.value, item_id),
                name='{} Data'.format(iid_r['name']),
                game_version=game_version.value,
                media_url=media_r['assets'][0]['value'],
                media_file_data_id=media_r['assets'][0]['file_data_id'],
                purchase_price=iid_r['purchase_price'],
                sell_price=iid_r['sell_price'],
                level=iid_r['level'],
                required_level=iid_r['required_level'],
                quality=iid_r['quality']['type'],
            )
            
            # get ItemClassHierarchy
            item_class_hierarchy=self._get_item_class_hierarchy(
                iid_r['item_class']['name'], iid_r['item_subclass']['name'])
            
            # get item_name
            item_name = iid_r['name']
            
            # return tuple
            return obj, item_name, item_class_hierarchy
            
        # TODO: figure out a better way to handle 404 errors for non-existent
        # item_ids (eg. 107976)    
        except:
            print('[{}] Exception for item_id={}'.format(game_version.value, item_id))
            return None, None, None


    '''
    --------------
    Loader Methods
    --------------
    '''

    
    '''
    DESC
        Loads the `item_class` table
        
    INPUT
        
    RETURN
    '''    
    def load_item_class(self) -> None:
        
        # call the /item-class/index endpoint
        index_r = self._bnet_api_util.get_item_class_index()
        
        if index_r is None:   
            raise Exception('Error: get_item_class_index() in bnet_data_loader.load_item_class()') 
        
        # iterate through the item classes
        for item_class in index_r['item_classes']:
        
            # enqueue StgRecipeItem objects for loading
            obj = ItemClass(
                item_class_id=item_class['id'],
                name=item_class['name']
            )
            self._obj_loader.add(obj)                

        # load any remaining objects
        self._obj_loader.commit_remaining()
        
        
        
    '''
    DESC
        Loads the `item_class_hierarchy` table
        
        There is no way to get a list of all item_subclasses via the Battle.net 
        API, but since the cardinality is low we can naively obtain them by 
        incrementing the ID until the API returns an error
        
    INPUT
        
    RETURN
    '''    
    def load_item_class_hierarchy(self) -> None:
        
        # query the item_class table
        item_classes = ItemClass.objects.all()
        
        # get ItemClass object
        for item_class in item_classes:
        
            # naively iterate up to 50 item_subclass_ids
            for i in range(0, 50):
        
                # call the /item-class/{itemClassId}/item-subclass/{itemSubclassId} endpoint
                try:
                    isid_r = self._bnet_api_util.get_item_subclass_metadata(
                        item_class.pk, i)
                    
                    # enqueue ItemSubclass object for loading 
                    obj = ItemClassHierarchy(
                        item_class_hierarchy_id='{}_{}'.format(item_class.pk,
                            isid_r['subclass_id']),
                        item_subclass_id=isid_r['subclass_id'],
                        class_name=item_class.name,
                        subclass_name=isid_r['display_name'],
                        item_class=item_class,
                        name='{} - {}'.format(item_class.name, 
                            isid_r['display_name'])
                    )
                    self._obj_loader.add(obj) 
                    
                except:
                    pass               

        # load any remaining objects
        self._obj_loader.commit_remaining()
        
        
    '''
    DESC
        Loads the `item` and `item_data` tables
        
        This table stores data for both CLASSIC and RETAIL versions of the Item. 
        The universe of items to load is found in the `stg_recipe_item` table
        
    INPUT
        
    RETURN
    '''    
    def load_item_and_item_data(self) -> None:
        
        # iterate through each item_key (reagent item and crafted item)
        for item_key in ['item_id', 'crafted_item_id']:
            
            # query the stg_recipe_item table for distinct item_key objects
            item_id_objs = StgRecipeItem.objects.values(item_key).distinct()
            
            # implement custom chunk_sizing since ItemData need to be loaded
            # before Item
            counter = 0
            
            # iterate through each item_key
            for item_id in [x[item_key] for x in item_id_objs]:
            
                # ------
                # RETAIL
                # ------
    
                retail_obj, r_item_name, r_item_class_hierarchy = self._get_item_data_object(
                    item_id, GameVersion.RETAIL)
  
                # -------
                # CLASSIC
                # -------
                
                # TODO: explicitly identify items in CLASSIC
                # approximate with item_level <= 40 for RETAIL data
                if retail_obj is None or retail_obj.level <= 40:
                    classic_obj, c_item_name, c_item_class_hierarchy = self._get_item_data_object(
                        item_id, GameVersion.CLASSIC)
                else:
                    classic_obj = None
                    c_item_name = None
                    c_item_class_hierarchy = None
                
                # ----    
                # ITEM
                # ----
                
                # determine item_name and item_class_hierarchy, this uses
                # "falsey" logic (0, None, False, "")
                item_name = r_item_name or c_item_name
                item_class_hierarchy = r_item_class_hierarchy or c_item_class_hierarchy
                
                # skip if required item metadata doesn't exist (ie. errors)
                if (None in [item_class_hierarchy, item_id, item_name] 
                    and retail_obj is None and classic_obj is None):
                    continue
                
                # create Item object
                item_obj = Item(
                    item_id=item_id,
                    name=item_name,
                    item_class_hierarchy=item_class_hierarchy,
                    classic_item_data=classic_obj,
                    retail_item_data=retail_obj,
                )
                
                # add all valid objects
                if retail_obj is not None:
                    self._obj_loader.add(retail_obj, False) 
                if classic_obj is not None:
                    self._obj_loader.add(classic_obj, False)
                self._obj_loader.add(item_obj, False)
                
                # implement custom chunk_size loading because ItemData need to
                # be loaded before Item
                counter += 1
                
                if counter >= self.chunk_size:
                    self._obj_loader.commit_remaining([ItemData, Item])
                    counter = 0
                
            # load any remaining objects
            self._obj_loader.commit_remaining([ItemData, Item])
            

    '''
    DESC
        Updates the is_vendor_item metadata in the `item_data` table
        
    INPUT
        
    RETURN
    '''    
    def update_is_vendor_item_for_item_data(self):
        
        # get item_data objects for item_ids in vendor_items dict
        item_datas = ItemData.objects.extra(
          	tables=['item'],
          	where=[
          	  'item_data.item_data_id=item.classic_item_data_id OR item_data.item_data_id=item.retail_item_data_id',
          	  'item.item_id IN %s'
          	],
          	params=[list(self.vendor_items.keys())]
          )
        
        # iterate through each item_data
        for item_data in item_datas:
            item_data.is_vendor_item = True

        ItemData.objects.bulk_update(item_datas, ['is_vendor_item'])
        print('Updated item_datas to set is_vendor_item = True for vendor items')

'''
===========
Recipe Data 
===========
'''


'''
This class manages data for the following models
- StgRecipeItem
- Recipe
- Reagent
'''

class RecipeDataManager:


    '''
    ===============
    Class Variables
    ===============
    '''
    
    _bnet_api_util = None
    _obj_loader = None
    chunk_size = 100


    '''
    =============
    Class Methods
    =============
    '''
    
    
    '''
    DESC
        Class constructor
        
    INPUT
        
    RETURN
        Empty state object
    '''    
    def __init__(self):
        self._bnet_api_util = BNetAPIUtil()
        self._obj_loader = BulkObjectLoader(self.chunk_size)
    
        
    '''
    --------------
    Helper Methods
    --------------
    '''


    '''
    DESC
         Get the Item object for the given item_id
        
    INPUT
        item_id of the item
        
    RETURN
        Item for the given input
    '''    
    def _get_item(self, item_id) -> Item:
        return Item.objects.get(pk=item_id)


    '''
    DESC
         Determine the crafted_item_id to return given the recipe_response
         
         There are 3 cases to consider:
         
         [1] The Recipe produces different items for Alliance and Horde. In this
         case return the crafted item ID for Alliance, if exists, otherwise for
         Horde (eg. recipe_id=40709 and item_id in (168682, 168688))
         
         [2] The Recipe produces one item for both Alliance and Horde. In this
         case return the singular crafted item ID
         
         [3] The Recipe produces no crafted item, which appears to be the case
         for armor enhancements (eg. recipe_id=26880)
        
    INPUT
        Response from /recipe/{recipeId} endpoint
        
    RETURN
        Item for the given input
    '''    
    def _get_resolved_crafted_item_id(self, recipe_response) -> int:
        
        # Case 1
        if 'alliance_crafted_item' in recipe_response:
            crafted_item_id = recipe_response['alliance_crafted_item']['id']
            
        elif 'horde_crafted_item' in recipe_response:
            crafted_item_id = recipe_response['horde_crafted_item']['id']
        
        # Case 2        
        elif 'crafted_item' in recipe_response:
            crafted_item_id = recipe_response['crafted_item']['id']
        
        # Case 3    
        else:
            crafted_item_id = None
            
        return crafted_item_id


    '''
    --------------
    Loader Methods
    --------------
    '''


    '''
    DESC
        Loads the `stg_recipe_item` table
        
    INPUT
        
    RETURN
    '''    
    def load_stg_recipe_item(self) -> None:
        
        # query profession_skill_tier table for crafting professions
        profession_skill_tiers = ProfessionSkillTier.objects.filter(
            profession__is_crafting=True)
        
        # get ProfessionSkillTier object
        for profession_skill_tier in profession_skill_tiers:
                
            # call the /profession/{professionID}/skill-tier/{skillTierID} endpoint
            sid_r = self._bnet_api_util.get_profession_skill_tier_metadata(
                profession_skill_tier.profession_id, 
                profession_skill_tier.skill_tier_id)

            if sid_r is None:   
                raise Exception('Error: get_profession_skill_tier_metadata() in bnet_data_loader.load_stg_recipe_item()') 
            
            # iterate through the recipe categories
            for category in sid_r['categories']:
                
                # iterate through the recipes
                for recipe in category['recipes']:
                    
                    # check if recipe reagents have already been loaded
                    if StgRecipeItem.objects.filter(recipe_id=recipe['id']).exists():
                        continue
                    
                    # call the /recipe/{recipeID} endpoint
                    rid_r = self._bnet_api_util.get_recipe_metadata(recipe['id'])
                    
                    if rid_r is None:
                        raise Exception('Error: get_recipe_metadata() in bnet_data_loader.load_stg_recipe_item()')
                    
                    # check if recipe has reagents
                    if 'reagents' not in rid_r:
                        continue
                    
                    # get crafted_item_id
                    crafted_item_id = self._get_resolved_crafted_item_id(rid_r)
                    
                    if crafted_item_id is None:
                        continue
                    
                    # iterate though reagents
                    for reagent in rid_r['reagents']:
                    
                        # enqueue StgRecipeItem objects for loading
                        obj = StgRecipeItem(
                            stg_recipe_item_id='_'.join([str(x) for x in
                                [recipe['id'], reagent['reagent']['id'], 
                                crafted_item_id]]),
                            recipe_id=recipe['id'],
                            item_id=reagent['reagent']['id'],
                            crafted_item_id=crafted_item_id,
                            name='{} Reagent'.format(rid_r['name']),
                            skill_tier_id=profession_skill_tier.skill_tier_id,
                            item_quantity=reagent['quantity'],
                            )
                        self._obj_loader.add(obj)                
            
            # load any remaining objects
            self._obj_loader.commit_remaining()


    '''
    DESC
        Loads the `recipe` and `reagent` tables
        Mostly maps to /recipe/{recipeId} endpoint
        
        Recipes must be added before Reagents
        The source of Recipes to 
    INPUT
        
    RETURN
    '''    
    def load_recipe_and_reagent(self):
        
        counter = 0
        
        recipes = Recipe.objects.all().values('recipe_id')
        stg_recipe_items_to_load = StgRecipeItem.objects.filter(
            ~Q(recipe_id__in=[x['recipe_id'] for x in recipes]))
        
        # iterate through each unique recipe_id in stg_recipe_item not already loaded
        for recipe_id_dict in stg_recipe_items_to_load.values('recipe_id').distinct():
        
            # get the recipe_id
            recipe_id = recipe_id_dict['recipe_id']
        
            # get the StgRecipeItems
            stg_recipe_items = StgRecipeItem.objects.filter(recipe_id=recipe_id)
                
            # if there are multiple crafted_item_ids (eg. Alliance vs Horde items)
            # then only keep the one with the lower crafted_item_id
            if len(stg_recipe_items.values('crafted_item_id').distinct()) > 1:
                crafted_item_id = min([x.crafted_item_id for x in stg_recipe_items])
                stg_recipe_items = stg_recipe_items.filter(
                    crafted_item_id=crafted_item_id)
            crafted_item_id = stg_recipe_items.first().crafted_item_id
            
            # get crafted Item 
            crafted_item = self._get_item(crafted_item_id)
            
            if crafted_item is None:
                continue
    
            # call the /recipe/{recipeId} endpoint
            rid_r = self._bnet_api_util.get_recipe_metadata(recipe_id)
            
            if rid_r is None:
                raise Exception('Error: get_recipe_metadata() in bnet_data_loader.load_recipe_and_reagent()')        
            
            # get the min and max quantity crafted
            if 'value' in rid_r['crafted_quantity']:
                min_quantity = rid_r['crafted_quantity']['value']
                max_quantity = rid_r['crafted_quantity']['value']
            elif 'minimum' in rid_r['crafted_quantity'] and 'maximum' in rid_r['crafted_quantity']:
                min_quantity = rid_r['crafted_quantity']['minimum']
                max_quantity = rid_r['crafted_quantity']['maximum']
            else:
                raise Exception('Cannot find item quantity for recipe_id={}'.format(recipe_id))
    
            # get recipe media
            media_r = self._bnet_api_util.get_recipe_media_metadata(recipe_id)
            
            if media_r is None:
                raise Exception('Error: get_recipe_media_metadata() in bnet_data_loader.load_recipe_and_reagent()')
        
            # enqueue the Recipe object for loading
            recipe_obj = Recipe(
                recipe_id=recipe_id,
                name=rid_r['name'],
                skill_tier_id=stg_recipe_items.first().skill_tier_id,
                crafted_item=crafted_item,
                min_quantity=min_quantity,
                max_quantity=max_quantity,
                media_url=media_r['assets'][0]['value'],
                media_file_data_id=media_r['assets'][0]['file_data_id'],
            )
            self._obj_loader.add(recipe_obj, False)
            
            # iterate through each reagent
            for stg_recipe_item in stg_recipe_items:
            
                # get Item object
                item = self._get_item(stg_recipe_item.item_id)
                
                if item is None:
                    continue
            
                # enqueue the Reagent object for loading
                reagent_obj = Reagent(
                    reagent_id='{}_{}'.format(recipe_id, item.item_id),
                    recipe=recipe_obj,
                    item=item,
                    name='{} Reagent - {}'.format(rid_r['name'], item.name),
                    item_quantity=stg_recipe_item.item_quantity,
                    )
            
                # implement custom chunk_size loading because Recipe need to
                # be loaded before Reagent
                # add all valid objects
                self._obj_loader.add(reagent_obj, False)
                
            # implement custom chunk_size loading because Recipe need to
            # be loaded before Reagent
            counter += 1
            
            if counter >= self.chunk_size:
                self._obj_loader.commit_remaining([Recipe, Reagent])
                counter = 0
    
        # load any remaining objects
        self._obj_loader.commit_remaining([Recipe, Reagent])  
                 
                    
    '''
    ---------------
    Updater Methods
    ---------------
    '''


    '''
    DESC
        Updates the skill_tier_id in the `stg_recipe_item` table
        
    INPUT
        
    RETURN
    '''    
    def update_skill_tier_id_for_stg_recipe_item(self):

        # query profession_skill_tier table for crafting professions
        profession_skill_tiers = ProfessionSkillTier.objects.filter(
            profession__is_crafting=True)
        
        # get ProfessionSkillTier object
        for profession_skill_tier in profession_skill_tiers:
                
            # call the /profession/{professionID}/skill-tier/{skillTierID} endpoint
            sid_r = self._bnet_api_util.get_profession_skill_tier_metadata(
                profession_skill_tier.profession_id, 
                profession_skill_tier.skill_tier_id)

            if sid_r is None:   
                raise Exception('Error: get_profession_skill_tier_metadata() in bnet_data_loader.load_stg_recipe_item()') 
            
            # iterate through the recipe categories
            for category in sid_r['categories']:
                
                # iterate through the recipes
                for recipe in category['recipes']:
                    
                    # get StgRecipeItem objects
                    stg_recipe_items = StgRecipeItem.objects.filter(recipe_id=recipe['id'])
                    
                    # update skill tier id
                    stg_recipe_items.update(skill_tier_id=profession_skill_tier.skill_tier_id)
                    print('Updated recipe_id={} with skill_tier_id={}'.format(
                        recipe['id'], profession_skill_tier.skill_tier_id))

    '''
    DESC
        Updates the item_quantity in the `stg_recipe_item` table
        
    INPUT
        
    RETURN
    '''    
    def update_item_quantity_for_stg_recipe_item(self):
        
        # get unique recipe_ids
        for recipe_id_dict in StgRecipeItem.objects.filter(item_quantity=0).values('recipe_id').distinct():

           # call the /recipe/{recipeID} endpoint
            rid_r = self._bnet_api_util.get_recipe_metadata(recipe_id_dict['recipe_id'])
            
            if rid_r is None:
                raise Exception('Error: get_recipe_metadata() in bnet_data_loader.load_stg_recipe_item()')
                
            if 'reagents' not in rid_r:
                continue
            
            # iterate though reagents
            for reagent in rid_r['reagents']:
            
                stg_recipe_items = StgRecipeItem.objects.filter(
                    recipe_id=rid_r['id'], item_id=reagent['reagent']['id'])
            
                stg_recipe_items.update(item_quantity=reagent['quantity'])
                print('Updated recipe_id={} and item_id={} with item_quantity={}'.format(
                    rid_r['id'], reagent['reagent']['id'], reagent['quantity']))
                    

    '''
    DESC
        Updates the media metadata in the `recipe` table
        
    INPUT
        
    RETURN
    '''    
    def update_media_for_recipe(self):
        
        # get recipe_id for Recipes without media metadata
        for recipe in Recipe.objects.filter(media_url__isnull=True):

            # call the /media/recipe/{recipeID} endpoint
            media_r = self._bnet_api_util.get_recipe_media_metadata(recipe.recipe_id)
            
            if media_r is None:
                raise Exception('Error: get_recipe_media_metadata() in bnet_data_loader.update_media_for_recipe()')
            
            Recipe.objects.filter(recipe_id=recipe.recipe_id).update(
                media_url=media_r['assets'][0]['value'],
                media_file_data_id=media_r['assets'][0]['file_data_id'])
            print('Updated recipe_id={} with media_url={} and media_file_data_id={}'.format(
                recipe.recipe_id, media_r['assets'][0]['value'], media_r['assets'][0]['file_data_id']))


'''
=============
Game Metadata
=============
'''


'''
--------------
Expansion Data
--------------
'''


'''
This class manages data for the following models
- Expansion
'''


class ExpansionDataManager:
    
    
    '''
    ===============
    Class Variables
    ===============
    '''
    
    _bnet_api_util = None
    _obj_loader = None
    chunk_size = 100
    
    
    '''
    This dataclass stores data for each expansion
    '''
    @dataclass
    class ExpansionData:
        name: str           # Eg. Wrath of the Lich King
        skill_tier_prefix: str     # Eg. Northrend
        max_level: int      # Eg. 80 for Wrath of the Lich King
        is_classic: bool     # TRUE if the expansion is part of CLASSIC
    
    
    expansion_data = {
        0: ExpansionData('World of Warcraft', 'Classic', 60, True),
        1: ExpansionData('The Burning Crusade', 'Outland', 70, True),
        2: ExpansionData('Wrath of the Lich King', 'Northrend', 80, True),
        3: ExpansionData('Cataclysm', 'Cataclysm', 85, False),
        4: ExpansionData('Mists of Pandaria', 'Pandaria', 90, False),
        5: ExpansionData('Warlords of Draenor', 'Draenor', 100, False),
        6: ExpansionData('Legion', 'Legion', 110, False),
        7: ExpansionData('Battle for Azeroth', 'Zandalari', 120, False),
        8: ExpansionData('Shadowlands', 'Shadowlands', 60, False),
        9: ExpansionData('Dragonflight', 'Dragon Isles', 70, False),
        }
    
    
    '''
    =============
    Class Methods
    =============
    '''
    
    
    '''
    DESC
        Class constructor
        
    INPUT
        
    RETURN
        Empty state object
    '''    
    def __init__(self):
        self._bnet_api_util = BNetAPIUtil()
        self._obj_loader = BulkObjectLoader(self.chunk_size)
        
        
    '''
    DESC
        Loads the `expansion` table
        There is no endpoint for this data
        
    INPUT
        
    RETURN
    '''    
    def load_expansion(self):
        
        # iterate through expansion data
        for expansion_id, expansion_data in self.expansion_data.items():
            
            # enqueue ItemSubclass object for loading 
            obj = Expansion(
                expansion_id=expansion_id,
                name=expansion_data.name,
                skill_tier_prefix=expansion_data.skill_tier_prefix,
                max_level=expansion_data.max_level,
                is_classic=expansion_data.is_classic,
            )
            self._obj_loader.add(obj) 

        # load any remaining objects
        self._obj_loader.commit_remaining()
        
        
'''
----------
Realm Data
----------
'''


'''
This class manages data for the following models
- Region
- Realm
- Connected Realm
'''


class RealmDataManager:
    
    
    '''
    ===============
    Class Variables
    ===============
    '''
    
    _bnet_api_util = None
    _obj_loader = None
    chunk_size = 100

    
    '''
    =============
    Class Methods
    =============
    '''
    
    
    '''
    DESC
        Class constructor
        
    INPUT
        
    RETURN
        Empty state object
    '''    
    def __init__(self):
        self._bnet_api_util = BNetAPIUtil()
        self._obj_loader = BulkObjectLoader(self.chunk_size)
    
        
    '''
    --------------
    Helper Methods
    --------------
    '''    
    
    
    '''
    DESC
         Get the RealmCategory for the given input
        
    INPUT
        Maybe a mappable RealmCategory value
        
    RETURN
        RealmCategory enum
    '''    
    def _get_realm_category(self, realm_category) -> RealmCategory:
        realm_categories = {
            'Brazil': RealmCategory.BRAZIL,
            'Classic': RealmCategory.CLASSIC,
            'Latin America': RealmCategory.LATIN_AMERICA,
            'Oceanic': RealmCategory.OCEANIC,
            'United States': RealmCategory.UNITED_STATES,
            'US East': RealmCategory.US_EAST,
            'US West': RealmCategory.US_WEST
            }
            
        if realm_category not in realm_categories.keys():
            raise Exception('Unknown realm_category={}'.format(realm_category))
            
        return realm_categories[realm_category]


    '''
    DESC
         Get the RealmPopulation for the given input
        
    INPUT
        Maybe a mappable RealmPopulation value
        
    RETURN
        RealmPopulation enum
    '''    
    def _get_realm_population(self, realm_population) -> RealmPopulation:
        realm_populations = {
            'NEW': RealmPopulation.NEW,
            'RECOMMENDED': RealmPopulation.RECOMMENDED,
            'LOW': RealmPopulation.LOW,
            'MEDIUM': RealmPopulation.MEDIUM,
            'HIGH': RealmPopulation.HIGH,
            'FULL': RealmPopulation.FULL,
            'LOCKED': RealmPopulation.LOCKED,
            }
            
        if realm_population not in realm_populations.keys():
            raise Exception('Unknown realm_population={}'.format(realm_population))
            
        return realm_populations[realm_population]


    '''
    DESC
         Get the RealmStatus for the given input
        
    INPUT
        Maybe a mappable RealmStatus value
        
    RETURN
        RealmStatus enum
    '''    
    def _get_realm_status(self, realm_status) -> RealmStatus:
        realm_statuses = {
            'UP': RealmStatus.UP
            }
            
        if realm_status not in realm_statuses.keys():
            raise Exception('Unknown realm_status={}'.format(realm_status))
            
        return realm_statuses[realm_status]
    
 
    '''
    DESC
         Get the RealmType for the given input
        
    INPUT
        Maybe a mappable RealmType value
        
    RETURN
        RealmType enum
    '''    
    def _get_realm_type(self, realm_type) -> RealmType:
        realm_types = {
            'NORMAL': RealmType.NORMAL,
            'PVP': RealmType.PVP,
            'PVP_RP': RealmType.PVP_RP,
            'RP': RealmType.RP
            }

        if realm_type not in realm_types.keys():
            raise Exception('Unknown realm_type={}'.format(realm_type))
            
        return realm_types[realm_type].value
 
    
    '''
    --------------
    Loader Methods
    --------------
    '''
    
    
    '''
    DESC
        Loads the `region` table
        Mostly maps to the /region/{regionId} endpoint
        
    INPUT
        GameVersion of the Region to load
        
    RETURN
    '''    
    def load_region(self, game_version):
        
        # call the /region/index endpoint
        index_r = self._bnet_api_util.get_region_index(game_version)
        
        if index_r is None:
            raise Exception('Error: get_region_index() in bnet_data_loader.load_region()')
        
        # iterate through each region
        for region in index_r['regions']:
            
            # parse region_id from URL
            parse = urlparse(region['href'])
            region_id = int(parse.path.split('/')[-1])
            
            # call the /region/{regionId} endpoint
            rid_r = self._bnet_api_util.get_region_metadata(game_version, region_id)
            
            if rid_r is None:
                raise Exception('Error: get_region_metadata() in bnet_data_loader.load_region()')
            
            # enqueue Region object for loading 
            obj = Region(
                region_id=region_id,
                name=rid_r['name'],
                tag=rid_r['tag'],
                game_version=game_version.value
            )
            self._obj_loader.add(obj) 

        # load any remaining objects
        self._obj_loader.commit_remaining()
        
        
    '''
    DESC
        Loads the `realm` table
        Mostly maps to the /realmn/{realm_slug} endpoint
        
    INPUT
        GameVersion of the Realm to load
        
    RETURN
    '''    
    def load_realm(self, game_version):
        
        # call the /realmn/index endpoint
        index_r = self._bnet_api_util.get_realm_index(game_version)
        
        if index_r is None:
            raise Exception('Error: get_realm_index() in bnet_data_loader.load_realm()')
        
        # iterate through each realm
        for realm in index_r['realms']:
            
            # call the /realm/{realm_slug} endpoint
            rid_r = self._bnet_api_util.get_realm_metadata(game_version, 
                realm['slug'])
            
            if rid_r is None:
                raise Exception('Error: get_realm_index() in bnet_data_loader.load_realm()')
            
            # enqueue Realm object for loading 
            obj = Realm(
                realm_id=rid_r['id'],
                region=Region.objects.get(region_id=rid_r['region']['id']),
                name=rid_r['name'],
                slug=rid_r['slug'],
                realm_type=self._get_realm_type(rid_r['type']['type']).value,
                realm_category=self._get_realm_category(rid_r['category']).value,
                timezone=rid_r['timezone'],
            )
            self._obj_loader.add(obj) 

        # load any remaining objects
        self._obj_loader.commit_remaining()
        
        
    '''
    DESC
        Loads the `connected_realm` and 'realm_connection' tables
        Mostly maps to the /connected-realm/{connectedRealmId} endpoint
        
    INPUT
        GameVersion of the Connected Realm to load
        
    RETURN
    '''    
    def load_connected_realm_and_realm_connection(self, game_version):
        
        # call the /connected-realmn/index endpoint
        index_r = self._bnet_api_util.get_connected_realm_index(game_version)
        
        if index_r is None:
            raise Exception('Error: get_connected_realm_index() in bnet_data_loader.load_connected_realm()')
        
        # iterate through each connected realm
        for connected_realm in index_r['connected_realms']:
            
            # parse connected_realm_id from URL
            parse = urlparse(connected_realm['href'])
            connected_realm_id = int(parse.path.split('/')[-1])
            
            # call the /connected-realm/{connectedRealmId} endpoint
            rid_r = self._bnet_api_util.get_connected_realm_metadata(
                game_version, connected_realm_id)
            
            if rid_r is None:
                raise Exception('Error: get_connected_realm_metadata() in bnet_data_loader.load_connected_realm()')
            
            # enqueue ConnectedRealm object for loading 
            connected_realm_obj = ConnectedRealm(
                connected_realm_id=connected_realm_id,
                name='Connected Realm - {}'.format(connected_realm_id),
                status=self._get_realm_status(rid_r['status']['type']).value,
                population=self._get_realm_population(
                    rid_r['population']['type']).value,
                )
            self._obj_loader.add(connected_realm_obj, auto_commit=False) 
            
            # iterate through each realm
            for realm in rid_r['realms']:
            
                # get Realm object
                realm_obj = Realm.objects.get(realm_id=realm['id'])
                
                # enqueue RealmConnection object for loading
                realm_connection_obj = RealmConnection(
                    realm_connection_id='{}_{}'.format(connected_realm_id, 
                        realm_obj.realm_id),
                    connected_realm=connected_realm_obj,
                    realm=realm_obj,
                    name='Realm Connection - {}_{}'.format(connected_realm_id, 
                        realm_obj.realm_id),
                    )
                self._obj_loader.add(realm_connection_obj, auto_commit=False) 

        # load any remaining objects
        self._obj_loader.commit_remaining([ConnectedRealm, RealmConnection])
        
        
'''
------------
Auction Data
------------
'''


'''
This class manages data for the following models
- AuctionHouse
- Auction
'''


class AuctionDataManager:
    
    
    '''
    ===============
    Class Variables
    ===============
    '''
    
    _bnet_api_util = None
    _obj_loader = None
    chunk_size = 1000

    
    '''
    =============
    Class Methods
    =============
    '''
    
    
    '''
    DESC
        Class constructor
        
    INPUT
        
    RETURN
        Empty state object
    '''    
    def __init__(self):
        self._bnet_api_util = BNetAPIUtil()
        self._obj_loader = BulkObjectLoader(self.chunk_size)
    
        
    '''
    --------------
    Helper Methods
    --------------
    '''    
    
    
    '''
    DESC
         Get the Faction enum for the given input
        
    INPUT
        Maybe a mappable faction ID
        
    RETURN
        Faction enum
    '''    
    def _get_faction(self, faction_id) -> Faction:
        factions = {
            2: Faction.ALLIANCE,
            6: Faction.HORDE,
            7: Faction.BLACKWATER
            }
            
        if faction_id not in factions.keys():
            raise Exception('Unknown faction_id={}'.format(faction_id))
            
        return factions[faction_id]


    '''
    DESC
         Get the AuctionHouseFaction enum for the given input
        
    INPUT
        Maybe a mappable auction house faction ID
        
    RETURN
        AuctionHouseFaction enum
    '''    
    def _get_auction_house_faction(self, faction_id) -> AuctionHouseFaction:
        factions = {
            2: AuctionHouseFaction.ALLIANCE,
            6: AuctionHouseFaction.HORDE,
            7: AuctionHouseFaction.BLACKWATER
            }
            
        if faction_id not in factions.keys():
            raise Exception('Unknown faction_id={}'.format(faction_id))
            
        return factions[faction_id]
 
    
    '''
    DESC
         Get the AuctionTimeLeft enum for the given input
        
    INPUT
        Maybe a mappable auction time left value
        
    RETURN
        AuctionTimeLeft enum
    '''    
    def _get_auction_time_left(self, time_left) -> AuctionTimeLeft:
        auction_time_left = {
            'SHORT': AuctionTimeLeft.SHORT,
            'MEDIUM': AuctionTimeLeft.MEDIUM,
            'LONG': AuctionTimeLeft.LONG,
            'VERY_LONG': AuctionTimeLeft.VERY_LONG,
            }
            
        if time_left not in auction_time_left.keys():
            raise Exception('Unknown time_left={}'.format(time_left))
            
        return auction_time_left[time_left]


    '''
    --------------
    Loader Methods
    --------------
    '''
    
    
    '''
    DESC
        Loads the `auction_house` table
        Mostly maps to the /connected-realm/{connectedRealmId}/auctions/index 
        endpoint
        
    INPUT
        - GameVersion of the Region to load
        - COnnected Realm ID
        
    RETURN
    '''    
    # TODO: figure out how this works for RETAIL
    def load_auction_house(self, game_version):
        
        # iterate through each connected realm
        connected_realms = ConnectedRealm.objects.extra(
            tables=['realm_connection', 'realm', 'region'],
            where=[
                'connected_realm.connected_realm_id=realm_connection.connected_realm_id',
                'realm_connection.realm_id=realm.realm_id',
                'realm.region_id=region.region_id',
                'region.game_version=%s'
                ],
            params=[game_version.value]
            )
        for connected_realm in connected_realms:
        
            # call the /connected-realm/{connectedRealmId}/auctions/index endpoint
            index_r = self._bnet_api_util.get_auction_house_index(game_version, 
                connected_realm.connected_realm_id)
            
            if index_r is None:
                raise Exception('Error: get_auction_house_index() in bnet_data_loader.load_auction_house()')
            
            # iterate through each auction house
            for auction_house in index_r['auctions']:
                
                # get faction ID
                faction_id = self._get_auction_house_faction(
                    auction_house['id']).value
                
                # enqueue AuctionHouse object for loading 
                obj = AuctionHouse(
                    auction_house_id='{}_{}'.format(
                        connected_realm.connected_realm_id, faction_id),
                    name=auction_house['name'],
                    faction=self._get_faction(faction_id).value,
                    faction_id=faction_id,
                    connected_realm=connected_realm
                )
                self._obj_loader.add(obj) 

        # load any remaining objects
        self._obj_loader.commit_remaining()
        

    '''
    DESC
        Loads the `auction` table
        Mostly maps to the /connected-realm/{connectedRealmId}/auctions/{auctionHouseId} 
        endpoint
        
    INPUT
        - GameVersion of the Region to load
        - Connected Realm ID
        - Auction House Faction ID
        
    RETURN
    '''    
    # TODO: figure out how this works for RETAIL
    def load_auction(self, game_version, connected_realm_id, auction_house_faction_id):
        
        # call the /connected-realm/{connectedRealmId}/auctions/{auctionHouseId} endpoint
        auction_r = self._bnet_api_util.get_auctions(game_version, 
            connected_realm_id, auction_house_faction_id)
       
        if auction_r is None:
            raise Exception('Error: get_auctions() in bnet_data_loader.load_auction()')
       
        # set the load timestamps
        update_time = dt.datetime.now()
        update_date = update_time.date()
        update_hour = update_time.strftime('%H')
    
        # iterate through each auction
        for auction in auction_r['auctions']:

            # get unit prices
            bid_unit_price = None if 'bid' not in auction else auction['bid'] / auction['quantity']
            buyout_unit_price = None if 'buyout' not in auction else auction['buyout'] / auction['quantity']

            # enqueue Auction object for loading 
            obj = Auction(
                auction_listing_id='{}_{}_{}'.format(
                    update_date.strftime('%Y%m%d'),
                    update_hour, 
                    auction['id']),
                auction_id=auction['id'],
                item_id=auction['item']['id'],
                quantity=auction['quantity'],
                bid_unit_price=bid_unit_price,
                buyout_unit_price=buyout_unit_price,
                time_left=self._get_auction_time_left(auction['time_left']),
                update_time=update_time,
                update_date=update_date,
                update_hour=int(update_hour),
                auction_house=AuctionHouse.objects.get(
                    connected_realm_id=connected_realm_id, 
                    faction_id=auction_house_faction_id),
                name='Auction - {}'.format(auction['id'])
            )
            self._obj_loader.add(obj) 

        # load any remaining objects
        self._obj_loader.commit_remaining()
        

    '''
    DESC
        Loads the `auction_summary` table
        Summarizes the hourly scrapes of auction_listing to get the
            - quantity / vwap
            - min_quantity / min_price
        
    INPUT
        - update_date ('YYYY-MM-DD')
        - update_hour (0-23)
        
    RETURN
    '''    
    def load_auction_summary(self, update_date, update_hour):
        
        # set the load timestamps
        update_time = dt.datetime.now()
    
        qm = QueryManager()

        # check for existing data
        if AuctionSummary.objects.filter(
                update_date=update_date,
                update_hour=update_hour
            ).exists():
                raise Exception('Error: Auction Summary for (update_date={}, update_hour{}) already exists'.format(
                    update_date, update_hour))
            
        # query data
        sql = '''
            SELECT
            	auction_house_id,
            	item_id,
            	SUM(quantity) AS quantity,
            	1.0 * SUM(buyout_unit_price * quantity) / SUM(quantity) AS vwap,
            	SUM(CASE WHEN rnk = 1 THEN quantity END) AS min_quantity,
            	MIN(CASE WHEN rnk = 1 THEN buyout_unit_price END) AS min_price
            FROM
            (
            	SELECT
            		auction_house_id,
            		item_id,
            		buyout_unit_price,
            		quantity,
            		RANK() OVER (PARTITION BY auction_house_id, item_id ORDER BY buyout_unit_price) AS rnk
            	FROM
            	(
            		SELECT
            			a.auction_house_id,
            			a.item_id,
            			a.buyout_unit_price,
            			SUM(a.quantity) AS quantity
            		FROM auction a
            		JOIN auction_house ah ON a.auction_house_id = ah.auction_house_id
            		JOIN realm_connection rc ON ah.connected_realm_id = rc.connected_realm_id
            		JOIN realm r ON rc.realm_id = r.realm_id
            		WHERE
            			a.update_date = %s
            			AND HOUR(a.update_time) = %s
            			AND a.buyout_unit_price > 0
            		GROUP BY 1, 2, 3
            	) z
            ) y
            GROUP BY 1, 2;
        '''
        params = [update_date, update_hour]
        res = qm.query(sql, params)
        
        # enqueue objects for loading
        for r in res:
            obj = AuctionSummary(
                auction_summary_id='{}_{}_{}_{}'.format(
            		r['auction_house_id'],
            		r['item_id'],
            		update_date.replace('-',''),
            		update_hour),
            	auction_house=AuctionHouse.objects.get(
                    auction_house_id=r['auction_house_id']),
                item_id=r['item_id'],
                quantity=r['quantity'],
                vwap=r['vwap'],
                min_quantity=r['min_quantity'],
                min_price=r['min_price'],
                update_time=update_time,
                update_date=dt.datetime.strptime(update_date, '%Y-%m-%d').date(),
                update_hour=update_hour,
                name='Auction Summary - {}_{}_{}_{}'.format(
            		r['auction_house_id'],
            		r['item_id'],
            		update_date.replace('-',''),
            		update_hour)
            )
            self._obj_loader.add(obj) 

        # load any remaining objects
        self._obj_loader.commit_remaining()