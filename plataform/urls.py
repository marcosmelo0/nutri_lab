from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from . import views


urlpatterns = [
    path('patients/', views.patient, name="patient"),
    path('patient-data-list/', views.patient_data_list, name="patient_data_list"),
    path('patient-data/<str:id>/', views.patient_data, name="patient-data"),
    path('chart-weight/<str:id>/', views.chart_weight, name="chart-weight"),
    path('meal-plan-list/', views.meal_plan_list, name="meal-plan-list"),
    path('meal-plan/<str:id>/', views.meal_plan, name="meal-plan"),
    path('snack/<str:id_patient>/', views.snack, name="snack"),
    path('option/<str:id_patient>/', views.option, name="option"),
    path('', RedirectView.as_view(url='patients/', permanent=False)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
