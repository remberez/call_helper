from django.urls import path
from users.views.users import RegistrationView, ChangePasswordView, MeView

urlpatterns = [
    path('users/reg/', RegistrationView.as_view(), name='reg'),
    path('users/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('users/me/', MeView.as_view(), name='me'),
]
