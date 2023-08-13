from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Experience


class ExperienceSerializer(ModelSerializer):

    class Meta:
        model = Experience
        fields = '__all__'

    def validate(self, model_fields):
        if model_fields.get('start_date') >= model_fields.get('end_date'):
            raise ValidationError({
                'start_date': 'The start date must be less than the end date'
            })
        return model_fields
