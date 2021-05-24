from rest_framework import routers
from .views import CoursesViewSet, StepsViewSet

router = routers.DefaultRouter()
router.register('courses', CoursesViewSet, basename='courses_base')
router.register('steps', StepsViewSet, basename='steps_base')

urlpatterns = router.urls
