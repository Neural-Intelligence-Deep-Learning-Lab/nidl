import json
from pathlib import Path

from django.views.generic import TemplateView


def load_publications():
    publications_file = Path(__file__).resolve().parent / "publications.json"
    if not publications_file.exists():
        return []

    publications = json.loads(publications_file.read_text(encoding="utf-8"))
    return sorted(publications, key=lambda item: int(item["year"]), reverse=True)


class HomeView(TemplateView):
    template_name = "lab/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_publications"] = load_publications()[:3]
        return context


class AdvisorView(TemplateView):
    template_name = "lab/advisor.html"


class PublicationsView(TemplateView):
    template_name = "lab/publications.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["publications"] = load_publications()
        context["publication_years"] = sorted(
            {item["year"] for item in context["publications"]},
            reverse=True,
        )
        return context


class TeamView(TemplateView):
    template_name = "lab/team.html"
