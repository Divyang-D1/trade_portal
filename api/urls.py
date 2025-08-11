from django.urls import path
from .views import (
    RegisterView,
    CompanyListView,
    WatchlistView,
    CreateWatchlist,
    AddCompanyToWatchlist,
    RemoveCompanyFromWatchlist,
)
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('companies/', CompanyListView.as_view(), name='company-list'),
    path('watchlists/', WatchlistView.as_view(), name='watchlist-list'),
    path('watchlists/create/', CreateWatchlist.as_view(), name='watchlist-create'),
    path('watchlists/add-companies/', AddCompanyToWatchlist.as_view(), name='watchlist-add-companies'),
    path('watchlists/remove-company/', RemoveCompanyFromWatchlist.as_view(), name='watchlist-remove-company'),
]