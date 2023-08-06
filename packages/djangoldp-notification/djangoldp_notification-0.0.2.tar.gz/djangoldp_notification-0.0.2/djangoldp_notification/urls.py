"""djangoldp_notifications URL Configuration"""
from django.conf.urls import url
from .models import Notification
from djangoldp.views import LDPViewSet


urlpatterns = [
    url(r'^notifications/', LDPViewSet.urls(model=Notification)),
]
