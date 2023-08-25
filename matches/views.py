from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authentication.models import Company, User
from authentication.serializers import CompanySerializer, UserSerializer

from .models import Match
from .serializers import MatchSerializer


# Create your views here.
class MatchViewSet(ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    @action(methods=['POST'], detail=False)
    def match_user(self, request: Request):
        user_id = request.user.user.id
        company_id = request.data.get('company_id', 0)
        like = request.data.get('like', False)

        try:
            match_u = self.get_queryset().get(user_id=user_id, company_id=company_id)
            match_u.user_like = like
            match_u.save()
        except Match.DoesNotExist:
            match_u = Match(user_id=user_id, company_id=company_id, user_like=like)
            match_u.save()

        match_u = self.get_queryset().get(user_id=user_id, company_id=company_id)

        base_user_user = User.objects.get(id=user_id)
        base_user_company = Company.objects.get(id=company_id)

        response = {
            'match': True if match_u.user_like and match_u.company_like else False,
            'user': base_user_user.base_user.id,
            'company': base_user_company.base_user.id,
        }
        return Response(data=response)

    @action(methods=['POST'], detail=False)
    def match_company(self, request: Request):
        company_id = request.user.company.id
        user_id = request.data.get('user_id', 0)
        like = request.data.get('like', True)

        try:
            match_c = self.get_queryset().get(user_id=user_id, company_id=company_id)
            match_c.company_like = like
            match_c.save()
        except Match.DoesNotExist:
            match_c = Match(user_id=user_id, company_id=company_id, company_like=like)
            match_c.save()

        match_c = self.get_queryset().get(user_id=user_id, company_id=company_id)

        base_user_user = User.objects.get(id=user_id)
        base_user_company = Company.objects.get(id=company_id)

        response = {
            'match': True if match_c.user_like and match_c.company_like else False,
            'user': base_user_user.base_user.id,
            'company': base_user_company.base_user.id,
        }
        return Response(data=response)

    @action(methods=['GET'], detail=False)
    def get_user_match(self, request: Request):
        companies = Company.objects.order_by('?')[0]
        company_serializer = CompanySerializer(instance=companies)
        return Response(company_serializer.data)

    @action(methods=['GET'], detail=False)
    def get_company_match(self, request: Request):
        users = User.objects.order_by('?')[0]
        user_serializer = UserSerializer(instance=users)
        return Response(user_serializer.data)

    @action(methods=['GET'], detail=False)
    def retrieve_company_matches(self, request: Request):
        """Retrieves the matches of the company (base_user user ids)"""
        try:
            company_id = request.user.company.id
            matched_user_ids = self.get_queryset().filter(
                company_id=company_id,
                company_like=True,
                user_like=True).values_list('user_id', flat=True)
            matched_users = User.objects.filter(
                id__in=matched_user_ids).values_list('base_user', flat=True)
            response = {
                'matches': list(matched_users)
            }
            return Response(response)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False)
    def retrieve_user_matches(self, request: Request):
        """Retrieves the matches of the user (base_user company ids)"""
        try:
            user_id = request.user.user.id
            matched_company_ids = self.get_queryset().filter(
                user_id=user_id,
                company_like=True,
                user_like=True).values_list('company_id', flat=True)
            matched_companies = Company.objects.filter(
                id__in=matched_company_ids).values_list('base_user', flat=True)
            response = {
                'matches': list(matched_companies)
            }
            return Response(response)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
