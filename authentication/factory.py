import random

import factory
from django.contrib.auth.hashers import make_password
from faker import Faker

from authentication.constants import LOCATION_CHOICES, MODALITY_CHOICES
from authentication.models import BaseUser, Company, MongoUser, User
from roles.models import Role
from sectors.models import Sector

faker = Faker('es-MX')

class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    about = factory.Faker('sentence', nb_words=20)
    mission = factory.Faker('sentence', nb_words=20)
    vision = factory.Faker('sentence', nb_words=20)
    verified = True
    image = None

    @factory.lazy_attribute
    def location(self):
        return random.choice(LOCATION_CHOICES)[0]

    @factory.lazy_attribute
    def sector(self):
        return Sector.objects.order_by('?')[0]

    @factory.lazy_attribute
    def name(self):
        return faker.unique.company()

    @factory.lazy_attribute
    def base_user(self):
        user = BaseUser(
            username=faker.unique.first_name(),
            email=faker.email(),
            password=make_password('Hola123++'),
            is_active=True,
            is_staff=False,
            is_admin=False,
        )
        user.save()
        return user

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    about = factory.Faker('sentence', nb_words=20)
    image = None

    @factory.lazy_attribute
    def position(self):
        return Role.objects.order_by('?')[0]

    @factory.lazy_attribute
    def expected_salary(self):
        return faker.pyint()

    @factory.lazy_attribute
    def name(self):
        return faker.unique.first_name()

    @factory.lazy_attribute
    def lastname(self):
        return faker.unique.last_name()

    @factory.lazy_attribute
    def modality(self):
        return random.choice(MODALITY_CHOICES)[0]

    @factory.lazy_attribute
    def location(self):
        return random.choice(LOCATION_CHOICES)[0]

    @factory.lazy_attribute
    def base_user(self):
        user = BaseUser(
            username=faker.unique.first_name(),
            email=faker.email(),
            password=make_password('Hola123++'),
            is_active=True,
            is_staff=False,
            is_admin=False,
        )
        user.save()
        return user

class MongoUserFactory:
    def __init__(self, users, companies) -> None:
        self.users = users
        self.companies = companies
        self.run()

    def run(self):
        for user in self.users:
            mongo_user = MongoUser(
                base_user=user.base_user.id,
                name=user.name,
                email=user.base_user.email,
                role='user'
            )
            mongo_user.save()

        for company in self.companies:
            mongo_user = MongoUser(
                base_user=company.base_user.id,
                name=company.name,
                email=company.base_user.email,
                role='company'
            )
            mongo_user.save()
