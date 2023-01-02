from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Views
from .views import CheckVulnerability, UserView, UserRegisterView, PastDiseaseView, ReportViewSet


router = DefaultRouter()
router.register('', ReportViewSet, basename="report")


urlpatterns = [
    path('user/', UserView.as_view(), name="user"),
    path('check-vulnerability/', CheckVulnerability.as_view(), name="check"),
    path('user/register/', UserRegisterView.as_view(), name="user-register"),
    path('user/past-disease/', PastDiseaseView.as_view(), name="past-disease"),
    path('user/reports/', include(router.urls)),
]
