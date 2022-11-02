from bnet_api_utils import BNetAPIUtil
from collections import defaultdict
from dataclasses import dataclass
from django.apps import apps
import datetime as dt
from enum import Enum
# add '/home/ec2-user/environment/wow-free-lunch/dj_wfl/wfl to PYTHONPATH
from wfl.models import Profession, ProfessionSkillTier


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
    def __init__(self, chunk_size=1000) -> None:
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
==================
Profession Loaders
==================
'''


'''
This class handles loading data for the `profession` and 
`profession_skill_tier` tables
'''

class ProfessionDataLoader:


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
    
    
    # '''
    # ---------
    # Endpoints
    # ---------
    # '''
    
    # host = 'https://0983fcdb7462476a98cf4fcf96f8e461.vfs.cloud9.us-west-1.amazonaws.com'
    
    # profession_create = '/profession/create'
    # profession_detail = '/profession/{profession_id}'
    
    
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
        Loads the `profession` and `profession_skill_tier` tables
        
    INPUT
        
    RETURN
    '''    
    def load_profession_and_profession_skill_tier(self) -> None:
        
        # call the /profession/index endpoint
        index_r = self._bnet_api_util.get_profession_index()
        
        if index_r is None:
            raise Exception('Error: get_profession_index() in bnet_data_loader.load_profession()')
            
        # iterate through professions
        for profession in index_r['professions']:
            
            # get profession media
            media_r = self._bnet_api_util.get_profession_media(profession['id'])
            
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
                is_primary=(pid_r['type']['type'] == 'PRIMARY')
                )
            self._obj_loader.add(profession_obj)
            
            # check if profession has skill tiers
            if 'skill_tiers' not in pid_r:
                continue 
            
            # iterate through skill tiers
            for skill_tier in pid_r['skill_tiers']:
                
                skill_tier_levels = self._get_skill_tier_levels(skill_tier['name'])
                
                # get skill tier metadata
                sid_r = self._bnet_api_util.get_profession_skill_tier_metadata(
                    profession['id'], skill_tier['id'])
                    
                if sid_r is None:
                    raise Exception('Error: get_profession_skill_tier_metadata() in bnet_data_loader.load_profession()')
                
                # enqueue ProfessionSkillTier object for loading
                skill_tier_obj = ProfessionSkillTier(
                    skill_tier_id=skill_tier['id'],
                    profession=profession_obj, 
                    name=skill_tier['name'],
                    min_skill_level=sid_r['minimum_skill_level'],
                    max_skill_level=sid_r['maximum_skill_level'],
                    min_total_skill_level=skill_tier_levels.min_level,
                    max_total_skill_level=skill_tier_levels.max_level,
                    is_legacy_tier=skill_tier_levels.is_legacy_tier,
                    )
                self._obj_loader.add(skill_tier_obj)
            
        # load any remaining objects
        self._obj_loader.commit_remaining()
       
        
'''
Main code
'''

def main():
    util = ProfessionDataLoader()
    util.load_profession_and_profession_skill_tier()
    
if __name__ == "__main__":
    main()