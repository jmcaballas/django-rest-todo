from knox import views as knox_views

from django.urls import path

from .views import RegisterView, LoginView

urlpatterns = [
    path('registration', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]
