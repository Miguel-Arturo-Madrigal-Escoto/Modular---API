#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# flake8: noqa

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modularAPI.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            'available on your PYTHONPATH environment variable? Did you '
            'forget to activate a virtual environment?'
        ) from exc
    execute_from_command_line(sys.argv)

    # NLP Libraries
    import nltk

    nltk.download('stopwords', download_dir='./')
    nltk.download('punkt', download_dir='./')

    # Load fixtures & factories into db
    if len(sys.argv) == 2 and sys.argv[1] == 'migrate':
        execute_from_command_line(['manage.py', 'loaddata', 'initial_roles.json'])
        execute_from_command_line(['manage.py', 'loaddata', 'initial_sectors.json'])

        from authentication.factory import (CompanyFactory, MongoUserFactory,
                                            UserFactory)
        from roles.factory import CompanyRolesFactory

        """users = UserFactory.create_batch(size=10)
        print('Factory installed for User')

        companies = CompanyFactory.create_batch(size=10)
        print('Factory installed for Company')

        CompanyRolesFactory.create_batch(size=10)
        print('Factory installed for Company Roles')

        MongoUserFactory(users, companies)
        print('Factory installed for MongoDB Users')"""


if __name__ == '__main__':
    main()
