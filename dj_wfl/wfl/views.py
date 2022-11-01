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
Supported methods: GET, PUT, PATCH, DELETE
'''
class ProfessionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer