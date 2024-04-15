from django.urls import path
from django.contrib.auth import views as admin_views
from django.contrib.auth.urls import urlpatterns
from django.views.generic import TemplateView


from .views import (
                    RegisterView,
                    ProfileDetailView,
                    ProfileUpdateView,
                    ProfileCreateView,
                    CustomResetPasswordConfirmView,
                    CheckCodeView,
                    )

urlpatterns = [
    # path('send-reset-code/', send_reset_code, name='send_reset_code'),
    path('check-code/', CheckCodeView.as_view(), name='check_code'),

    path('profile/', ProfileDetailView.as_view(), name='profile'),
    path('profile-create/', ProfileCreateView.as_view(), name='profile_create'),
    path('profile-update/<str:pk>/', ProfileUpdateView.as_view(), name='profile_update'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', admin_views.LoginView.as_view(), name='login'),
    path('logout/', admin_views.LogoutView.as_view(), name='logout'),
    path('password-change/', admin_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', admin_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/', CustomResetPasswordConfirmView, name='password_reset_confirm'),
    path('password-reset-done/', admin_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
]