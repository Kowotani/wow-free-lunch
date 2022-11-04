from bnet_api_utils import BNetAPIUtil
from collections import defaultdict
from dataclasses import dataclass
from django.apps import apps
import datetime as dt
from enum import Enum
# add '/home/ec2-user/environment/wow-free-lunch/dj_wfl/wfl to PYTHONPATH
from wfl.models import (ItemClass, ItemClassHierarchy, Profession, ProfessionSkillTier, 
    StgRecipeItem)


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
        Constructor class
        
    INPUT
        
    RETURN
        Empty state object
    '''    
    def __init__(self):
        self._bnet_api_util = BNetAPIUtil()
        self._obj_loader = BulkObjectLoader()
    
    
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
            profession__is_crafting=True, is_legacy_tier=True)
        
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
'''


class ItemDataManager:
    
    
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
        Constructor class
        
    INPUT
        
    RETURN
        Empty state object
    '''    
    def __init__(self):
        self._bnet_api_util = BNetAPIUtil()
        self._obj_loader = BulkObjectLoader()
        
    
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
        
            # naively iterate up to 50 item_subclass_ids until the API returns an error
            for i in range(0, 50):
        
                # call the /item-class/{itemClassId}/item-subclass/{itemSubclassId} endpoint
                try:
                    isid_r = self._bnet_api_util.get_item_subclass_metadata(
                        item_class.pk, i)
                    
                    # enqueue ItemSubclass objects for loading 
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
                    # skip to the next item_class
                    break               

        # load any remaining objects
        self._obj_loader.commit_remaining()