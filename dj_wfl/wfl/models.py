from django.db import models

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
    media_url = models.CharField('URL of the media asset', max_length=512, unique=True)
    media_file_data_id = models.IntegerField('ID provided by Battle.net endpoints', null=True)

    
    class Meta:
        abstract = True


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

    
    class Meta:
        db_table = 'profession_skill_tier'
        
    
    def __str__(self):
        return CommonData.__str__(self)


'''
DESC
    Staging table for collecting all of the item_ids to pull based on the recipe reagent and crafted item
    This will be used to determine which item_ids to load into the item table
'''

class StgRecipeItem(CommonData):
    stg_recipe_item_id = models.IntegerField('concatenation of IDs for recipe / item / crafted_item', primary_key=True) 
    recipe_id = models.IntegerField('recipe ID', default=0)
    item_id = models.IntegerField('reagent item ID', default=0)
    crafted_item_id = models.IntegerField('crafted item ID', default=0)

    
    class Meta:
        db_table = 'stg_recipe_item'
        
    
    def __str__(self):
        return CommonData.__str__(self)


'''
===========
Item Models
===========
'''