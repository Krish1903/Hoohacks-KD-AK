from django.shortcuts import render, HttpResponse, redirect
from .models import UserProfile, Event
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Event, UserProfile
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.urls import reverse

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

def index(request):
    return HttpResponse("Hello, world!")

def personalize_screen(request):
    return render(request, 'personalize.html')

def leaderboard(request):
    leaderboard_data = UserProfile.objects.all().order_by('-points')
    context = {'leaderboard': leaderboard_data}
    return render(request, 'leaderboard.html', context)

def add_points(user, points):
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.points += points
    profile.save()

def event_list(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'event_list.html', {'events': events})

def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'event_detail.html', {'event': event})

def scan_qr_code(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        if request.user.is_authenticated:
            user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

            if event not in user_profile.scanned_events.all():
                request.session['event_id_for_points'] = event_id
                return render(request, 'points_added_success.html') 
            else:
                return render(request, 'already_scanned.html')
        else:
            request.session['event_id_for_points'] = event_id
            login_url = reverse('login')
            return redirect(f'{login_url}?next={request.path}')
    except Event.DoesNotExist:
        return render(request, {'error': 'Event not found'})



@receiver(user_logged_in)
def add_points_post_login(sender, request, user, **kwargs):
    event_id = request.session.pop('event_id_for_points', None)
    if event_id:
        try:
            event = Event.objects.get(id=event_id)
            user_profile, _ = UserProfile.objects.get_or_create(user=user)
            if event not in user_profile.scanned_events.all():
                user_profile.points += event.point_value
                user_profile.scanned_events.add(event)
                user_profile.save()
        except Event.DoesNotExist:
            pass 
