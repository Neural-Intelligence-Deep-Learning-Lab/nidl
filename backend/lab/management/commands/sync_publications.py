import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from django.core.management.base import BaseCommand


ORCID_ID = "0000-0002-4631-3446"
DEFAULT_CODE_URL = "https://github.com/Neural-Intelligence-Deep-Learning-Lab/nidl"


class Command(BaseCommand):
    help = "Sync publications from ORCID and Crossref metadata"

    def add_arguments(self, parser):
        parser.add_argument("--orcid", default=ORCID_ID)
        parser.add_argument("--code-url", default=DEFAULT_CODE_URL)

    def handle(self, *args, **options):
        orcid_id = options["orcid"]
        code_url = options["code_url"]
        works = self.fetch_orcid_works(orcid_id)
        publications = []
        seen = set()

        for work in works:
            doi = self.find_doi(work)
            if not doi or doi.lower() in seen:
                continue
            seen.add(doi.lower())

            title = self.work_title(work)
            year = self.work_year(work)
            venue = ""
            authors = ["Muhammad Shadab Alam Hashmi"]

            try:
                doi_url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
                message = self.fetch_json(doi_url)["message"]
                title = message.get("title", [title])[0] or title
                venue = (message.get("container-title") or [""])[0]
                authors = self.crossref_authors(message)
                year = str(message.get("published", {}).get("date-parts", [[year]])[0][0] or year)
            except (KeyError, OSError, ValueError, urllib.error.URLError):
                pass

            if doi.lower().startswith("10.5281/zenodo."):
                try:
                    record_id = doi.rsplit(".", 1)[-1]
                    zenodo = self.fetch_json(f"https://zenodo.org/api/records/{record_id}")
                    zenodo_metadata = zenodo["metadata"]
                    venue = zenodo_metadata.get("journal_title") or zenodo_metadata.get("publisher") or "Zenodo"
                    zenodo_authors = []
                    for creator in zenodo_metadata.get("creators", []):
                        name = creator.get("name", "").strip()
                        zenodo_authors.extend(
                            part.strip() for part in name.split(",") if part.strip()
                        )
                    if zenodo_authors:
                        authors = zenodo_authors
                except (KeyError, OSError, ValueError, urllib.error.URLError):
                    pass

            publications.append({
                "year": year,
                "title": title,
                "venue": venue,
                "authors": authors,
                "read_url": f"https://doi.org/{doi}",
                "code_url": code_url,
            })

        publications.sort(key=lambda item: (int(item["year"]), item["title"].lower()), reverse=True)
        output = Path(__file__).resolve().parents[2] / "publications.json"
        output.write_text(json.dumps(publications, ensure_ascii=False, indent=2) + "\n")
        self.stdout.write(self.style.SUCCESS(f"Synced {len(publications)} publications to {output}"))

    def fetch_orcid_works(self, orcid_id):
        url = f"https://pub.orcid.org/v3.0/{orcid_id}/works"
        request = urllib.request.Request(url, headers={
            "Accept": "application/json",
            "User-Agent": "NIDL publication sync",
        })
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response).get("group", [])

    def fetch_json(self, url):
        request = urllib.request.Request(url, headers={"User-Agent": "NIDL publication sync"})
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)

    def find_doi(self, work):
        summaries = work.get("work-summary") or [{}]
        external_ids = summaries[0].get("external-ids", {}).get("external-id") or []
        for external_id in external_ids:
            if external_id.get("external-id-type", "").lower() == "doi":
                return external_id.get("external-id-value", "").strip()
        return ""

    def work_title(self, work):
        summaries = work.get("work-summary") or [{}]
        return summaries[0].get("title", {}).get("title", {}).get("value", "").replace("&amp;", "&")

    def work_year(self, work):
        summaries = work.get("work-summary") or [{}]
        return summaries[0].get("publication-date", {}).get("year", {}).get("value", "")

    def crossref_authors(self, message):
        authors = []
        for author in message.get("author", []):
            name = " ".join(filter(None, [author.get("given", ""), author.get("family", "")])).strip()
            if name:
                authors.append(name)
        return authors or ["Muhammad Shadab Alam Hashmi"]
