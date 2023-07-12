# api.urls.py

from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.user_viewset, basename='users')
router.register(r'courses', views.course_viewset, basename='courses')

urlpatterns = router.urls
