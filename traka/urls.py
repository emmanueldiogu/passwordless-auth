from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('profile', views.ProfileViewSet)

urlpatterns = router.urls
