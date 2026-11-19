import json
from pathlib import Path

from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "lab/home.html"


class AdvisorView(TemplateView):
    template_name = "lab/advisor.html"


class PublicationsView(TemplateView):
    template_name = "lab/publications.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        publications_file = Path(__file__).resolve().parent / "publications.json"
        if publications_file.exists():
            context["publications"] = json.loads(publications_file.read_text())
            context["publication_years"] = sorted(
                {item["year"] for item in context["publications"]},
                reverse=True,
            )
        else:
            context["publications"] = []
            context["publication_years"] = []
        return context


class TeamView(TemplateView):
    template_name = "lab/team.html"
