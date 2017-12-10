from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from .serializers import RiskTypeSerializer, RiskFieldSerializer, UserSerializer
from .permissions import IsStaffOrOwner, IsStaffOrOwnerField
from risktypes import models
from rest_framework import generics
from django.shortcuts import render


	
class RiskFieldViewSet(viewsets.ModelViewSet):
	serializer_class = RiskFieldSerializer
	permission_classes = (IsStaffOrOwnerField,)

	def get_queryset(self):
		if self.request.user.is_superuser:
			return models.RiskField.objects.all()
		else:
			return models.RiskField.objects.filter(user_riskfield=self.request.user)

	def perform_create(self, serializer):
		serializer.save(user_riskfield=self.request.user)

class RiskTypeViewSet(viewsets.ModelViewSet):
	serializer_class = RiskTypeSerializer
	permission_classes = (IsStaffOrOwner,)

	def get_queryset(self):
		if self.request.user.is_superuser:
			return models.RiskType.objects.all()
		else:
			return models.RiskType.objects.all() #filter(user_risktype = self.request.user)

	def perform_create(self, serializer):
		serializer.save(user_risktype = self.request.user)

	# The detail_route allows me to see all the riskfields of a risk type
	# with the following URL: /risktypes/risktype/(?P<pk>\d+)/riskfields

	@detail_route(url_path='formatted')
	def riskanswer(self, request, pk):
		risktype = models.RiskType.objects.get(pk=pk)
		riskfields = risktype.risktype_riskfield.all().order_by('order')
		serializer = RiskFieldSerializer(riskfields, context={'request': request})
		#return Response(serializer.data)
		return Response([riskfield.name for riskfield in riskfields])

class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	
	
def index(request, pk):
	context = {
	    'title':pk,
		'enum_values': ['red','blue','yellow'],
		'fields': [{
            "id": 1,
            "url": "http://127.0.0.1:8000/risktypes/riskfield/1",
            "user_riskfield": "http://127.0.0.1:8000/risktypes/users/6/",
            "risktype": "http://127.0.0.1:8000/risktypes/risktype/1",
            "name": "test",
            "description": "test",
            "type": 1,
            "length": 256,
            "len_decim": 0,
            "order": 1,
            "min_value": 0,
            "max_value": 256,
            "is_nullable": 'true',
            "enum_values": []
        },
        {
            "id": 2,
            "url": "http://127.0.0.1:8000/risktypes/riskfield/2",
            "user_riskfield": "http://127.0.0.1:8000/risktypes/users/6/",
            "risktype": "http://127.0.0.1:8000/risktypes/risktype/1",
            "name": "test 2",
            "description": "test2",
            "type": 2,
            "length": 256,
            "len_decim": 0,
            "order": 2,
            "min_value": 0,
            "max_value": 256,
            "is_nullable": 'true',
            "enum_values": []
        },{
            "id": 3,
            "url": "http://127.0.0.1:8000/risktypes/riskfield/2",
            "user_riskfield": "http://127.0.0.1:8000/risktypes/users/6/",
            "risktype": "http://127.0.0.1:8000/risktypes/risktype/1",
            "name": "test 3",
            "description": "test2",
            "type": 3,
            "length": 256,
            "len_decim": 0,
            "order": 3,
            "min_value": 0,
            "max_value": 256,
            "is_nullable": 'true',
            "enum_values": []
        },{
            "id": 4,
            "url": "http://127.0.0.1:8000/risktypes/riskfield/2",
            "user_riskfield": "http://127.0.0.1:8000/risktypes/users/6/",
            "risktype": "http://127.0.0.1:8000/risktypes/risktype/1",
            "name": "test 4",
            "description": "test2",
            "type": 4,
            "length": 256,
            "len_decim": 0,
            "order": 4,
            "min_value": 0,
            "max_value": 256,
            "is_nullable": 'true',
            "enum_values": ['red','blue','yellow']
        },],
	}
	return render(request, 'risktype.html', context)	