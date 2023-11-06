import ast
import random

import numpy as np
import pandas as pd
from cloudinary.uploader import upload
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from unidecode import unidecode

from authentication.constants import LOCATION_CHOICES, MODALITY_CHOICES
from authentication.models import BaseUser, Company, User
from experience.models import Experience
from matches.utilities import download_image
from roles.models import CompanyRoles, Role
from sectors.models import Sector
from skills.models import Skill


# Create your views here.
class FormViewSet(ViewSet):
    """
    This viewset purpose is to retrieve the form data
    that should be rendered in the UI.
    """
    permission_classes = (IsAuthenticated, )

    def list(self, request: Request):
        form_data = {
            'modalities': self.parse_constant(MODALITY_CHOICES),
            'locations': self.parse_constant(LOCATION_CHOICES),
            'positions': self.get_roles(),
            'sectors': self.get_sectors()
        }
        return Response(form_data, status=200)

    def parse_constant(self, constant):
        form_data = []
        for idx, value in enumerate(constant):
            form_data.append({
                'value': value[0],
                'display': value[1],
                'id': idx + 1
            })
        return form_data

    def get_roles(self):
        try:
            response = []
            roles = Role.objects.all()
            for role in roles:
                response.append({
                    'value': role.position,
                    'display': f'{ role.position }'.capitalize(),
                    'id': role.pk
                })
            return response
        except Exception:
            return []

    def get_sectors(self):
        try:
            response = []
            sectors = Sector.objects.all()
            for sector in sectors:
                response.append({
                    'value': sector.name,
                    'display': f'{ sector.name }'.capitalize(),
                    'id': sector.pk
                })
            return response
        except Exception:
            return []


class UserSeedViewSet(ViewSet):
    """
        Seeds the database with users and their images.
    """
    def list(self, request: Request):
        # Type example: administrador_profiles, musico_profiles, etc
        # Role: the id of the role to be seeded
        type = request.query_params.get('type')
        role = request.query_params.get('role')

        try:
            users_df = pd.read_csv(f'./form/users/{type}/{type}.csv')

            users_df['experiences'] = users_df['experiences'].apply(ast.literal_eval)


            for index, row in users_df.iterrows():
                name = row['name']
                about = row['about']
                salary = row['salary']
                location = row['location']
                experiences = row['experiences'][0]
                skills = row['skills'].replace(', ', ',').split(',')

                try:
                    bu = BaseUser(
                        username=f'{name}{ random.randint(1, 10000) }' ,
                        email=unidecode(name.replace(' ', '').lower()) + f'{random.randint(1, 10000)}' + random.choice(['@gmail.com', '@outlook.com', '@hotmail.com']),
                        password=make_password('Hola123++')
                    )
                    bu.save()

                    url = None
                    with open(f'./form/users/{type}/{index+1}.jpg', 'rb') as image_file:
                        result = upload(image_file)
                        url = result['url']

                    upload_index = url.find('image/upload/')

                    user = User(
                        name=name.split(' ')[0],
                        lastname=name.split(' ')[1],
                        expected_salary=salary,
                        modality=random.choice(['presencial', 'remoto', 'hibrido']),
                        location=location,
                        about=about,
                        base_user_id=bu.id,
                        image=url[upload_index:],
                        position_id=role
                    )
                    user.save()

                    exp = Experience(
                        start_date=experiences[-2],
                        end_date=experiences[-1],
                        description=f'{experiences[0]} - {experiences[-3]}. {experiences[1]}',
                        role_id=role,
                        user_id=user.id
                    )
                    exp.save()

                    skill_name = skills[0]
                    skill_description = skills[1:]
                    skill_description = ', '.join(k for k in skill_description).strip().capitalize()
                    s = Skill(
                        name=skill_name,
                        description=skill_description,
                        user_id=user.id
                    )
                    s.save()
                except:
                    pass
            return Response({ 'ok': 'db seeded' })

        except Exception as e:
            return Response({ 'ok': f'{e}' })


class CompanySeedViewSet(ViewSet):
    """
        Seeds the database with companies and their images.
    """
    def list(self, request: Request):
        # Type example: scraped_administrador, scraped_qa_tester, etc
        # Role: the id of the role to be seeded
        type = request.query_params.get('type')
        sector = request.query_params.get('sector')
        role = request.query_params.get('role')
        try:
            companies_df = pd.read_csv(f'./form/companies/{type}.csv')

            print(companies_df.head())

            for index, row in companies_df.iterrows():
                job_link = row['Job link']
                company_name = row['Company name']
                company_location = row['Company Location']
                company_about = row['Company About']
                job_name = row['Job name']
                job_desc = row['Job Offer Desc']
                company_logo = row['Company logo']

                print('job_name: ', job_name)

                company = None

                # save the base user and company
                try:
                    company = Company.objects.get(name=company_name)
                except Company.DoesNotExist:
                    bu = BaseUser(
                        username=f'{company_name}'[:50] ,
                        email=unidecode(company_name.replace(' ', '').lower()) + f'{random.randint(1, 10000)}' + random.choice(['@gmail.com', '@outlook.com', '@hotmail.com']),
                        password=make_password('Hola123++')
                    )
                    bu.save()

                    download_image(company_logo)

                    url = None
                    with open(f'./form/downloaded_pic.jpg', 'rb') as image_file:
                        result = upload(image_file)
                        url = result['url']
                    upload_index = url.find('image/upload/')

                    company = Company(
                        name=company_name,
                        about=company_about,
                        mission=company_about,
                        vision=company_about,
                        verified=True,
                        location=company_location,
                        image=url[upload_index:],
                        base_user_id=bu.id,
                        sector_id=sector
                    )
                    company.save()

                # save the job
                cr = CompanyRoles(
                    name=job_name,
                    description=job_desc,
                    link=job_link,
                    company_id=company.id,
                    role_id=role
                )
                cr.save()

            return Response({ 'ok': 'db seeded' })
        except Exception as e:
            return Response({ 'ok': f'{e}' })
