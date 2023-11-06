import requests
from django.db.models import Q

from authentication.models import Company, User
from matches.models import Match


class AlterMatchLikes:
    def __init__(self) -> None:
        pass

    @staticmethod
    def alter_user(user: User):
        """
            Remove the dislike from the company if my role is 'user'.
        """
        Match.objects.filter(Q(company_like=False) | Q(company_like__isnull=True), user=user).update(company_like=None)

    @staticmethod
    def alter_company(company: Company):
        """
            Remove the dislike from the user if my role is 'company'.
        """
        Match.objects.filter(Q(user_like=False) | Q(user_like__isnull=True), company=company).update(user_like=None)


def download_image(url, local_filename = './form/downloaded_pic.jpg'):
    response = requests.get(url, stream=True)
    with open(local_filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
