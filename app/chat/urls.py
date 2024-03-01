from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chat.views.chat_viewset import ChatViewSet

router = DefaultRouter()
router.register('Chat',
                ChatViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
