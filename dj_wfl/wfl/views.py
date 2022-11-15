from django.http import Http404
from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from wfl.models import (Item, ItemClass, ItemClassHierarchy, ItemData, 
    Expansion, Profession, ProfessionSkillTier, Reagent, Realm, Recipe, Region, 
    StgRecipeItem)
    
from wfl.serializers import (ItemSerializer, ItemClassSerializer, 
    ItemClassHierarchySerializer, ItemDataSerializer, ProfessionSerializer, 
    ExpansionSerializer, ProfessionSkillTierSerializer, ReagentSerializer,
    RealmSerializer, RecipeSerializer, RegionSerializer, StgRecipeItemSerializer)
    


'''
================
Profession Views
================
'''


'''
----------
Profession
----------
'''


'''
Creates a Profession
Supported methods: POST
'''
class ProfessionCreate(generics.CreateAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    

'''
Retrieve list of Professions
Supported methods: GET
'''
class ProfessionList(generics.ListAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    
    
'''
Manages read / update / delete operations for a Profession
Supported methods: GET / PUT / PATCH / DELETE
'''
class ProfessionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    

'''
---------------------
Profession Skill Tier
---------------------
'''


'''
Creates a Profession Skill Tier
Supported methods: POST
'''
class ProfessionSkillTierCreate(generics.CreateAPIView):
    queryset = ProfessionSkillTier.objects.all()
    serializer_class = ProfessionSkillTierSerializer
    

'''
Retrieve list of Profession Skill Tiers
Supported methods: GET
'''
class ProfessionSkillTierList(generics.ListAPIView):
    queryset = ProfessionSkillTier.objects.all()
    serializer_class = ProfessionSkillTierSerializer
    
    
'''
Manages read / update / delete operations for a Profession Skill Tier
Supported methods: GET / PUT / PATCH / DELETE
'''
class ProfessionSkillTierDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProfessionSkillTier.objects.all()
    serializer_class = ProfessionSkillTierSerializer
    
    
'''
==========
Item Views
==========
'''


'''
----------
Item Class
----------
'''


'''
Creates an Item Class
Supported methods: POST
'''
class ItemClassCreate(generics.CreateAPIView):
    queryset = ItemClass.objects.all()
    serializer_class = ItemClassSerializer
    

'''
Retrieve list of Item Classes
Supported methods: GET
'''
class ItemClassList(generics.ListAPIView):
    queryset = ItemClass.objects.all()
    serializer_class = ItemClassSerializer
    
    
'''
Manages read / update / delete operations for an Item Class
Supported methods: GET / PUT / PATCH / DELETE
'''
class ItemClassDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ItemClass.objects.all()
    serializer_class = ItemClassSerializer
    

'''
--------------------
Item Class Hierarchy
--------------------
'''


'''
Creates an Item Class Hierarchy
Supported methods: POST
'''
class ItemClassHierarchyCreate(generics.CreateAPIView):
    queryset = ItemClassHierarchy.objects.all()
    serializer_class = ItemClassHierarchySerializer
    

'''
Retrieve list of Item Subclasses
Supported methods: GET
'''
class ItemClassHierarchyList(generics.ListAPIView):
    queryset = ItemClassHierarchy.objects.all()
    serializer_class = ItemClassHierarchySerializer
    
    
'''
Manages read / update / delete operations for an Item Subclass
Supported methods: GET / PUT / PATCH / DELETE
'''
class ItemClassHierarchyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ItemClassHierarchy.objects.all()
    serializer_class = ItemClassHierarchySerializer
     
    
'''
---------
Item Data
---------
'''


'''
Creates an Item Data
Supported methods: POST
'''
class ItemDataCreate(generics.CreateAPIView):
    queryset = ItemData.objects.all()
    serializer_class = ItemDataSerializer
    

'''
Retrieve list of Item Datas
Supported methods: GET
'''
class ItemDataList(generics.ListAPIView):
    queryset = ItemData.objects.all()
    serializer_class = ItemDataSerializer
    
    
'''
Manages read / update / delete operations for an Item Data
Supported methods: GET / PUT / PATCH / DELETE
'''
class ItemDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ItemData.objects.all()
    serializer_class = ItemDataSerializer  
    
'''
----
Item
----
'''


'''
Creates an Item
Supported methods: POST
'''
class ItemCreate(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    

'''
Retrieve list of Items
Supported methods: GET
'''
class ItemList(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    
    
'''
Manages read / update / delete operations for an Item
Supported methods: GET / PUT / PATCH / DELETE
'''
class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    
    
'''
============
Recipe Views
============
'''
    
    
'''
---------------
Stg Recipe Item
---------------
'''

    
'''
Creates a StgRecipeItem
Supported methods: POST
'''
class StgRecipeItemCreate(generics.CreateAPIView):
    queryset = StgRecipeItem.objects.all()
    serializer_class = StgRecipeItemSerializer
    

'''
Retrieve list of Stg Recipe Items
Supported methods: GET
'''
class StgRecipeItemList(generics.ListAPIView):
    queryset = StgRecipeItem.objects.all()
    serializer_class = StgRecipeItemSerializer
    
    
'''
Manages read / update / delete operations for a Stg Recipe Item
Supported methods: GET / PUT / PATCH / DELETE
'''
class StgRecipeItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = StgRecipeItem.objects.all()
    serializer_class = StgRecipeItemSerializer
    
 
'''
------
Recipe
------
'''

    
'''
Creates a Recipe
Supported methods: POST
'''
class RecipeCreate(generics.CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    

'''
Retrieve list of Recipes
Supported methods: GET
'''
class RecipeList(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    
    
'''
Manages read / update / delete operations for a Recipe
Supported methods: GET / PUT / PATCH / DELETE
'''
class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer 


'''
-------
Reagent
-------
'''

    
'''
Creates a Reagent
Supported methods: POST
'''
class ReagentCreate(generics.CreateAPIView):
    queryset = Reagent.objects.all()
    serializer_class = ReagentSerializer
    

'''
Retrieve list of Reagents
Supported methods: GET
'''
class ReagentList(generics.ListAPIView):
    queryset = Reagent.objects.all()
    serializer_class = ReagentSerializer
    
    
'''
Manages read / update / delete operations for a Reagent
Supported methods: GET / PUT / PATCH / DELETE
'''
class ReagentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reagent.objects.all()
    serializer_class = ReagentSerializer 
 
    
'''
===================
Game Metadata Views
===================
'''


'''
---------
Expansion
---------
'''


'''
Creates an Expansion
Supported methods: POST
'''
class ExpansionCreate(generics.CreateAPIView):
    queryset = Expansion.objects.all()
    serializer_class = ExpansionSerializer
    

'''
Retrieve list of Expansions
Supported methods: GET
'''
class ExpansionList(generics.ListAPIView):
    queryset = Expansion.objects.all()
    serializer_class = ExpansionSerializer
    
    
'''
Manages read / update / delete operations for an Expansion
Supported methods: GET / PUT / PATCH / DELETE
'''
class ExpansionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expansion.objects.all()
    serializer_class = ExpansionSerializer
    
    
'''
------
Region
------
'''


'''
Creates a Region
Supported methods: POST
'''
class RegionCreate(generics.CreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    

'''
Retrieve list of Regions
Supported methods: GET
'''
class RegionList(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    
    
'''
Manages read / update / delete operations for an Region
Supported methods: GET / PUT / PATCH / DELETE
'''
class RegionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    
    
'''
---------
Realm
---------
'''


'''
Creates a Realm
Supported methods: POST
'''
class RealmCreate(generics.CreateAPIView):
    queryset = Realm.objects.all()
    serializer_class = RealmSerializer
    

'''
Retrieve list of Realms
Supported methods: GET
'''
class RealmList(generics.ListAPIView):
    queryset = Realm.objects.all()
    serializer_class = RealmSerializer
    
    
'''
Manages read / update / delete operations for a Realm
Supported methods: GET / PUT / PATCH / DELETE
'''
class RealmDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Realm.objects.all()
    serializer_class = RealmSerializer