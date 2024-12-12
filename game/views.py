from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Location, Dialogue, PlayerProgress
from .serializers import (
    LocationSerializer,
    DialogueSerializer,
    PlayerProgressSerializer
)

def home(request):
    context = {}
    if request.user.is_authenticated:
        context['locations'] = Location.objects.all()
        context['player_progress'] = PlayerProgress.objects.filter(user=request.user).first()
    return render(request, 'game/home.html', context)

class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]

class DialogueViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DialogueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        location_id = self.request.query_params.get('location', None)
        if location_id:
            return Dialogue.objects.filter(location_id=location_id)
        return Dialogue.objects.none()

    @action(detail=True, methods=['post'])
    def check_answer(self, request, pk=None):
        dialogue = self.get_object()
        user_answer = request.data.get('answer', '').strip().lower()
        correct_answer = dialogue.correct_response.strip().lower()
        
        is_correct = user_answer == correct_answer
        
        if is_correct:
            progress = PlayerProgress.objects.get(user=request.user)
            progress.completed_dialogues.add(dialogue)
            progress.score += dialogue.difficulty * 10
            progress.save()
        
        return Response({
            'correct': is_correct,
            'hint': dialogue.hint if not is_correct else None
        })

class PlayerProgressViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PlayerProgress.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def change_location(self, request):
        location_id = request.data.get('location_id')
        if not location_id:
            return Response(
                {'error': 'location_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        location = get_object_or_404(Location, id=location_id)
        progress = get_object_or_404(PlayerProgress, user=request.user)
        progress.current_location = location
        progress.save()
        
        return Response(PlayerProgressSerializer(progress).data)
