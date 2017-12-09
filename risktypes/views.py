from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from .serializers import RiskTypeSerializer, RiskFieldSerializer, UserSerializer
from .permissions import IsStaffOrOwner
from risktypes import models
from rest_framework import generics

class RiskFieldViewSet(viewsets.ModelViewSet):
	serializer_class = RiskFieldSerializer
	permission_classes = (IsStaffOrOwner,)

	def get_queryset(self):
		if self.request.user.is_superuser:
			return models.RiskField.objects.all()
		else:
			return self.request.user.user_riskfield.all()

	def perform_create(self, serializer):
		serializer.save(user_riskfield=self.request.user)

class RiskTypeViewSet(viewsets.ModelViewSet):
	serializer_class = RiskTypeSerializer
	permission_classes = (IsStaffOrOwner,)

	def get_queryset(self):
		if self.request.user.is_superuser:
			return models.RiskType.objects.all()
		else:
			return self.request.user.user_risktype.all()

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