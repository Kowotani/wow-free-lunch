from rest_framework import serializers
from wfl.models import Profession, ProfessionSkillTier, StgRecipeItem


'''
======================
Profession Serializers
======================
'''


'''
DESC
    Profession serializer
'''

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = '__all__'
            

'''
DESC
    Profession Skill Tier serializer
'''

class ProfessionSkillTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionSkillTier
        fields = '__all__'
        

'''
DESC
    Stg Recipe Item serializer
'''

class StgRecipeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StgRecipeItem
        fields = '__all__'