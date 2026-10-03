"""
OmniExtract Analytics Engine - Maritime Division
Itinerary metrics and validation module
"""

import os
import sys
import json
import pandas as pd

def analyze_disney_data(csv_path: str = "results_disney.csv"):
    if not os.path.exists(csv_path):
        if os.path.exists("results.csv"):
            csv_path = "results.csv"
        else:
            print(f"[ERROR] Neither '{csv_path}' nor 'results.csv' found.")
            return

    df = pd.read_csv(csv_path)
    print(f"[INFO] Loaded dataset from {csv_path} with {len(df)} rows.")

    # (i) Pacific destination count
    pacific_mask = (
        df["Title"].astype(str).str.contains("Pacific", case=False, na=False) |
        df["Destination"].astype(str).str.contains("Pacific", case=False, na=False) |
        df["Ports Of Call"].astype(str).str.contains("Pacific", case=False, na=False)
    )
    q1 = int(pacific_mask.sum())

    # (ii) Total cruises
    q2 = int(len(df))

    # (iii) Holiday cruises
    holiday_keywords = ["Holiday", "Christmas", "Halloween", "New Year", "Merrytime", "Thanksgiving"]
    holiday_pattern = "|".join(holiday_keywords)
    holiday_mask = (
        df["Title"].astype(str).str.contains(holiday_pattern, case=False, na=False) |
        df.get("Inclusions", pd.Series([""] * len(df))).astype(str).str.contains(holiday_pattern, case=False, na=False)
    )
    q3 = int(holiday_mask.sum())

    # (iv) Cruises offering more than 2 dates for booking
    if "Available Dates Count" in df.columns:
        q4 = int((pd.to_numeric(df["Available Dates Count"], errors="coerce").fillna(0) > 2).sum())
    else:
        q4 = 0

    # (v) Cruises with Miami and London as departure ports
    miami_london_mask = (
        df["Departing From"].astype(str).str.contains("Miami", case=False, na=False) |
        df["Departing From"].astype(str).str.contains("London", case=False, na=False) |
        df["Departing From"].astype(str).str.contains("Southampton", case=False, na=False)
    )
    q5 = int(miami_london_mask.sum())

    report = f"""
================================================================================
OMNIEXTRACT MARITIME PIPELINE - DISNEY CRUISE LINE EVALUATION REPORT
Target: Disney Cruise Line (disneycruise.disney.go.com)
================================================================================
(i)   Total cruises for the Pacific as a destination: {q1}
(ii)  Total cruises extracted: {q2}
(iii) Total holiday cruises: {q3}
(iv)  Cruises offering more than 2 dates for booking: {q4}
(v)   Cruises with Miami and London as departure ports: {q5}
================================================================================
"""
    print(report)

    answers = {
        "q1_pacific_cruises": q1,
        "q2_total_cruises": q2,
        "q3_holiday_cruises": q3,
        "q4_more_than_2_dates": q4,
        "q5_miami_london_departure": q5
    }
    with open("disney_answers.json", "w", encoding="utf-8") as f:
        json.dump(answers, f, indent=2)
    print("[SUCCESS] Answers exported to disney_answers.json for Google Form entry.")

if __name__ == "__main__":
    csv_file = sys.argv[1] if len(sys.argv) > 1 else "results_disney.csv"
    analyze_disney_data(csv_file)
