from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, PastDisease, Report


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'email', 'gender', 'age', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user

    def validate(self, data):
        user = User(**data)
        password = data.get('password')

        errors = dict()
        try:
            validate_password(password=password, user=user)
        except ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)


class PastDiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PastDisease
        fields = ['pneumonia', 'diabetes', 'asthma',
                  'hypertension', 'cardiovascular', 'renal_chronic', 'tobacco', 'obesity']


class ReportSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
    message = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = ['id', 'user', 'fever', 'tiredness', 'dry_cough', 'difficulty_in_breathing',
                  'sore_throat', 'pains', 'diarrhea', 'nasal_congestion', 'runny_nose', 'vulnerability_score', 'message', 'severity_level', 'date']
        extra_kwargs = {
            'user': {
                'write_only': True
            }
        }

    def get_message(self, obj):
        return obj.get_message_display()
