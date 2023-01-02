from cProfile import run
from math import floor, ceil
from django.shortcuts import render
import pickle

# Rest Framework
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Models
from .models import PastDisease, User, Report

# Serializer
from .serializers import UserSerializer, PastDiseaseSerializer, ReportSerializer

# Create your views here.


class UserView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        id = request.user.id
        user = User.objects.get(pk=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserRegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(pk=serializer.data['id'])
        PastDisease(user=user).save()
        return Response(serializer.data)


class PastDiseaseView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        serializer = PastDiseaseSerializer(user.past_disease)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        id = request.user.id
        user = User.objects.get(pk=id)

        for key, value in data.items():
            if hasattr(user.past_disease, key):
                setattr(user.past_disease, key, value)
        user.past_disease.save()

        serializer = PastDiseaseSerializer(user.past_disease)
        return Response(serializer.data)


class ReportViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ReportSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return Report.objects.filter(user=user_id)

    # def get(self, request):
    #     id = request.user.id
    #     user = User.objects.get(pk=id)
    #     reports = user.reports.all()
    #     serializer = ReportSerializer(reports, many=True)
    #     return serializer.data


class CheckVulnerability(APIView):
    permission_classes = [IsAuthenticated, ]

    def get_past_disease_data(self, user: User):
        pd_obj = user.past_disease
        past_disease = []

        # Past Disease
        past_disease.append(1 if pd_obj.pneumonia else 0)
        past_disease.append(1 if pd_obj.diabetes else 0)
        past_disease.append(1 if pd_obj.asthma else 0)
        past_disease.append(1 if pd_obj.hypertension else 0)
        past_disease.append(1 if pd_obj.cardiovascular else 0)
        past_disease.append(1 if pd_obj.renal_chronic else 0)
        past_disease.append(1 if pd_obj.tobacco else 0)
        past_disease.append(1 if pd_obj.obesity else 0)

        # Age
        past_disease.append(1 if user.age in range(0, 10) else 0)
        past_disease.append(1 if user.age in range(10, 20) else 0)
        past_disease.append(1 if user.age in range(20, 25) else 0)
        past_disease.append(1 if user.age in range(25, 60) else 0)
        past_disease.append(1 if user.age > 60 else 0)

        # Gender
        past_disease.append(1 if user.gender == 'F' else 0)
        past_disease.append(1 if user.gender == 'M' else 0)

        past_disease = tuple(past_disease)
        return past_disease

    def get_common_symptoms_data(self, data, user):
        common_symptoms = []

        common_symptoms.append(1 if data['fever'] else 0)
        common_symptoms.append(1 if data['tiredness'] else 0)
        common_symptoms.append(1 if data['dry_cough'] else 0)
        common_symptoms.append(1 if data['difficulty_in_breathing'] else 0)
        common_symptoms.append(1 if data['sore_throat'] else 0)
        common_symptoms.append(1)
        common_symptoms.append(1 if data['pains'] else 0)
        common_symptoms.append(1 if data['diarrhea'] else 0)

        common_symptoms.append(1 if user.age in range(0, 10) else 0)
        common_symptoms.append(1 if user.age in range(10, 20) else 0)
        common_symptoms.append(1 if user.age in range(20, 25) else 0)
        common_symptoms.append(1 if user.age in range(25, 60) else 0)
        common_symptoms.append(1 if user.age > 60 else 0)

        # Gender
        common_symptoms.append(1 if user.gender == 'F' else 0)
        common_symptoms.append(1 if user.gender == 'M' else 0)
        common_symptoms.append(1 if user.gender == 'O' else 0)

        common_symptoms = tuple(common_symptoms)
        return common_symptoms

    def generate_report(self, user, final_score, data):
        report = Report(user=user, vulnerability_score=final_score, fever=data['fever'],
                        tiredness=data['tiredness'], dry_cough=data['dry_cough'],
                        difficulty_in_breathing=data['difficulty_in_breathing'],
                        sore_throat=data["sore_throat"], pains=data['pains'], diarrhea=data['diarrhea'], nasal_congestion=True,
                        runny_nose=True, message="NONE", severity_level=0)

        if final_score in range(0, 4):
            report.__setattr__('severity_level', 0)
            report.__setattr__('message', "NONE")
        elif final_score in range(4, 6):
            report.__setattr__('severity_level', 1)
            report.__setattr__('message', "MILD")
        elif final_score in range(5, 8):
            report.__setattr__('severity_level', 2)
            report.__setattr__('message', "MODERATE")
        else:
            report.__setattr__('severity_level', 3)
            report.__setattr__('message', "SEVERE")

        report.save()
        return report

    def post(self, request):
        data = request.data
        id = request.user.id
        user = User.objects.get(pk=id)

        models = pickle.load(open('core/models.pkl', 'rb'))
        past_disease_model, common_symptoms_model = models[
            'past_disease_model'], models['common_disease_model']

        past_disease_data = self.get_past_disease_data(user)
        common_symptom_data = self.get_common_symptoms_data(data, user)

        print(past_disease_data)
        print(common_symptom_data)

        pd_score = past_disease_model.predict([past_disease_data])
        cs_score = common_symptoms_model.predict([common_symptom_data])

        final_score = ceil((pd_score * 3 / 3) + (cs_score * 7 / 3))
        final_score = 10 if final_score > 10 else final_score

        report = self.generate_report(user, final_score, data)
        return Response(ReportSerializer(report).data)
