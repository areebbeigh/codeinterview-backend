from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from rooms.views.home import HomePageView
from rooms.views.room import RoomViewSet, LanguageViewSet

router = routers.DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'languages', LanguageViewSet)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
