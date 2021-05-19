from rest_framework import routers
from .views import UploadViewSet

router = routers.DefaultRouter()
router.register('', UploadViewSet, basename='upload')

urlpatterns = router.urls
