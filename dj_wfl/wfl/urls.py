from django.urls import path
from wfl.views import (
    ProfessionCreate, ProfessionList, ProfessionDetail,
    
    ProfessionSkillTierCreate, ProfessionSkillTierList, 
    ProfessionSkillTierDetail,
    
    StgRecipeItemCreate, StgRecipeItemList, StgRecipeItemDetail
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
]