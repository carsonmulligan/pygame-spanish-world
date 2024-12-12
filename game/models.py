from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    background_image = models.ImageField(upload_to='locations/', null=True, blank=True)
    x_position = models.IntegerField(default=50, help_text="X coordinate on the map (0-100)")
    y_position = models.IntegerField(default=50, help_text="Y coordinate on the map (0-100)")
    
    def __str__(self):
        return self.name

class Dialogue(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='dialogues')
    npc_text = models.TextField()
    correct_response = models.TextField()
    hint = models.CharField(max_length=200)
    difficulty = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.location.name} - {self.npc_text[:50]}..."

class PlayerProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    completed_dialogues = models.ManyToManyField(Dialogue, blank=True)
    score = models.IntegerField(default=0)
    last_played = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Progress"
