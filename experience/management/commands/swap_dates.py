from django.core.management.base import BaseCommand

from experience.models import Experience


class Command(BaseCommand):
    help = 'Swap start_date and end_date values'

    def handle(self, *args, **options):
        for obj in Experience.objects.all():
            obj.start_date, obj.end_date = obj.end_date, obj.start_date
            obj.save()
