from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authentication.models import Company, User
from authentication.serializers import CompanySerializer, UserSerializer
from experience.models import Experience
from roles.models import CompanyRoles
from skills.models import Skill

from .algorithms.nlp import NlpAlgorithm
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
        string_to_match = ''
        string_to_match += f'{ request.user.user.position.position } '
        string_to_match += f'{ request.user.user.expected_salary } '
        string_to_match += f'{ request.user.user.modality } '
        string_to_match += f'{ request.user.user.location } '
        string_to_match += f'{ request.user.user.about } '

        experiences = Experience.objects.filter(user_id=request.user.user.id)
        for experience in experiences:
            string_to_match += f'{ experience.description } '
            string_to_match += f'{ experience.role.position } '

        skills = Skill.objects.filter(user_id=request.user.user.id)
        for skill in skills:
            string_to_match += f'{ skill.name } '
            string_to_match += f'{ skill.description } '

        nlp = NlpAlgorithm()
        nlp.df_company(request.user.user, string_to_match)
        nlp.df_company_roles()

        companies = Company.objects.order_by('?')[0]
        company_serializer = CompanySerializer(instance=companies)
        return Response(company_serializer.data)

    @action(methods=['GET'], detail=False)
    def get_company_match(self, request: Request):
        string_to_match = ''
        string_to_match += f'{ request.user.company.about } '
        string_to_match += f'{ request.user.company.mission } '
        string_to_match += f'{ request.user.company.vision } '
        string_to_match += f'{ request.user.company.location } '
        string_to_match += f'{ request.user.company.sector.name } '

        roles = CompanyRoles.objects.filter(company_id=request.user.company.id)

        for rol in roles:
            string_to_match += f'{ rol.name } '
            string_to_match += f'{ rol.description } '
            string_to_match += f'{ rol.role.position } '

        users = User.objects.order_by('?')[0]
        user_serializer = UserSerializer(instance=users)
        return Response(user_serializer.data)

    @action(methods=['GET'], detail=False)
    def retrieve_user_matches_list(self, request: Request):
        try:
            user_id = request.user.user.id
            matched_companies = self.get_queryset().filter(
                user_id=user_id,
                user_like=True,
                company_like=True
            ).values_list('company_id', flat=True)
            companies = Company.objects.filter(id__in=matched_companies)
            company_serializer = CompanySerializer(companies, many=True)
            return Response(company_serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False)
    def retrieve_company_matches_list(self, request: Request):
        try:
            company_id = request.user.company.id
            matched_users = self.get_queryset().filter(
                company_id=company_id,
                user_like=True,
                company_like=True
            ).values_list('user_id', flat=True)
            users = User.objects.filter(id__in=matched_users)
            user_serializer = UserSerializer(users, many=True)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
