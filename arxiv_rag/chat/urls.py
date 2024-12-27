from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatView

router = DefaultRouter()
router.register(r'chat', ChatView, basename='chat')

urlpatterns = [
    path('', include(router.urls)),
]
