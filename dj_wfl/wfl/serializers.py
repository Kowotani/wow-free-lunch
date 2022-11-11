from rest_framework import serializers
from wfl.models import (Item, ItemClass, ItemClassHierarchy, ItemData, 
    Expansion, Profession, ProfessionSkillTier, Reagent, Recipe, StgRecipeItem)


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
    Item Class Hierarchy serializer
'''

class ItemClassHierarchySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemClassHierarchy
        fields = '__all__'


'''
DESC
    ItemData serializer
'''

class ItemDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemData
        fields = '__all__'


'''
DESC
    Item serializer
'''

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


'''
==================
Recipe Serializers
==================
'''

   
'''
DESC
    Stg Recipe Item serializer
'''

class StgRecipeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StgRecipeItem
        fields = '__all__'
        
        
'''
DESC
    Recipe serializer
'''

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'     


'''
DESC
    Reagent serializer
'''

class ReagentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reagent
        fields = '__all__'   
        
        
'''
================
Item Serializers
================
'''
        
        
'''
=====================
Expansion Serializers
=====================
'''


'''
DESC
    Expansion serializer
'''

class ExpansionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expansion
        fields = '__all__'