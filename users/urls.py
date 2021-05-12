from rest_framework import routers
from .views import BaseAuthViewSet

router = routers.DefaultRouter()
router.register('', BaseAuthViewSet, basename='auth_base')

urlpatterns = router.urls
