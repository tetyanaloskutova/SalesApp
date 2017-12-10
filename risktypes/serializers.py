from django.contrib.auth.models import User
from rest_framework import serializers
from risktypes import models

class UserSerializer(serializers.ModelSerializer):
	#risktypes = serializers.PrimaryKeyRelatedField(many=True, queryset=models.RiskType.objects.all())
	#url = serializers.HyperlinkedIdentityField(view_name="user-detail")

	class Meta:
		model = User
		#fields = ('url', 'username')
		fields = '__all__'# ('id', 'username', 'risktypes')

		
class RiskFieldSerializer(serializers.HyperlinkedModelSerializer):
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
