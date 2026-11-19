from django.urls import path

from .views import AdvisorView, HomeView, PublicationsView, TeamView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("advisor/", AdvisorView.as_view(), name="advisor"),
    path("publications/", PublicationsView.as_view(), name="publications"),
    path("team/", TeamView.as_view(), name="team"),
]
