from django.http import Http404
from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from wfl.models import Profession
from wfl.serializers import ProfessionSerializer


'''
================
Profession Views
================
'''


'''
Creates a list of Professions
'''
class ProfessionList(generics.ListCreateAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    
    
'''
Manages CRUD operations for a Profession
'''
class ProfessionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer