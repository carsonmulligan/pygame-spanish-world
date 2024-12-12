from rest_framework import serializers
from .models import Location, Dialogue, PlayerProgress
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class DialogueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dialogue
        fields = ('id', 'npc_text', 'hint', 'difficulty')

class PlayerProgressSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    current_location = LocationSerializer(read_only=True)
    completed_dialogues = DialogueSerializer(many=True, read_only=True)

    class Meta:
        model = PlayerProgress
        fields = '__all__' 