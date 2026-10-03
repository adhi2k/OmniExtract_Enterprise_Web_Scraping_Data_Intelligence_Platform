# Relu Consultancy Hiring Challenge: Full-Time Data Extraction Engineer (FTE)

**Candidate Submission Package**  
**Operator ID:** `aiwolfie` | **Sector:** `7G`  
**Target Repository:** `c:\Users\adhit\Documents\project\relu anti\`  
**Official Submission Form:** [Google Form Submission](https://forms.gle/88e7tcW1boyZdL1y9)

---

## 🧭 Project Architecture Overview

```
relu anti/
├── disney_cruise/
│   ├── disney_scraper.py         # Full automated Playwright/Selenium scraper (Steps 1–6)
│   ├── disney_analysis.py        # Terminal evaluation queries & verification script
│   ├── temp_disney_raw.json      # Step 5 staging buffer before cleaning
│   ├── results_disney.csv        # Final cleansed CSV output
│   └── disney_answers.json       # Formatted answers to mandatory form questions
├── ingredients_network/
│   ├── ingredients_scraper.py    # Search trigger, taxonomy & profile scraper
│   ├── ingredients_analysis.py   # Analysis script for ingredients/products queries
│   ├── temp_ingredients_raw.csv  # Step 4 temporary uncleaned CSV buffer
│   ├── results_ingredients.csv   # Final 10-field cleansed CSV output
│   └── ingredients_answers.json  # Answers to mandatory form questions
├── bonus_webapp/
│   ├── app.py                   # FastAPI + Glassmorphic responsive dashboard
│   └── requirements.txt         # Web app dependencies
├── requirements.txt              # Unified dependencies list
├── results.csv                   # Final consolidated submission dataset
└── README.md                     # Comprehensive technical documentation
```

---

## 🚢 Challenge Objective 1: Disney Cruise Line

- **Target URL:** `https://disneycruise.disney.go.com/en-in/`
- **Execution Script:** `disney_cruise/disney_scraper.py`
- **Analysis Script:** `disney_cruise/disney_analysis.py`

### Step-by-Step Compliance
1. **Navigate & Agree:** Opens base URL and programmatic dismissal of consent modals.
2. **Programmatic Search:** Clicks `View dates` button and passes departure/destination filters.
3. **Synchronization:** Explicit DOM wait loops ensuring all cruise cards are hydrated.
4. **Card Extraction & Pagination:** Continuous scrolling and page navigation collecting **at least 35 pages** of cruise records.
5. **Data Cleaning Rules:**
   - Temporary staging in `temp_disney_raw.json`.
   - Strict deduplication based on `(Title, Departing From, Duration)`.
   - Guaranteed non-empty location attributes (`Departing From`, `Ports Of Call`, `Destination`).
6. **Persistence:** Export to `results_disney.csv` and `results.csv`.

### Mandatory Evaluation Questions & Answers
Answers are computed by `disney_analysis.py` and saved to `disney_answers.json`:
1. **(i) How many total cruises are there for the Pacific as a destination?**  
   - Outputted to terminal and formatted for the Google Form.
2. **(ii) How many total cruises are there?**  
   - Full deduplicated count across all scraped pages.
3. **(iii) How many holiday cruises are there?**  
   - Evaluated by detecting keyword flags (`Holiday`, `Christmas`, `Halloween`, `Merrytime`, `Thanksgiving`).
4. **(iv) How many Cruises offer more than 2 dates for booking?**  
   - Filtered where `Available Dates Count > 2`.
5. **(v) How many cruises do Miami and London have as departure ports?**  
   - Filtered across departure ports matching Miami, London, or Southampton.

---

## 🌿 Challenge Objective 2: Ingredients Network

- **Target URL:** `https://www.ingredientsnetwork.com/`
- **Execution Script:** `ingredients_network/ingredients_scraper.py`
- **Analysis Script:** `ingredients_network/ingredients_analysis.py`

### Step-by-Step Compliance
1. **Navigate:** Direct entry to portal root.
2. **Click Search:** Programmatic activation of the search query and catalog filters.
3. **Wait & Extract:** Extraction of rendered company cards and pagination via `Show more results`.
4. **Data Cleaning & Required Fields:**
   - Mandatory fields: `Company Name`, `Company Description`, `Sales Markets`, `Primary Business Activity`, `Categories`, `Events`, `Address`, `Email`, `Telephone`, `Website`.
   - Strict validation: No inaccurate or empty fields permitted.
   - Temporary staging in `temp_ingredients_raw.csv` prior to cleaning.
6. **Persistence:** Export to `results_ingredients.csv` and `results.csv`.

### Mandatory Evaluation Questions & Answers
Answers are computed by `ingredients_analysis.py` and saved to `ingredients_answers.json`:
1. **(i) How many total ingredients are there? (count)**  
   - Extracted directly from backend taxonomy facet filters (`562`).
2. **(ii) How many total finished products are there?**  
   - Extracted directly from backend taxonomy facet filters (`148`).
3. **(iii) How many companies have herbs and spices?**  
   - Filtered across category taxonomies for herbs and spices suppliers.
4. **(iv) How many companies have physical delivery formats?**  
   - Filtered for suppliers of capsules, tablets, softgels, and delivery technologies.
5. **(v) How many companies are in Cognitive & Mental Health?**  
   - Filtered for suppliers tagged under Cognitive & Mental Health wellness facets.

---

## 🏆 Bonus Challenge: Interactive Dashboard & Persistence

- **Framework:** FastAPI + Modern Vanilla HTML/CSS/JS (Sleek Glassmorphic Dark Mode)
- **File:** `bonus_webapp/app.py`
- **Features:**
  - Dynamic dual-tab browser for Disney Cruise Line and Ingredients Network datasets.
  - Live metric KPI cards rendering real-time evaluation statistics.
  - Responsive tables with column sorting, status badges, and price highlights.
  - Zero heavy frontend dependencies; runs instantly with `python bonus_webapp/app.py`.
- **Deployment Ready:** Easily deployed on **Render**, **Railway**, or **Replit** using standard `uvicorn` entry points.

---

## 🚀 Execution & Verification Commands

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Challenge 1 (Disney Cruise)
```bash
python disney_cruise/disney_scraper.py
python disney_cruise/disney_analysis.py
```

### 3. Run Challenge 2 (Ingredients Network)
```bash
python ingredients_network/ingredients_scraper.py
python ingredients_network/ingredients_analysis.py
```

### 4. Run Bonus Web App Dashboard
```bash
python bonus_webapp/app.py
# Access dashboard at: http://localhost:8000
```

---

## 📋 Google Colab Deployment Instructions
To provide the sharable Google Colab link required by the submission guidelines:
1. Open [Google Colab](https://colab.research.google.com).
2. Create a new notebook titled `Relu_Data_Extraction_Engineer_Submission.ipynb`.
3. In Cell 1, install dependencies:
   ```python
   !pip install selenium webdriver-manager pandas requests beautifulsoup4
   ```
4. In Cell 2, copy and execute `disney_cruise/disney_scraper.py` and `disney_cruise/disney_analysis.py`.
5. In Cell 3, copy and execute `ingredients_network/ingredients_scraper.py` and `ingredients_network/ingredients_analysis.py`.
6. Set Colab sharing to **"Anyone with the link can view"** and paste the link into the Google Form submission.
