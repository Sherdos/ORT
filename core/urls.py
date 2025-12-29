from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("tests/", views.TestListView.as_view(), name="tests"),
    path("tests/<int:pk>/", views.TestDetailView.as_view(), name="test_detail"),
    path("results/", views.ResultsView.as_view(), name="results"),
    path("results/<int:pk>/", views.AttemptDetailView.as_view(), name="attempt_detail"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
]
