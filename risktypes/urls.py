
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from . import views as risktypes_views

router = DefaultRouter(trailing_slash=False)
router.register(r'riskfield', risktypes_views.RiskFieldViewSet, base_name="riskfield")
router.register(r'risktype', risktypes_views.RiskTypeViewSet, base_name="risktype")

urlpatterns = [
    # API URIs
    url(r'', include(router.urls)),
    url(r'^risktypes-auth/', include('rest_framework.urls', namespace='rest_framework')),
   	url(r'^users/$',  risktypes_views.UserList.as_view(),name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', risktypes_views.UserDetail.as_view(), name='user-detail'),

]
