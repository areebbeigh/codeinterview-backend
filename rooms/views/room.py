from urllib.parse import urljoin

from django.views.generic.base import View
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings

from rooms.models import Room, Language
from rooms.serializers import RoomSerializer, LanguageSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'room_id'

class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    lookup_field = 'code'
    lookup_value_regex = r'[^/]+'