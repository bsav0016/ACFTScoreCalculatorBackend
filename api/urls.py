from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import UserViewSet, CustomObtainAuthToken, ACFTResultViewSet, PaymentSheetViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('acft_scores', ACFTResultViewSet)
router.register('payment_sheets', PaymentSheetViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(r'authenticate/', CustomObtainAuthToken.as_view())
]