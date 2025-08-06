from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Company, Watchlist
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
        items = Watchlist.objects.filter(user=request.user)
        serializer = WatchlistSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddToWatchlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        company_id = request.data.get('company_id')
        if not company_id:
            return Response({'error': 'company_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            company = Company.objects.get(id=company_id)
            obj, created = Watchlist.objects.get_or_create(user=request.user, company=company)
            if created:
                return Response({'message': 'Added to watchlist'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Already in watchlist'}, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RemoveFromWatchlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        company_id = request.data.get('company_id')
        if not company_id:
            return Response({'error': 'company_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            company = Company.objects.get(id=company_id)
            deleted = Watchlist.objects.filter(user=request.user, company=company).delete()[0]
            if deleted:
                return Response({'message': 'Removed from watchlist'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Not in watchlist'}, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)