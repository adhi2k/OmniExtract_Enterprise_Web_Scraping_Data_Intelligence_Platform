"""
Relu Consultancy Hiring Challenge - Bonus Track Dashboard
Dynamic Full-Stack Persistence & Presentation Engine
Framework: FastAPI + Modern Dark Glassmorphic UI
Author: Autonomous Data Extraction Engineer | Operator: aiwolfie
"""

import os
import json
import pandas as pd
from typing import Optional, Dict, Any
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="Relu Data Extraction Live Dashboard", version="2.0.0")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DISNEY_CSV = os.path.join(BASE_DIR, "disney_cruise", "results_disney.csv")
if not os.path.exists(DISNEY_CSV):
    DISNEY_CSV = os.path.join(BASE_DIR, "results_disney.csv")

INGREDIENTS_CSV = os.path.join(BASE_DIR, "ingredients_network", "results_ingredients.csv")
if not os.path.exists(INGREDIENTS_CSV):
    INGREDIENTS_CSV = os.path.join(BASE_DIR, "results_ingredients.csv")

DISNEY_ANSWERS_JSON = os.path.join(BASE_DIR, "disney_answers.json")
INGREDIENTS_ANSWERS_JSON = os.path.join(BASE_DIR, "ingredients_answers.json")


def load_disney_df() -> pd.DataFrame:
    if os.path.exists(DISNEY_CSV):
        df = pd.read_csv(DISNEY_CSV).fillna("")
        return df
    return pd.DataFrame()


def load_ingredients_df() -> pd.DataFrame:
    if os.path.exists(INGREDIENTS_CSV):
        df = pd.read_csv(INGREDIENTS_CSV).fillna("")
        # Strictly filter out non-company rows like 'PRODUCT'
        if "Company Name" in df.columns:
            df = df[~df["Company Name"].str.upper().isin(["PRODUCT", "COMPANY", "NAN", ""])]
        return df
    return pd.DataFrame()


def get_live_metrics() -> Dict[str, Any]:
    disney_df = load_disney_df()
    ingr_df = load_ingredients_df()

    # Disney Metrics
    total_disney = len(disney_df)
    pacific_count = 0
    holiday_count = 0
    dates_gt_2 = 0
    miami_london = 0

    if not disney_df.empty:
        pacific_mask = (
            disney_df["Title"].astype(str).str.contains("Pacific", case=False, na=False) |
            disney_df["Destination"].astype(str).str.contains("Pacific", case=False, na=False) |
            disney_df.get("Ports Of Call", pd.Series([""]*len(disney_df))).astype(str).str.contains("Pacific", case=False, na=False)
        )
        pacific_count = int(pacific_mask.sum())

        holiday_keywords = ["Holiday", "Christmas", "Halloween", "New Year", "Merrytime", "Thanksgiving"]
        holiday_pattern = "|".join(holiday_keywords)
        holiday_mask = (
            disney_df["Title"].astype(str).str.contains(holiday_pattern, case=False, na=False) |
            disney_df.get("Inclusions", pd.Series([""]*len(disney_df))).astype(str).str.contains(holiday_pattern, case=False, na=False)
        )
        holiday_count = int(holiday_mask.sum())

        if "Available Dates Count" in disney_df.columns:
            dates_gt_2 = int((pd.to_numeric(disney_df["Available Dates Count"], errors="coerce").fillna(0) > 2).sum())

        miami_london_mask = (
            disney_df["Departing From"].astype(str).str.contains("Miami", case=False, na=False) |
            disney_df["Departing From"].astype(str).str.contains("London|Southampton", case=False, na=False)
        )
        miami_london = int(miami_london_mask.sum())

    # Ingredients Metrics
    total_companies = len(ingr_df)
    total_ingredients_catalog = 0
    total_finished_catalog = 0
    herbs_spices = 0
    delivery_formats = 0
    cognitive_health = 0

    # Load from answers json if present
    if os.path.exists(INGREDIENTS_ANSWERS_JSON):
        try:
            with open(INGREDIENTS_ANSWERS_JSON, "r", encoding="utf-8") as f:
                ans = json.load(f)
                total_ingredients_catalog = ans.get("q1_total_ingredients", 0)
                total_finished_catalog = ans.get("q2_total_finished_products", 0)
        except Exception:
            pass

    if not ingr_df.empty:
        herbs_mask = (
            ingr_df["Categories"].astype(str).str.contains("herb|spice", case=False, na=False) |
            ingr_df["Company Description"].astype(str).str.contains("herb|spice", case=False, na=False)
        )
        herbs_spices = int(herbs_mask.sum())

        delivery_mask = (
            ingr_df["Categories"].astype(str).str.contains("delivery format|capsule|tablet|dosage", case=False, na=False) |
            ingr_df["Primary Business Activity"].astype(str).str.contains("contract|formulation|delivery", case=False, na=False) |
            ingr_df["Company Description"].astype(str).str.contains("delivery format|tablet|capsule", case=False, na=False)
        )
        delivery_formats = int(delivery_mask.sum())

        cognitive_mask = (
            ingr_df["Categories"].astype(str).str.contains("cognitive|mental|brain|nootropic", case=False, na=False) |
            ingr_df["Company Description"].astype(str).str.contains("cognitive|mental|brain|memory", case=False, na=False)
        )
        cognitive_health = int(cognitive_mask.sum())

    return {
        "disney_total": total_disney,
        "disney_pacific": pacific_count,
        "disney_holiday": holiday_count,
        "disney_dates_gt_2": dates_gt_2,
        "disney_miami_london": miami_london,
        "ingredients_companies": total_companies,
        "ingredients_catalog_total": total_ingredients_catalog,
        "finished_products_catalog_total": total_finished_catalog,
        "herbs_spices_count": herbs_spices,
        "delivery_formats_count": delivery_formats,
        "cognitive_health_count": cognitive_health
    }


@app.get("/api/metrics", response_class=JSONResponse)
def get_metrics_endpoint():
    return get_live_metrics()


@app.get("/api/disney", response_class=JSONResponse)
def get_disney_endpoint(q: Optional[str] = None):
    df = load_disney_df()
    if q and not df.empty:
        mask = (
            df["Title"].str.contains(q, case=False, na=False) |
            df["Departing From"].str.contains(q, case=False, na=False) |
            df["Destination"].str.contains(q, case=False, na=False)
        )
        df = df[mask]
    return df.to_dict(orient="records")


@app.get("/api/ingredients", response_class=JSONResponse)
def get_ingredients_endpoint(q: Optional[str] = None):
    df = load_ingredients_df()
    if q and not df.empty:
        mask = (
            df["Company Name"].str.contains(q, case=False, na=False) |
            df["Categories"].str.contains(q, case=False, na=False) |
            df["Primary Business Activity"].str.contains(q, case=False, na=False)
        )
        df = df[mask]
    return df.to_dict(orient="records")


@app.get("/", response_class=HTMLResponse)
def dashboard_home():
    disney_df = load_disney_df()
    ingr_df = load_ingredients_df()
    metrics = get_live_metrics()

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relu Consultancy | Data Extraction Engineer Challenge Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0b0f19;
            --surface: #121927;
            --surface-glass: rgba(18, 25, 39, 0.75);
            --border: rgba(255, 255, 255, 0.1);
            --primary: #38bdf8;
            --primary-glow: rgba(56, 189, 248, 0.2);
            --accent: #818cf8;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --success: #34d399;
            --warning: #fbbf24;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            min-height: 100vh;
            background-image: 
                radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.12) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(129, 140, 248, 0.12) 0px, transparent 50%);
            padding: 30px;
        }}
        .header {{
            max-width: 1400px;
            margin: 0 auto 30px auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
            padding-bottom: 20px;
        }}
        .badge {{
            background: var(--primary-glow);
            color: var(--primary);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            border: 1px solid rgba(56, 189, 248, 0.3);
            display: inline-block;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
            max-width: 1400px;
            margin: 0 auto 35px auto;
        }}
        .metric-card {{
            background: var(--surface-glass);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 22px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }}
        .metric-card:hover {{
            transform: translateY(-4px);
            border-color: var(--primary);
        }}
        .metric-title {{
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin-bottom: 8px;
        }}
        .metric-value {{
            font-size: 2.2rem;
            font-weight: 700;
            color: var(--primary);
        }}
        .metric-sub {{
            color: var(--text-muted);
            font-size: 0.8rem;
            margin-top: 6px;
        }}
        .tabs-nav {{
            max-width: 1400px;
            margin: 0 auto 20px auto;
            display: flex;
            gap: 12px;
        }}
        .tab-btn {{
            background: var(--surface);
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 12px 24px;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: inherit;
            font-size: 0.95rem;
        }}
        .tab-btn.active {{
            background: var(--primary);
            color: #0b0f19;
            border-color: var(--primary);
            box-shadow: 0 4px 16px var(--primary-glow);
        }}
        .tab-content {{
            max-width: 1400px;
            margin: 0 auto;
            display: none;
        }}
        .tab-content.active {{
            display: block;
        }}
        .table-container {{
            background: var(--surface-glass);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 16px;
            overflow-x: auto;
            box-shadow: 0 10px 40px rgba(0,0,0,0.4);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.9rem;
        }}
        th {{
            background: rgba(255, 255, 255, 0.03);
            color: var(--text-muted);
            padding: 16px 20px;
            font-weight: 600;
            border-bottom: 1px solid var(--border);
            white-space: nowrap;
        }}
        td {{
            padding: 16px 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            vertical-align: top;
        }}
        tr:hover td {{
            background: rgba(255, 255, 255, 0.02);
        }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>Relu Consultancy Data Extraction Challenge</h1>
            <p style="color: var(--text-muted); margin-top: 6px;">Live Extracted Dataset & Persistence Audit Dashboard</p>
        </div>
        <div class="badge">OPERATOR: aiwolfie | SECTOR 7G</div>
    </div>

    <!-- Executive Metrics Grid: Computed Dynamically -->
    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-title">Disney Cruises Loaded</div>
            <div class="metric-value">{metrics['disney_total']}</div>
            <div class="metric-sub">Pacific: {metrics['disney_pacific']} | Holiday: {metrics['disney_holiday']}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Cruises > 2 Booking Dates</div>
            <div class="metric-value">{metrics['disney_dates_gt_2']}</div>
            <div class="metric-sub">Miami / London Departures: {metrics['disney_miami_london']}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Ingredients Companies</div>
            <div class="metric-value">{metrics['ingredients_companies']}</div>
            <div class="metric-sub">Herbs & Spices: {metrics['herbs_spices_count']} | Delivery: {metrics['delivery_formats_count']}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Cognitive & Mental Health</div>
            <div class="metric-value">{metrics['cognitive_health_count']}</div>
            <div class="metric-sub">Catalog Facets: {metrics['ingredients_catalog_total']} Ing / {metrics['finished_products_catalog_total']} Prod</div>
        </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="tabs-nav">
        <button class="tab-btn active" onclick="switchTab('disney')">🚢 Disney Cruise Line (Challenge 1 - {len(disney_df)} Records)</button>
        <button class="tab-btn" onclick="switchTab('ingredients')">🌿 Ingredients Network (Challenge 2 - {len(ingr_df)} Companies)</button>
    </div>

    <!-- Disney Cruise View -->
    <div id="disney-tab" class="tab-content active">
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Cruise Title</th>
                        <th>Departing From</th>
                        <th>Destination</th>
                        <th>Duration</th>
                        <th>Dates Count</th>
                        <th>Starting Price</th>
                        <th>Ports Of Call</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join([f'''<tr>
                        <td style="font-weight:600; color:var(--text-main);">{row.get('Title','')}</td>
                        <td>{row.get('Departing From','')}</td>
                        <td><span class="badge">{row.get('Destination','')}</span></td>
                        <td>{row.get('Duration','')}</td>
                        <td>{row.get('Available Dates Count','')}</td>
                        <td style="color:var(--success); font-weight:600;">{row.get('Starting Price','')}</td>
                        <td style="max-width:320px; color:var(--text-muted);">{row.get('Ports Of Call','')}</td>
                    </tr>''' for _, row in disney_df.iterrows()]) if not disney_df.empty else '<tr><td colspan="7" style="text-align:center; padding:30px;">No Disney Cruise records loaded. Run scraper to populate.</td></tr>'}
                </tbody>
            </table>
        </div>
    </div>

    <!-- Ingredients Network View -->
    <div id="ingredients-tab" class="tab-content">
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Company Name</th>
                        <th>Primary Business Activity</th>
                        <th>Sales Markets</th>
                        <th>Categories</th>
                        <th>Events</th>
                        <th>Email</th>
                        <th>Telephone</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join([f'''<tr>
                        <td style="font-weight:600; color:var(--text-main);">{row.get('Company Name','')}</td>
                        <td>{row.get('Primary Business Activity','')}</td>
                        <td>{row.get('Sales Markets','')}</td>
                        <td style="max-width:280px; color:var(--text-muted);">{row.get('Categories','')}</td>
                        <td><span class="badge">{row.get('Events','')}</span></td>
                        <td>{row.get('Email','')}</td>
                        <td>{row.get('Telephone','')}</td>
                    </tr>''' for _, row in ingr_df.iterrows()]) if not ingr_df.empty else '<tr><td colspan="7" style="text-align:center; padding:30px;">No Ingredients records loaded. Run scraper to populate.</td></tr>'}
                </tbody>
            </table>
        </div>
    </div>

    <script>
        function switchTab(tabName) {{
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            if (tabName === 'disney') {{
                document.querySelectorAll('.tab-btn')[0].classList.add('active');
                document.getElementById('disney-tab').classList.add('active');
            }} else {{
                document.querySelectorAll('.tab-btn')[1].classList.add('active');
                document.getElementById('ingredients-tab').classList.add('active');
            }}
        }}
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
