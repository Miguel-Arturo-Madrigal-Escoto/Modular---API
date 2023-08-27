import random

import factory
from faker import Faker
from translate import Translator

from authentication.models import Company
from roles.models import CompanyRoles, Role

from .factory_data import medicine_words, software_words

faker = Faker('es-MX')

class CompanyRolesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CompanyRoles

    @factory.lazy_attribute
    def name(self):
        return faker.unique.job()[:35]

    @factory.lazy_attribute
    def description(self):
        # Todo: generar descripcion logica
        word_type = random.choice(['medicine', 'software'])
        translator = Translator(to_lang='es')

        if word_type == 'medicine':
            desc = random.choices(medicine_words, k=30)
            string = ' '.join(k for k in desc)
            return translator.translate(string)
        else:
            desc = random.choices(software_words, k=30)
            string = ' '.join(k for k in desc)
            return translator.translate(string)

    @factory.lazy_attribute
    def link(self):
        return faker.url()

    @factory.lazy_attribute
    def role(self):
        return Role.objects.order_by('?')[0]

    @factory.lazy_attribute
    def company(self):
        return Company.objects.order_by('?')[0]
