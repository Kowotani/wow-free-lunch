from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views import View

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from wfl.models import (Auction, AuctionHouse, ConnectedRealm, Expansion, Item, 
    ItemClass, ItemClassHierarchy, ItemData, Profession, ProfessionSkillTier, 
    Reagent, Realm, RealmConnection, Recipe, Region, StgRecipeItem)
    
from wfl.serializers import (AuctionSerializer, AuctionHouseSerializer, 
    ConnectedRealmSerializer, ExpansionSerializer, ItemClassSerializer, 
    ItemClassHierarchySerializer, ItemDataSerializer, ItemSerializer, 
    ProfessionSerializer,  ProfessionSkillTierSerializer, ReagentSerializer, 
    RealmSerializer, RealmConnectionSerializer, RecipeSerializer, 
    RegionSerializer, StgRecipeItemSerializer)

from wfl.utils import QueryManager

import json


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
    queryset = ItemData.objects.all()[:1000]
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
    queryset = Item.objects.all()[:1000]
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
    queryset = StgRecipeItem.objects.all()[:1000]
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
    queryset = Recipe.objects.all()[:1000]
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
    queryset = Reagent.objects.all()[:1000]
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
-----
Realm
-----
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
    
    
'''
--------------
ConnectedRealm
--------------
'''


'''
Creates a Connected Realm
Supported methods: POST
'''
class ConnectedRealmCreate(generics.CreateAPIView):
    queryset = ConnectedRealm.objects.all()
    serializer_class = ConnectedRealmSerializer
    

'''
Retrieve list of Connected Realms
Supported methods: GET
'''
class ConnectedRealmList(generics.ListAPIView):
    queryset = ConnectedRealm.objects.all()
    serializer_class = ConnectedRealmSerializer
    
    
'''
Manages read / update / delete operations for a Connected Realm
Supported methods: GET / PUT / PATCH / DELETE
'''
class ConnectedRealmDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ConnectedRealm.objects.all()
    serializer_class = ConnectedRealmSerializer
    
    
'''
---------------
RealmConnection
---------------
'''


'''
Creates a Realm Connection
Supported methods: POST
'''
class RealmConnectionCreate(generics.CreateAPIView):
    queryset = RealmConnection.objects.all()
    serializer_class = RealmConnectionSerializer
    

'''
Retrieve list of Realm Connections
Supported methods: GET
'''
class RealmConnectionList(generics.ListAPIView):
    queryset = RealmConnection.objects.all()
    serializer_class = RealmConnectionSerializer
    
    
'''
Manages read / update / delete operations for a Realm Connection
Supported methods: GET / PUT / PATCH / DELETE
'''
class RealmConnectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RealmConnection.objects.all()
    serializer_class = RealmConnectionSerializer
    
    
'''
-------
Auction
-------
'''


'''
Creates an Auction
Supported methods: POST
'''
class AuctionCreate(generics.CreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    

'''
Retrieve list of Auctions
Supported methods: GET
'''
class AuctionList(generics.ListAPIView):
    queryset = Auction.objects.all()[:1000]
    serializer_class = AuctionSerializer
    
    
'''
Manages read / update / delete operations for an Auction
Supported methods: GET / PUT / PATCH / DELETE
'''
class AuctionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    

'''
------------
AuctionHouse
------------
'''


'''
Creates an Auction House
Supported methods: POST
'''
class AuctionHouseCreate(generics.CreateAPIView):
    queryset = AuctionHouse.objects.all()
    serializer_class = AuctionHouseSerializer
    

'''
Retrieve list of Auction Houses
Supported methods: GET
'''
class AuctionHouseList(generics.ListAPIView):
    queryset = AuctionHouse.objects.all()
    serializer_class = AuctionHouseSerializer
    
    
'''
Manages read / update / delete operations for an Auction House
Supported methods: GET / PUT / PATCH / DELETE
'''
class AuctionHouseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AuctionHouse.objects.all()
    serializer_class = AuctionHouseSerializer
    
    
'''
================
FE API Endpoints
================
'''

'''
--------------
Profession Nav
--------------
'''

'''
This class provides endpoints for retrieving Reagent prices
'''
class ReagentPrices(View) :
    
    '''
    Retrieve Reagent Prices for the given inputs
    - profession
    - realm
    - faction
    - date (date or latest)
    Supported methods: POST
    '''
    def post(self, request):
    
        response_data = {}
        qm = QueryManager()
        
        # parse inputs
        data = request.POST
        profession = data.get('profession')
        realm = data.get('realm')
        faction = data.get('faction')
        date = data.get('date')
        
        # get latest update_data if required
        if date == 'latest':
            sql = '''
				SELECT MAX(update_date) AS update_data
				FROM auction a
				JOIN auction_house ah ON a.auction_house_id = ah.auction_house_id
				JOIN realm_connection rc ON ah.connected_realm_id = rc.connected_realm_id
				JOIN realm r ON rc.realm_id = r.realm_id
				WHERE 
					r.name = %s
					AND ah.faction = %s
            '''
            params = [realm, faction]
            res = qm.query(sql, params)
            date = res[0]['update_date']
        
        # query data
        sql = '''
            SELECT DISTINCT
            	ich.class_name,
            	ich.subclass_name,
            	i.item_id,
            	i.name,
            	id.level,
            	id.quality,
            	id.media_url,
            	ap.quantity,
            	IF(id.is_vendor_item, id.purchase_price, ap.min_price) AS min_price,
            	IF(id.is_vendor_item, id.purchase_price, ap.vwap_price) AS vwap_price
            FROM profession p
            JOIN profession_skill_tier pst ON p.profession_id = pst.profession_id
            JOIN expansion e ON pst.expansion_id = e.expansion_id
            JOIN recipe rec ON pst.skill_tier_id = rec.skill_tier_id
            JOIN reagent rea ON rec.recipe_id = rea.recipe_id
            LEFT JOIN item i ON rea.item_id = i.item_id
            LEFT JOIN item_class_hierarchy ich ON i.item_class_hierarchy_id = ich.item_class_hierarchy_id
            LEFT JOIN item_data id ON i.classic_item_data_id = id.item_data_id
            LEFT JOIN 
            (
            	SELECT 
            		a.item_id,
            		SUM(a.quantity) AS quantity,
            		MIN(CASE WHEN a.buyout_unit_price > 0 THEN a.buyout_unit_price END) AS min_price,
            		CEIL(SUM(a.buyout_unit_price * a.quantity) / SUM(a.quantity)) AS vwap_price
            	FROM auction a 
            	JOIN auction_house ah ON a.auction_house_id = ah.auction_house_id
            	JOIN realm_connection rc ON ah.connected_realm_id = rc.connected_realm_id
            	JOIN realm r ON rc.realm_id = r.realm_id
            	WHERE 
            		r.name = %s
            		AND ah.faction = %s
            		AND a.update_date = %s
            	GROUP BY 1
            ) ap ON i.item_id = ap.item_id
            WHERE 
            	p.name = %s
            	AND e.is_classic
            	AND id.level IS NOT NULL
            ORDER BY
            	ich.class_name,
            	ich.subclass_name,
            	id.level,
            	i.item_id;            
        '''
        params = [realm, faction, date, profession]
        res = qm.query(sql, params)
        
        # return data
        
        return HttpResponse(json.dumps(res), 
            content_type='application/json')
