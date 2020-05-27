from rest_framework import serializers

from rooms.models import Room, Language


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ['room_id', 'participants']

    def create(self, validated_data):
        if validated_data.get('participants'):
            del validated_data['participants']
        return super(RoomSerializer, self).create(validated_data)


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = ['name', 'code', 'template']