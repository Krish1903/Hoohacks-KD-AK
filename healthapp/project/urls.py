from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.index, name="index"),
    path('personalize/', views.personalize_screen, name="personalize"),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('scan/<int:event_id>/', views.scan_qr_code, name='scan_qr_code'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
