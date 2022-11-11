from bnet_api_utils import BNetAPIUtil, GameVersion
from collections import defaultdict
from dataclasses import dataclass
from django.apps import apps
import datetime as dt
from enum import Enum
# add '/home/ec2-user/environment/wow-free-lunch/dj_wfl/wfl to PYTHONPATH
from wfl.models import (Item, ItemClass, ItemClassHierarchy, ItemData, 
    Expansion, Profession, ProfessionSkillTier, StgRecipeItem)
# enums
from wfl.utils import GameVersion, ItemQuality


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
        Name of the model class to bulk create
        
    RETURN
    '''
    def _commit(self, model_class) -> None:
        model_key = model_class._meta.label
        model_class.objects.bulk_create(self._create_queues[model_key])
        print('{} model - created {} objects'.format(
            model_key, len(self._create_queues[model_key])))
        self._create_queues[model_key].clear()
        
    
    '''
    DESC
        Add the passed object to its queue if it doesn't already exist
        
    INPUT
        Model object to queue up for bulk creation
        
    RETURN
    '''
    def add(self, obj) -> None:
        
        model_class = type(obj)
        model_key = model_class._meta.label
        
        # check existence of obj
        if not model_class.objects.filter(pk=obj.pk).exists():
        
            # add to respective queue
            self._create_queues[model_key].append(obj)
            print('{} queue - added pk={}'.format(model_key, obj.pk))
        
            # bulk create if threshold has been met
            if len(self._create_queues[model_key]) >= self.chunk_size:
                self._commit(model_class)
                
                
    '''
    DESC
        Bulk create any remaining model objects
        
    INPUT
        
    RETURN
    '''
    def commit_remaining(self) -> None:  
        for model_name, objs in self._create_queues.items():
            if len(objs) > 0:
                self._commit(apps.get_model(model_name))


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
        Loads the `stg_recipe_item` table
        
    INPUT
        
    RETURN
    '''    
    def load_stg_recipe_item(self) -> None:
        
        # query profession_skill_tier table
        profession_skill_tiers = ProfessionSkillTier.objects.filter(
            profession__is_crafting=True, is_legacy_tier=False)
        
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
                    
                    print(rid_r['id'])
                    
                    # check if recipe has reagents
                    if 'reagents' not in rid_r:
                        continue
                    
                    # get list of crafted item item_ids (for Alliance vs Horde items)
                    if ('alliance_crafted_item' in rid_r 
                        and 'horde_crafted_item' in rid_r):
                        crafted_item_ids = [rid_r['alliance_crafted_item']['id'], 
                            rid_r['horde_crafted_item']['id']]    
                            
                    elif 'crafted_item' in rid_r:
                        crafted_item_ids = [rid_r['crafted_item']['id']]
                        
                    else:
                        # this appears to be the case for armor enhancements (eg. recipe_id=26880)
                        continue
                    
                    # get list of reagent item_ids
                    reagent_item_ids = [x['reagent']['id'] for x in rid_r['reagents']]
                    
                    # enqueue StgRecipeItem objects for loading
                    for crafted_item_id in crafted_item_ids:
                        
                        for item_id in reagent_item_ids:
                        
                            obj = StgRecipeItem(
                                stg_recipe_item_id='_'.join([str(x) for x in
                                    [recipe['id'], item_id, crafted_item_id]]),
                                recipe_id=recipe['id'],
                                item_id=item_id,
                                crafted_item_id=crafted_item_id,
                                name='{} Reagent'.format(rid_r['name']),
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
        return ItemClassHierarchy.objects.filter(class_name=item_class_name, 
            subclass_name=item_subclass_name)[0] 


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
                        class_name=getattr(item_class, 'name'),
                        subclass_name=isid_r['display_name'],
                        item_class=item_class,
                        name='{} - {}'.format(getattr(item_class, 'name'), 
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
                if retail_obj is None or getattr(retail_obj, 'level') <= 40:
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
                    self._obj_loader.add(retail_obj) 
                if classic_obj is not None:
                    self._obj_loader.add(classic_obj)
                self._obj_loader.add(item_obj)
                
                # implement custom chunk_size loading because ItemData need to
                # be loaded before Item, use chunk_size - 1 to trigger this upload
                # instead of the one in BulkObjectLoader to guarantee order
                counter += 1
                
                if counter >= self.chunk_size - 1:
                    self._obj_loader._commit(ItemData)
                    self._obj_loader._commit(Item)
                    counter = 0
                
            # load any remaining objects
            self._obj_loader._commit(ItemData)
            self._obj_loader._commit(Item)
            

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
    --------------
    Loader Methods
    --------------
    '''


    '''
    DESC
        Loads the `recipe` table
        Mostly maps to /recipe/{recipeId} endpoint
        
    INPUT
        
    RETURN
    '''    
    def load_recipe(self):
        pass


'''
==============
Expansion Data 
==============
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