from django.urls import path

from .views import TashxisList, TashxisDetail


urlpatterns = [
    path('tashxis/', TashxisList.as_view(), name='tashxis-list'),
    path('tashxis/<int:pk>/', TashxisDetail.as_view(), name='tashxis-detail'),
]