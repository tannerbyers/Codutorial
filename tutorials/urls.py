from . import views
from django.urls import path

urlpatterns = [
    path('tutorial/', views.GetTutorial.as_view(), name='home'),
    path('tutorial/<slug:slug>/', views.GetTutorial.as_view(), name='unique url'),
]