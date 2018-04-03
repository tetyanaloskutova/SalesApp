
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

#from . import views as risktypes_views
from salesaccounts.views import *

router = DefaultRouter(trailing_slash=False)
router.register(r'riskfield', RiskFieldViewSet, base_name="riskfield")
router.register(r'risktype', RiskTypeViewSet, base_name="risktype")

urlpatterns = [
    # API URIs
    url(r'', include(router.urls)),
    url(r'^salesaccounts-auth/', include('rest_framework.urls', namespace='rest_framework')),
   	url(r'^users/$',  UserList.as_view(),name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='user-detail'),
	# URL that shows formatted fields for a particular risk type identified by PK (Task 3)
	url(r'^index/(?P<pk>[0-9]+)/$', index, name='index'),
]
