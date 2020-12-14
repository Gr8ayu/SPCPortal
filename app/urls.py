from django.urls import path, include
from django.http import HttpResponse
from app import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    

    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('profile/', views.edit_contact_profile, name='profile_view'),
    path('profile/', views.edit_profile, name='edit_profile'),

    path('profile/edit/contact/', views.edit_contact_details, name='edit_profile_contact'),
    path('profile/edit/education/', views.edit_education_details, name='edit_profile_education'),
    path('profile/edit/details/', views.edit_profile_details, name='edit_profile_details'),
    


    path('offers/', login_required(views.OfferListView.as_view()), name='offers'),
    path('offer/details/<int:pk>/', login_required(views.OfferDetailView.as_view()), name='offer_details'),
    path('offer/sendmail/<int:pk>/', views.sendOfferAlert, name='offer_alert'),

    path('companies/', login_required(views.CompanyListView.as_view()), name='companies'),
    path('company/details/<int:pk>/', login_required(views.CompanyDetailView.as_view()), name='company_details'),

    path('applications/', login_required(views.ApplicationListView.as_view()), name='my_applications'),
    path('apply/<int:id>/', views.AddApplication, name='add_application'),
    

]


