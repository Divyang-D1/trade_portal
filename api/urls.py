from django.urls import path
from .views import (
    RegisterView,
    CompanyListView,
    WatchlistView,
    AddToWatchlistView,
    RemoveFromWatchlistView
)
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('companies/', CompanyListView.as_view(), name='company-list'),
    path('watchlist/', WatchlistView.as_view(), name='watchlist'),
    path('watchlist/add/', AddToWatchlistView.as_view(), name='watchlist-add'),
    path('watchlist/remove/', RemoveFromWatchlistView.as_view(), name='watchlist-remove'),
]
