from django.urls import path
from wfl.views import (
    ItemClassCreate, ItemClassList, ItemClassDetail,
    
    ItemClassHierarchyCreate, ItemClassHierarchyList, ItemClassHierarchyDetail,
    
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
    
    path('item/item_class/create', ItemClassCreate.as_view()),
    path('item/item_class/all', ItemClassList.as_view()),
    path('item/item_class/<pk>', ItemClassDetail.as_view()),

    path('item/item_class_hierarchy/create', ItemClassHierarchyCreate.as_view()),
    path('item/item_class_hierarchy/all', ItemClassHierarchyList.as_view()),
    path('item/item_class_hierarchy/<pk>', ItemClassHierarchyDetail.as_view()),
]