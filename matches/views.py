from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

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

        try:
            match_u = self.get_queryset().get(user_id=user_id, company_id=company_id)
            match_u.user_like = True
            match_u.save()
        except Match.DoesNotExist:
            match_u = Match(user_id=user_id, company_id=company_id, user_like=True)
            match_u.save()

        match_u = self.get_queryset().get(user_id=user_id, company_id=company_id)
        response = {
            'match': True if match_u.user_like and match_u.company_like else False,
            'user': user_id,
            'company': company_id,
        }
        return Response(data=response)

    @action(methods=['POST'], detail=False)
    def match_company(self, request: Request):
        company_id = request.user.company.id
        user_id = request.data.get('user_id', 0)

        try:
            match_c = self.get_queryset().get(user_id=user_id, company_id=company_id)
            match_c.company_like = True
            match_c.save()
        except Match.DoesNotExist:
            match_c = Match(user_id=user_id, company_id=company_id, company_like=True)
            match_c.save()

        match_c = self.get_queryset().get(user_id=user_id, company_id=company_id)
        response = {
            'match': True if match_c.user_like and match_c.company_like else False,
            'user': user_id,
            'company': company_id,
        }
        return Response(data=response)
