from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Company, Watchlist, WatchlistItem
from .serializers import UserSerializer, CompanySerializer, WatchlistSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        symbol = self.request.query_params.get('symbol')
        scripcode = self.request.query_params.get('scripcode')

        if name:
            queryset = queryset.filter(company_name__icontains=name)
        if symbol:
            queryset = queryset.filter(symbol__icontains=symbol)
        if scripcode:
            queryset = queryset.filter(scripcode__icontains=scripcode)
        return queryset

class WatchlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        watchlists = Watchlist.objects.filter(user=request.user)
        serializer = WatchlistSerializer(watchlists, many=True)
        return Response(serializer.data)

class CreateWatchlist(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        name = request.data.get('name')
        if not name:
            return Response({'error': 'name is required'}, status=400)

        watchlist, created = Watchlist.objects.get_or_create(user=request.user, name_watchlist=name)
        if created:
            return Response({'message': 'Watchlist created'}, status=201)
        return Response({'message': 'Watchlist already exists'}, status=200)

class AddCompanyToWatchlist(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        watchlist_id = request.data.get('watchlist_id')
        company_ids = request.data.get('company_ids', [])

        if not watchlist_id or not isinstance(company_ids, list):
            return Response({'error': 'watchlist_id and list of company_ids required'}, status=400)

        try:
            watchlist = Watchlist.objects.get(id=watchlist_id, user=request.user)
        except Watchlist.DoesNotExist:
            return Response({'error': 'Watchlist not found'}, status=404)

        added = []
        already_exists = []

        for cid in company_ids:
            try:
                company = Company.objects.get(id=cid)
                obj, created = WatchlistItem.objects.get_or_create(watchlist=watchlist, company=company)
                if created:
                    added.append(cid)
                else:
                    already_exists.append(cid)
            except Company.DoesNotExist:
                continue

        return Response({
            "added": added,
            "already_exists": already_exists
        })

class RemoveCompanyFromWatchlist(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        watchlist_id = request.data.get('watchlist_id')
        company_id = request.data.get('company_id')

        if not watchlist_id or not company_id:
            return Response({'error': 'watchlist_id and company_id are required'}, status=400)

        try:
            item = WatchlistItem.objects.get(
                watchlist__id=watchlist_id,
                watchlist__user=request.user,
                company__id=company_id
            )
            item.delete()
            return Response({'message': 'Removed from watchlist'})
        except WatchlistItem.DoesNotExist:
            return Response({'error': 'Item not found in watchlist'}, status=404)
