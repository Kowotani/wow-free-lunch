from rest_framework import serializers
from wfl.models import Profession, ProfessionSkillTier


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
        fields = ['__all__']
            

'''
DESC
    Profession Skill Tier serializer
'''

class ProfessionSkillTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionSkillTier
        fields = ['__all__']