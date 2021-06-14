from rest_framework import routers
from .views import (
    TeacherCoursesViewSet,
    TeacherStepsViewSet,
    StudentCoursesViewSet,
    StudentStepsViewSet,
    AllCoursesViewSet,
)

router = routers.DefaultRouter()
router.register('overall_courses', AllCoursesViewSet, basename='courses_base')

router.register('teacher_courses', TeacherCoursesViewSet, basename='t_courses_base')
router.register('teacher_steps', TeacherStepsViewSet, basename='t_steps_base')

router.register('student_courses', StudentCoursesViewSet, basename='s_courses_base')
router.register('student_steps', StudentStepsViewSet, basename='s_steps_base')

urlpatterns = router.urls
