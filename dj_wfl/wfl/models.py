from django.db import models
from wfl.utils import GameVersion, ItemQuality, RealmCategory, RealmType


'''
==========
ABC Models
==========
'''


'''
DESC
   Stores data common throughout multiple models,
   but not data related to media storage
'''

class CommonData(models.Model):
    name = models.CharField('object name', max_length=256)

    
    class Meta:
        abstract = True

        
    def __str__(self):
        field_names = [x.name for x in self._meta.fields]
        return str({x: getattr(self, x) for x in field_names})
    
    
'''
DESC
   Stores data for media storage across models
'''

class MediaData(models.Model):
    media_url = models.CharField('URL of the media asset', max_length=512, null=True)
    media_file_data_id = models.IntegerField('ID provided by Battle.net endpoints', null=True)

    
    class Meta:
        abstract = True


'''
====================
Game Metadata Models
====================
'''


'''
DESC
    Dim table for Expansion
    This table will be populated manually since there is no endpoint
'''

class Expansion(CommonData):
    expansion_id = models.SmallIntegerField('expansion ID', primary_key=True)
    skill_tier_prefix = models.CharField('prefix to identy the expansion skill tiers', max_length=256, default='')
    max_level = models.SmallIntegerField('max character level', default=0)
    is_classic = models.BooleanField('TRUE if this expansion is part of Classic', default=False)
    

    class Meta:
        db_table = 'expansion'

        
    def __str__(self):
        return CommonData.__str__(self)


'''
DESC
    Dim table for Region
    Mostly maps to /region/{regionId} endpoint
'''

class Region(CommonData):
    region_id = models.SmallIntegerField('region ID', primary_key=True)
    tag = models.CharField('region tag', max_length=256, default='')
    game_version = models.CharField('game version of the region', max_length=256, choices=GameVersion.choices(), default=GameVersion.RETAIL)
    

    class Meta:
        db_table = 'region'

        
    def __str__(self):
        return CommonData.__str__(self)


'''
DESC
    Dim table for Region
    Mostly maps to /realm/{realmId} endpoint
'''

class Realm(CommonData):
    realm_id = models.SmallIntegerField('realm ID', primary_key=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    slug = models.CharField('realm slug', max_length=256, default='')
    realm_type = models.CharField('NORMAL / PVP / PVP_RP / RP', max_length=256, choices=RealmType.choices(), default=RealmType.NORMAL)
    realm_category = models.CharField('geographic region', max_length=256, choices=RealmCategory.choices(), default=RealmCategory.UNITED_STATES)
    timezone = models.CharField('realm timezone / locale', max_length=256, default='')
    

    class Meta:
        db_table = 'realm'

        
    def __str__(self):
        return CommonData.__str__(self)


'''
=================
Profession Models
=================
'''


'''
DESC
    Dim table for Professions
    Mostly maps to /profession/index endpoint
'''

class Profession(CommonData, MediaData):
    profession_id = models.SmallIntegerField('profession ID', primary_key=True)
    is_primary = models.BooleanField('TRUE if the profession is a primary profession', default=False)
    is_crafting = models.BooleanField('TRUE if the profession crafts items', default=False)


    class Meta:
        db_table = 'profession'

        
    def __str__(self):
        return CommonData.__str__(self)


'''
DESC
    Dim table for Profession Skill Tiers, which generally map to expansions (eg. Legion,
    Shadowlands, Classic).
    Mostly maps to /profession/{professionID} endpoint
'''

class ProfessionSkillTier(CommonData):
    skill_tier_id = models.SmallIntegerField('skill tier ID', primary_key=True) 
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE)
    min_skill_level = models.SmallIntegerField('minimum skill level for this tier (eg. 1 for Burning Crusade)', default=0)
    max_skill_level = models.SmallIntegerField('maximum skill level for this tier (eg. 75 for Burning Crusade)', default=0)
    min_total_skill_level = models.SmallIntegerField('minimum total skill level (eg. 301 for Burning Crusade)', default=0)
    max_total_skill_level = models.SmallIntegerField('maximum total skill level (eg. 375 for Burning Crusade)', default=0)
    is_legacy_tier = models.BooleanField('TRUE if the tier requires previous tiers to unlock', default=False)
    expansion = models.ForeignKey(Expansion, on_delete=models.CASCADE, default=0)

    
    class Meta:
        db_table = 'profession_skill_tier'
        
    
    def __str__(self):
        return CommonData.__str__(self)


'''
===========
Item Models
===========
'''


'''
DESC
    Dim table for Item Classes
    Mostly maps to /item_class/index endpoint
'''

class ItemClass(CommonData):
    item_class_id = models.SmallIntegerField('item class ID', primary_key=True)


    class Meta:
        db_table = 'item_class'

        
    def __str__(self):
        return CommonData.__str__(self)
        
        
'''
DESC
    Dim table for Item Class Hierarchy
    Mostly maps to /item_class/{itemClassId}/item_subclass/{itemSubclassId}
    endpoint
'''

class ItemClassHierarchy(CommonData):
    item_class_hierarchy_id = models.CharField('unique identifier for item_class and item_subclass IDs', max_length=256, primary_key=True)
    item_subclass_id = models.SmallIntegerField('item subclass ID', default=0)
    item_class = models.ForeignKey(ItemClass, on_delete=models.CASCADE)
    class_name = models.CharField('item class name', max_length=256, default=None)
    subclass_name = models.CharField('item subclass name', max_length=256, default=None)


    class Meta:
        db_table = 'item_class_hierarchy'

        
    def __str__(self):
        return CommonData.__str__(self)   
      
      
'''
DESC
    Dim table for ItemData - to be used in conjuction with Item
    Mostly maps to /item/{itemId} endpoint
    This model will store the actual data associated with the Item for both
    CLASSIC and RETAIL versions of the game
'''

class ItemData(CommonData, MediaData):    
    item_data_id = models.CharField('unique identifier for item_id and game_version', max_length=256, primary_key=True) 
    purchase_price = models.IntegerField('item vendor purchase price', default=0)
    sell_price = models.IntegerField('item vendor sell price', default=0)
    game_version = models.CharField('game version of the item', max_length=256, choices=GameVersion.choices(), default=GameVersion.RETAIL)
    level = models.SmallIntegerField('item level', default=0)
    required_level = models.SmallIntegerField('required player level', default=0)
    quality = models.CharField('quality level', max_length=256, choices=ItemQuality.choices(), default=ItemQuality.COMMON)


    class Meta:
        db_table = 'item_data'

        
    def __str__(self):
        return CommonData.__str__(self)      
      
        
'''
DESC
    Dim table for Item - to be used in conjuction with ItemData
    Mostly maps to /item/{itemId} endpoint
    This model mostly exists to support Django's singular column PK requirement
'''

class Item(CommonData):
    item_id = models.IntegerField('item ID', primary_key=True) 
    item_class_hierarchy = models.ForeignKey(ItemClassHierarchy, on_delete=models.CASCADE)
    classic_item_data = models.ForeignKey(ItemData, on_delete=models.CASCADE, related_name='classic_item_data', null=True)
    retail_item_data = models.ForeignKey(ItemData, on_delete=models.CASCADE, related_name='retail_item_data', null=True)
    

    class Meta:
        db_table = 'item'

        
    def __str__(self):
        return CommonData.__str__(self)
        

'''
=============
Recipe Models
=============
'''


'''
DESC
    Staging table for collecting all of the item_ids to pull based on the recipe reagent and crafted item
    This will be used to determine which item_ids to load into the item table
'''

class StgRecipeItem(CommonData):
    stg_recipe_item_id = models.CharField('concat (recipe / reagent item / crafted item IDs) as dummy PK', max_length=256, primary_key=True) 
    recipe_id = models.IntegerField('recipe ID', default=0)
    item_id = models.IntegerField('reagent item ID', default=0)
    crafted_item_id = models.IntegerField('crafted item ID', default=0)
    skill_tier_id = models.IntegerField('skill tier ID', default=0)
    item_quantity = models.SmallIntegerField('reagent item quantity', default=0)

    
    class Meta:
        db_table = 'stg_recipe_item'
        
    
    def __str__(self):
        return CommonData.__str__(self)


'''
DESC
    Dim table for Recipes
    This model will be used with the Reagent model to capture crafting recipes
    Mostly maps to /recipe/{recipeId}
'''

class Recipe(CommonData, MediaData):
    recipe_id = models.IntegerField('recipe ID', primary_key=True) 
    skill_tier = models.ForeignKey(ProfessionSkillTier, on_delete=models.CASCADE)
    crafted_item = models.ForeignKey(Item, on_delete=models.CASCADE)
    min_quantity = models.SmallIntegerField('min quantity produced', default=1)
    max_quantity = models.SmallIntegerField('max quantity produced', default=1)

    
    class Meta:
        db_table = 'recipe'
        
    
    def __str__(self):
        return CommonData.__str__(self)
        
        
'''
DESC
    Dim table for Reagents
    This model will be used with the Recipe model to capture crafting recipes
    Mostly maps to /recipe/{recipeId}
'''

class Reagent(CommonData):
    reagent_id = models.CharField('concat (recipe / item IDs) as dummy PK', max_length=256, primary_key=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_quantity = models.SmallIntegerField('quantity required', default=1)

    
    class Meta:
        db_table = 'reagent'
        
    
    def __str__(self):
        return CommonData.__str__(self)