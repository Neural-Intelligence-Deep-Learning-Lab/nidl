# NIDL — Neural Intelligence & Deep Learning Lab

It's a website for our Lab to share about our research, advisor and current team.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd main
python manage.py runserver
```

## Sync publications

Refresh the publication list and co-author metadata from ORCID and Crossref:

```bash
python backend/manage.py sync_publications
```

The command updates `backend/lab/publications.json`. The publications page reads
that file, so no template changes are needed when the publications change.

