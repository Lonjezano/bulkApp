from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='dashboard'),
    path('contact-list/', ContactListView.as_view(), name='contact-list'),
    path('contact-list/create', ContactListCreateView.as_view(), name='contact-list-create'),
    path('contact-list/<int:pk>', ContactListDetailView.as_view(), name='contact-list-detail'),
    path('contact-list/add-create/<int:pk>', ContactCreateView.as_view(), name='contact-create'),
    path('campaign', CampaignListView.as_view(), name='campaign'),
    path('campaign/create', CampaignCreateView.as_view(), name='campaign-create'),
]