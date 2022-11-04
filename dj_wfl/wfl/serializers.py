from rest_framework import serializers
from wfl.models import (ItemClass, ItemSubclass, Profession, 
    ProfessionSkillTier, StgRecipeItem)


'''
======================
Profession Serializers
======================
'''


'''
DESC
    Profession serializer
'''

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = '__all__'
            

'''
DESC
    Profession Skill Tier serializer
'''

class ProfessionSkillTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionSkillTier
        fields = '__all__'
        

'''
DESC
    Stg Recipe Item serializer
'''

class StgRecipeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StgRecipeItem
        fields = '__all__'
        
        
'''
================
Item Serializers
================
'''


'''
DESC
    Item Class serializer
'''

class ItemClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemClass
        fields = '__all__'
        
        
'''
DESC
    Item Sublass serializer
'''

class ItemSubclassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSubclass
        fields = '__all__'
            