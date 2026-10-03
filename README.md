# OmniExtract: Enterprise Web Scraping & Data Extraction Platform

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Framework](https://img.shields.io/badge/Framework-FastAPI%20%7C%20Selenium%20%7C%20Playwright-orange.svg)](#architecture)
[![Status](https://img.shields.io/badge/Production-Ready-brightgreen.svg)](#features)

OmniExtract is a production-grade automated web extraction and intelligence platform designed to handle complex, dynamic Single-Page Applications (SPAs) and dynamic B2B directories. It features resilient headless browser automation, facet taxonomy reconstruction, automated data cleansing, schema normalization, and an interactive real-time presentation dashboard.

---

## 🌟 Key Capabilities

- **Dynamic SPA Scraping:** Automated navigation, cookie and overlay bypass, lazy-loading synchronization, and multi-page pagination.
- **REST & Facet Taxonomy Parsing:** Direct interrogation of internal facet engines (`search46json.jsp`) for taxonomy mapping and categorical reconciliation.
- **Automated Data Sanitization:** Rigorous entity validation, zero-null constraints, whitespace normalization, and multi-field deduplication.
- **Real-Time Analytics Dashboard:** FastAPI and modern Vanilla CSS/JS glassmorphic dashboard with live KPI counters and query filtering.
- **Unified Datasets:** Dual-target structured datasets exported to standardized `.csv` and `.json` deliverables.

---

## 🧭 Repository Architecture

```
├── disney_cruise/                  # Maritime travel extraction pipeline
│   ├── disney_scraper.py           # Multi-region dynamic scraper with pagination
│   ├── disney_analysis.py          # Itinerary metrics calculation & analytics engine
│   ├── results_disney.csv          # Cleaned 14-column itinerary dataset
│   └── disney_answers.json         # Computed metric outputs
│
├── ingredients_network/            # Global B2B supplier extraction pipeline
│   ├── ingredients_scraper.py      # Supplier facet filtering and profile scraper
│   ├── ingredients_analysis.py     # Taxonomy aggregation and company analytics
│   ├── results_ingredients.csv     # Cleaned 10-column company profile dataset
│   └── ingredients_answers.json    # Computed taxonomy & facet metrics
│
├── bonus_webapp/                   # Live telemetry & presentation dashboard
│   └── app.py                      # FastAPI modern dark-mode glassmorphic application
│
├── results.csv                     # Consolidated, sanitized dataset
├── requirements.txt                # Unified dependency manifest
└── README.md                       # Platform documentation
```

---

## 🚢 Module 1: Disney Cruise Line Pipeline

- **Target:** Dynamic Angular SPA travel portal (`disneycruise.disney.go.com`)
- **Key Pipeline Steps:**
  1. **Automated Navigation & Consent Handling:** Programmatically bypasses regional modal dialogues and cookie consents.
  2. **Interactive Search Interaction:** Triggers the itinerary finder via the `View dates` button.
  3. **Hydration Awaiting:** Implements explicit wait conditions for DOM card stabilization.
  4. **Continuous Pagination:** Implements stepped incremental scrolling (`window.scrollBy(0, 800)`) and multi-region fleet itinerary aggregation.
  5. **Data Cleansing Rules:** Strict deduplication on `(Title, Departing From, Duration)`, guarantees non-empty departure ports and ports of call.
  6. **Export Schema:** 14 normalized attributes including cabin category pricing (Inside, Oceanview, Balcony, Suite) and booking URLs.

### Executing the Maritime Pipeline
```bash
python disney_cruise/disney_scraper.py
python disney_cruise/disney_analysis.py
```

---

## 🌿 Module 2: Ingredients Network Pipeline

- **Target:** Global supplier marketplace (`ingredientsnetwork.com`)
- **Key Pipeline Steps:**
  1. **Direct Search Activation:** Navigates search index and programmatically activates the `Suppliers` facet.
  2. **Product Record Filtration:** Eliminates standalone catalog products to preserve pure company entities.
  3. **Taxonomy Interrogation:** Queries internal facet trees to extract full category structures across ingredients, finished products, and delivery formats.
  4. **Mandatory Schema Compliance:** Validates 10 non-empty fields:
     - `Company Name`, `Company Description`, `Sales Markets`, `Primary Business Activity`, `Categories`, `Events`, `Address`, `Email`, `Telephone`, `Website`.
  5. **Deduplication & Cleansing:** Normalizes addresses, sanitizes corporate contact emails/phones, and exports to CSV.

### Executing the Supplier Pipeline
```bash
python ingredients_network/ingredients_scraper.py
python ingredients_network/ingredients_analysis.py
```

---

## 🖥️ Module 3: Live Analytics Dashboard

OmniExtract includes a lightweight, full-stack visualization engine built on **FastAPI** with a **Glassmorphic Dark UI**:
- **Zero Frontend Dependencies:** Built with Vanilla HTML5, modern CSS3 variables, and native ES6 JavaScript.
- **Dynamic KPI Aggregations:** Computes real-time inventory counts, category breakdown statistics, and fleet distributions directly from loaded datasets.
- **Dual-Tab Entity Browser:** Seamless switching between maritime cruise packages and global ingredient suppliers.

### Launching the Dashboard
```bash
python bonus_webapp/app.py
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser.

---

## 🛠️ Quickstart & Installation

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/<YOUR_USERNAME>/omniextract-data-pipeline.git
cd omniextract-data-pipeline

# Create virtual environment (optional)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 📊 Analytics & Metric Summary

### Maritime Itinerary Metrics
- **Pacific Coast / Alaska Itineraries:** `3`
- **Total Deduplicated Fleet Packages:** `10`
- **Special Holiday Sailings:** `2`
- **Itineraries Offering > 2 Booking Dates:** `10`
- **Major Hub Departures (Miami & London Southampton):** `3`

### Global Supplier & Taxonomy Metrics
- **Total Ingredients Catalog Facets:** `552`
- **Total Finished Products Catalog Facets:** `33`
- **Herbs & Spices Suppliers:** `3`
- **Physical Delivery Format Manufacturers:** `5`
- **Cognitive & Mental Health Formulators:** `5`

---

## 📄 License
This project is licensed under the MIT License.
