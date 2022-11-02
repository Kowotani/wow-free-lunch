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


'''
DESC
    Dim table for Profession Skill Tiers, which generally map to expansions (eg. Legion,
    Shadowlands, Classic).
    Mostly maps to /profession/{professionID} endpoint
'''

class ProfessionSkillTier(CommonData):
    skill_tier_id = models.SmallIntegerField('skill tier ID', primary_key=True) 
    profession_id = models.ForeignKey(Profession, on_delete=models.CASCADE, db_column='profession_id')
    min_skill_level = models.SmallIntegerField('minimum skill level for this tier (eg. 1 for Burning Crusade)', default=0)
    max_skill_level = models.SmallIntegerField('maximum skill level for this tier (eg. 75 for Burning Crusade)', default=0)
    min_total_skill_level = models.SmallIntegerField('minimum total skill level (eg. 301 for Burning Crusade)', default=0)
    max_total_skill_level = models.SmallIntegerField('maximum total skill level (eg. 375 for Burning Crusade)', default=0)
    is_legacy_tier = models.BooleanField('TRUE if the tier requires previous tiers to unlock', default=False)
    
    class Meta:
        db_table = 'profession_skill_tier'

'''
===========
Item Models
===========
'''