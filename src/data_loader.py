"""
data_loader.py
--------------
Module for loading raw emergency room timestamp logs and computing 
inter-arrival times, triage durations, and doctor consultation durations.

Module Mapping: HSTA104 (Statistical Computing 1), HSTA236 (Survey/Data Techniques)
"""

import pandas as pd
import numpy as np
import os
from typing import Tuple

def generate_synthetic_raw_data(num_records: int = 500, output_path: str = "data/raw/emergency_department_logs_raw.csv"):
    """
    Generates a realistic synthetic dataset of patient logs if raw data is missing.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    np.random.seed(42)
    start_time = pd.Timestamp("2026-10-01 08:00:00")
    
    # Generate Exponential Inter-arrival times (avg 5.2 mins)
    iats = np.random.exponential(scale=5.2, size=num_records)
    arrival_offsets = np.cumsum(iats)
    
    arrival_times = [start_time + pd.Timedelta(minutes=float(m)) for m in arrival_offsets]
    
    # Generate service durations
    triage_durations = np.random.gamma(shape=2.481, scale=4.137, size=num_records)
    doc_durations = np.random.lognormal(mean=2.3, sigma=0.5, size=num_records)
    
    records = []
    for i in range(num_records):
        arr = arrival_times[i]
        trg_start = arr + pd.Timedelta(minutes=float(np.random.uniform(0.5, 2.0)))
        trg_end = trg_start + pd.Timedelta(minutes=float(triage_durations[i]))
        doc_start = trg_end + pd.Timedelta(minutes=float(np.random.uniform(1.0, 5.0)))
        doc_end = doc_start + pd.Timedelta(minutes=float(doc_durations[i]))
        
        records.append({
            "patient_id": f"PAT_{i+1:04d}",
            "arrival_timestamp": arr,
            "triage_start": trg_start,
            "triage_end": trg_end,
            "doctor_assigned": doc_start,
            "discharge_timestamp": doc_end,
            "acuity_level": int(np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.2, 0.4, 0.2, 0.1]))
        })
        
    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)
    print(f"Generated raw synthetic dataset with {num_records} records at: {output_path}")

def process_raw_logs(raw_csv_path: str, processed_csv_path: str) -> pd.DataFrame:
    """
    Loads raw CSV timestamp data, calculates duration columns in minutes, 
    and exports clean numerical series for distribution fitting.
    """
    df = pd.read_csv(raw_csv_path)
    
    # Convert string columns to datetime
    time_cols = ['arrival_timestamp', 'triage_start', 'triage_end', 'doctor_assigned', 'discharge_timestamp']
    for col in time_cols:
        df[col] = pd.to_datetime(df[col])
        
    # Calculate duration features in minutes
    df_clean = pd.DataFrame()
    df_clean['inter_arrival_time'] = df['arrival_timestamp'].diff().dt.total_seconds() / 60.0
    df_clean['triage_duration'] = (df['triage_end'] - df['triage_start']).dt.total_seconds() / 60.0
    df_clean['doctor_duration'] = (df['discharge_timestamp'] - df['doctor_assigned']).dt.total_seconds() / 60.0
    
    # Drop initial NaN inter-arrival time
    df_clean = df_clean.dropna().reset_index(drop=True)
    
    os.makedirs(os.path.dirname(processed_csv_path), exist_ok=True)
    df_clean.to_csv(processed_csv_path, index=False)
    print(f"Exported processed metrics ({len(df_clean)} rows) to: {processed_csv_path}")
    
    return df_clean

if __name__ == "__main__":
    raw_path = "data/raw/emergency_department_logs_raw.csv"
    processed_path = "data/processed/fitted_input_metrics.csv"
    
    # Generate synthetic raw data if it doesn't exist yet
    if not os.path.exists(raw_path):
        generate_synthetic_raw_data(num_records=500, output_path=raw_path)
        
    processed_df = process_raw_logs(raw_path, processed_path)
    print("\nProcessed Data Preview:")
    print(processed_df.head())
