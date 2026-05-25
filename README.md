# Breathe ESG - Data Normalization & Review Pipeline

This repository contains the full-stack prototype for the Breathe ESG Tech Intern Assignment. It ingests messy emissions data from three distinct sources (SAP, Utility Portals, Corporate Travel APIs), normalizes the units and timeframes, and surfaces the records in a React dashboard for analyst review.

## Live Deployment
* **Frontend Dashboard:** [Insert your deployed React URL here]
* **Backend API:** [Insert your deployed Django URL here]

## Required Documentation
The architectural decisions, data models, and tradeoffs are documented in the following files as requested:
* [`MODEL.md`](./MODEL.md) - Database schema, multi-tenancy, and audit trail logic.
* [`SOURCES.md`](./SOURCES.md) - Research on real-world data shapes and sample data justifications.
* [`DECISIONS.md`](./DECISIONS.md) - Ambiguities resolved and subsets handled.
* [`TRADEOFFS.md`](./TRADEOFFS.md) - Deliberate scoping choices and omissions.

## Tech Stack
* **Backend:** Django, Django REST Framework, Python 3
* **Frontend:** React, Vite, Axios
* **Database:** SQLite (for rapid prototyping)

## Local Setup (If running locally)

### 1. Backend (Django)
```bash
cd esg_backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate