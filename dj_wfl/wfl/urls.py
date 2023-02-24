from django.urls import path
from django.views.decorators.cache import cache_page

from wfl.views import (
    
    # Metadata
    AuctionCreate, AuctionList, AuctionDetail,    
    
    AuctionHouseCreate, AuctionHouseList, AuctionHouseDetail,

    ConnectedRealmCreate, ConnectedRealmList, ConnectedRealmDetail,
    
    ItemCreate, ItemList, ItemDetail,
    
    ItemClassCreate, ItemClassList, ItemClassDetail,
    
    ItemClassHierarchyCreate, ItemClassHierarchyList, ItemClassHierarchyDetail,
    
    ItemDataCreate, ItemDataList, ItemDataDetail,
    
    ExpansionCreate, ExpansionList, ExpansionDetail,
    
    ProfessionCreate, ProfessionList, ProfessionDetail,
    
    ProfessionSkillTierCreate, ProfessionSkillTierList, 
    ProfessionSkillTierDetail,
    
    ReagentCreate, ReagentList, ReagentDetail,
    
    RealmCreate, RealmList, RealmDetail,
    
    RealmConnectionCreate, RealmConnectionList, RealmConnectionDetail,    
    
    RecipeCreate, RecipeList, RecipeDetail,
    
    RegionCreate, RegionList, RegionDetail,

    StgRecipeItemCreate, StgRecipeItemList, StgRecipeItemDetail,
    
    # FE API Endpoints
    AllFreeLunches, CraftedItemRecipes, ReagentPrices,
)


# =========
# Constants
# =========

DYNAMIC_CACHE_DURATION = 60 * 60 * 1   # 1 hour
STATIC_CACHE_DURATION = 60 * 60 * 24   # 24 hours


urlpatterns = [
    
    # ===========
    # Professions
    # ===========
    
    path('profession/create', ProfessionCreate.as_view()),
    path('profession/all', ProfessionList.as_view()),
    path('profession/<pk>', ProfessionDetail.as_view()),
    
    path('profession/skill_tier/create', ProfessionSkillTierCreate.as_view()),
    path('profession/skill_tier/all', ProfessionSkillTierList.as_view()),
    path('profession/skill_tier/<pk>', ProfessionSkillTierDetail.as_view()),
    
    
    # =====
    # Items
    # =====
    
    path('item/create', ItemCreate.as_view()),
    path('item/all', ItemList.as_view()),
    path('item/<pk>', ItemDetail.as_view()),
    
    path('item/item_data/create', ItemDataCreate.as_view()),
    path('item/item_data/all', ItemDataList.as_view()),
    path('item/item_data/<pk>', ItemDataDetail.as_view()),
    
    path('item/item_class/create', ItemClassCreate.as_view()),
    path('item/item_class/all', ItemClassList.as_view()),
    path('item/item_class/<pk>', ItemClassDetail.as_view()),

    path('item/item_class_hierarchy/create', ItemClassHierarchyCreate.as_view()),
    path('item/item_class_hierarchy/all', ItemClassHierarchyList.as_view()),
    path('item/item_class_hierarchy/<pk>', ItemClassHierarchyDetail.as_view()),
    
   
    # =======
    # Recipes
    # =======
    
    path('recipe/stg_recipe_item/create', StgRecipeItemCreate.as_view()),
    path('recipe/stg_recipe_item/all', StgRecipeItemList.as_view()),
    path('recipe/stg_recipe_item/<pk>', StgRecipeItemDetail.as_view()),   
    
    path('recipe/create', RecipeCreate.as_view()),
    path('recipe/all', RecipeList.as_view()),
    path('recipe/<pk>', RecipeDetail.as_view()), 
    
    path('recipe/reagent/create', ReagentCreate.as_view()),
    path('recipe/reagent/all', ReagentList.as_view()),
    path('recipe/reagent/<pk>', ReagentDetail.as_view()), 
    
    
    # =============
    # Game Metadata
    # =============
    
    # ----------
    # Expansions
    # ----------
    
    path('expansion/create', ExpansionCreate.as_view()),
    path('expansion/all', ExpansionList.as_view()),
    path('expansion/<pk>', ExpansionDetail.as_view()),
    
    # ------
    # Realms
    # ------
    
    path('region/create', RegionCreate.as_view()),
    path('region/all', RegionList.as_view()),
    path('region/<pk>', RegionDetail.as_view()),
    
    path('realm/create', RealmCreate.as_view()),
    path('realm/all', RealmList.as_view()),
    path('realm/<pk>', RealmDetail.as_view()),
    
    path('connected_realm/create', ConnectedRealmCreate.as_view()),
    path('connected_realm/all', ConnectedRealmList.as_view()),
    path('connected_realm/<pk>', ConnectedRealmDetail.as_view()),
    
    path('connected_realm/realm_connection/create', 
        RealmConnectionCreate.as_view()),
    path('connected_realm/realm_connection/all', 
        RealmConnectionList.as_view()),
    path('connected_realm/realm_connection/<pk>', 
        RealmConnectionDetail.as_view()),
    
    # --------
    # Auctions
    # --------
    
    path('auction/create', AuctionCreate.as_view()),
    path('auction/all', AuctionList.as_view()),
    path('auction/<pk>', AuctionDetail.as_view()),
    
    path('auction_house/create', AuctionHouseCreate.as_view()),
    path('auction_house/all', AuctionHouseList.as_view()),
    path('auction_house/<pk>', AuctionHouseDetail.as_view()),
    
    
    # ================
    # FE API Endpoints
    # ================
    
    path('api/reagent_prices', 
        cache_page(DYNAMIC_CACHE_DURATION)(ReagentPrices.as_view())),
    path('api/crafted_item_recipes', 
        cache_page(STATIC_CACHE_DURATION)(CraftedItemRecipes.as_view())),
    path('api/all_free_lunches', 
        cache_page(DYNAMIC_CACHE_DURATION)(AllFreeLunches.as_view())),
]