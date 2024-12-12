from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'locations', views.LocationViewSet, basename='location')
router.register(r'dialogues', views.DialogueViewSet, basename='dialogue')
router.register(r'progress', views.PlayerProgressViewSet, basename='progress')

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
] 