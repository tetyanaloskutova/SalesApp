from django.contrib.auth.models import User
from rest_framework import serializers
from risktypes import models

class UserSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = User
		fields = '__all__'# ('id', 'username', 'risktypes')

		
class RiskFieldSerializer(serializers.HyperlinkedModelSerializer):
	""" Validations on the correct combinations of field formats (i.e. min_value is valid for date but not for text,
	length is valid for text but not for enum, etc.) were not implemented as this was not mentioned as part of the task.
	
	"""
	user_riskfield = serializers.HyperlinkedRelatedField(view_name="user-detail", read_only=True)

	class Meta:
		model = models.RiskField
		fields = ('id', 'url', 'user_riskfield', 'risktype', 'name','description', 'type', 'length', 'len_decim', 'order', 'min_value', 'max_value', 'is_nullable', 'enum_values')

class RiskTypeSerializer(serializers.HyperlinkedModelSerializer):
	risktype_riskfield = serializers.HyperlinkedRelatedField(many=True, required=False, view_name='riskfield-detail', read_only=True)
	user_risktype = serializers.HyperlinkedRelatedField(view_name="user-detail", read_only=True)

	class Meta:
		model = models.RiskType
		fields = ('id', 'url', 'user_risktype', 'risktype_riskfield','name','description')
