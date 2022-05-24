from django.urls import path
from .views import *

urlpatterns = [
    # --------- functions
    path('campaign/search ', campaign_search, name='campaign-search'),
    path('campaign_csv_all', campaign_create_csv_all, name='campaign-csv-all'),
    path('campaign_csv/<int:list_name>', campaign_create_csv, name='campaign-csv'),
    path('download_sample/<str:file_type>', download_sample, name='download-sample'),

    # ---------Template views
    path('', home, name='dashboard'),
    path('api/chart/data/', ChartData.as_view()),
    path('contact-list/', ContactListView.as_view(), name='contact-list'),
    path('contact-list/create', ContactListCreateView.as_view(), name='contact-list-create'),
    path('contact-list/delete/<int:pk>', ContactListDeleteView.as_view(), name='contact-list-delete'),
    path('contact-list/<int:pk>', ContactListDetailView.as_view(), name='contact-list-detail'),
    path('contact-list/edit/<int:pk>', ContactListUpdateView.as_view(), name='contact-list-edit'),
    path('contact-list/add-create/<int:pk>', ContactCreateView.as_view(), name='contact-create'),
    path('contact/delete/<int:pk>', ContactDeleteView.as_view(), name='contact-delete'),
    path('campaign', CampaignListView.as_view(), name='campaign'),
    path('campaign/create', CampaignCreateView.as_view(), name='campaign-create'),
    path('campaign/<int:list_name>', campaign_detail, name='campaign-detail'),
    path('campaign/contact/<int:pk>', SingleCampaignDetailView.as_view(), name='campaign-single'),

]

# path('campaign/create/single', SingleCampaignCreateView.as_view(), name='campaign-create-single'),
# path('campaign/<slug:slug>', CampaignDetailView.as_view(), name='campaign-detail'),