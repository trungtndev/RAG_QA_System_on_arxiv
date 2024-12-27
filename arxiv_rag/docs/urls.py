from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentView

router = DefaultRouter()
router.register(r'docs', DocumentView, basename='docs')

urlpatterns = [
    path('', include(router.urls)),

]
