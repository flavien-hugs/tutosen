# api.urls.py

from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.user_view_set, basename='users')

urlpatterns = router.urls
