
from django.urls import path
from .views import StudentListView, OfferListView, ApplicationListView, StudentDetailView, addOffer, index, EditOfferStudents
urlpatterns = [
    path('',index, name='Home' ),
    path('students/',StudentListView.as_view() ),
    path('students/<int:pk>/',StudentDetailView.as_view() ),


    path('offers/',OfferListView.as_view() ),
    path('offers/<int:pk>/students',EditOfferStudents ),
    
    path('applications/',ApplicationListView.as_view() ),
    path('add/offer/',addOffer ),

]
