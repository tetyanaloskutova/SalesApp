from django.contrib.auth.models import User
from rest_framework import serializers
from salesaccounts import models

class UserSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = User
		fields = '__all__'# ('id', 'username', 'salesaccounts')

		
class AccountSerializer(serializers.HyperlinkedModelSerializer):
	user_riskfield = serializers.HyperlinkedRelatedField(view_name="user-detail", read_only=True)

	class Meta:
		model = models.Account
		fields = '__all__'

class PersonSerializer(serializers.HyperlinkedModelSerializer):
	user_risktype = serializers.HyperlinkedRelatedField(view_name="user-detail", read_only=True)

	class Meta:
		model = models.Person
		fields = '__all__'
