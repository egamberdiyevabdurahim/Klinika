from django.urls import path

from .views import TashxisList, TashxisDetail


urlpatterns = [
    path('tashxis/', TashxisList.as_view(), name='tashxis-list'),
    path('tashxis/<int:id>/', TashxisDetail.as_view(), name='tashxis-detail'),
]