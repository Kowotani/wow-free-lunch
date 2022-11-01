from django.urls import path
from wfl.views import ProfessionCreate, ProfessionList, ProfessionDetail

urlpatterns = [
    path('profession', ProfessionCreate.as_view()),
    path('profession/all', ProfessionList.as_view()),
    path('profession/<pk>', ProfessionDetail.as_view()),
]