from authentication.models import Company, User
from matches.models import Match


class AlterMatchLikes:
    def __init__(self) -> None:
        pass

    @staticmethod
    def alter_user(user: User):
        Match.objects.filter(user=user).update(user_like=None, company_like=None)

    @staticmethod
    def alter_company(company: Company):
        Match.objects.filter(company=company).update(user_like=None, company_like=None)
