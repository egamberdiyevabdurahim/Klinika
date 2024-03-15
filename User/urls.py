from django.urls import path

from .views import ChangePasswordView, Userdetail, SignUp, BemorList, BemorDetail


urlpatterns = [
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('user-detail/<int:id>/', Userdetail.as_view(), name='user-detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('bemor-list/', BemorList.as_view(), name='bemor-list'),
    path('bemor-detail/<int:id>/', BemorDetail.as_view(), name='bemor-detail'),
]
