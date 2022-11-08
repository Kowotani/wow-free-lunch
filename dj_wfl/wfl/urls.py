from django.urls import path
from wfl.views import (
    ItemCreate, ItemList, ItemDetail,
    
    ItemClassCreate, ItemClassList, ItemClassDetail,
    
    ItemClassHierarchyCreate, ItemClassHierarchyList, ItemClassHierarchyDetail,
    
    ItemDataCreate, ItemDataList, ItemDataDetail,
    
    ProfessionCreate, ProfessionList, ProfessionDetail,
    
    ProfessionSkillTierCreate, ProfessionSkillTierList, 
    ProfessionSkillTierDetail,
    
    StgRecipeItemCreate, StgRecipeItemList, StgRecipeItemDetail,
    )

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
    
    path('profession/stg_recipe_item/create', StgRecipeItemCreate.as_view()),
    path('profession/stg_recipe_item/all', StgRecipeItemList.as_view()),
    path('profession/stg_recipe_item/<pk>', StgRecipeItemDetail.as_view()),
    
    
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
]