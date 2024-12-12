from django.contrib import admin
from .models import Location, Dialogue, PlayerProgress

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Dialogue)
class DialogueAdmin(admin.ModelAdmin):
    list_display = ('location', 'npc_text', 'difficulty')
    list_filter = ('location', 'difficulty')
    search_fields = ('npc_text', 'correct_response')

@admin.register(PlayerProgress)
class PlayerProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_location', 'score', 'last_played')
    list_filter = ('current_location',)
    search_fields = ('user__username',)
