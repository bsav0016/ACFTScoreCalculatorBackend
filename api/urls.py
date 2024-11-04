from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import UserViewSet, CustomObtainAuthToken, ACFTResultViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('acft_scores', ACFTResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(r'authenticate/', CustomObtainAuthToken.as_view())
]