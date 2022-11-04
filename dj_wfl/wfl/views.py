from django.http import Http404
from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from wfl.models import (ItemClass, ItemClassHierarchy, Profession, ProfessionSkillTier, 
    StgRecipeItem)
from wfl.serializers import (ItemClassSerializer, ItemClassHierarchySerializer, 
    ProfessionSerializer, ProfessionSkillTierSerializer, StgRecipeItemSerializer)
    


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