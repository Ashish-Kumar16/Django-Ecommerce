from django.urls import path
from .views import RegisterView, login_user, activate_email_account, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_user, name='login'),
    path('activate/<str:uidb64>/<str:token>/', activate_email_account, name='activate'),


    path('logout/', LogoutView.as_view(), name='logout'),
]
