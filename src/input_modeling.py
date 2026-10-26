if __name__ == "__main__":
    import pandas as pd
    from data_loader import process_raw_logs, generate_synthetic_raw_data
    import os
    
    raw_path = "data/raw/emergency_department_logs_raw.csv"
    proc_path = "data/processed/fitted_input_metrics.csv"
    
    if not os.path.exists(raw_path):
        generate_synthetic_raw_data(500, raw_path)
        
    df = process_raw_logs(raw_path, proc_path)
    
    modeler = InputModeler()
    
    # Fit Triage Duration (Gamma Distribution)
    triage_params, triage_gof = modeler.fit_gamma_distribution(df['triage_duration'].values)
    
    # Fit Inter-Arrival Time (Exponential Distribution)
    iat_params, iat_gof = modeler.fit_exponential_distribution(df['inter_arrival_time'].values)
    
    print("\n=== FITTED INPUT DISTRIBUTIONS FROM DATA ===")
    print(f"IAT (Exponential)  : Scale = {iat_params['scale']:.3f} | K-S p-val = {iat_gof['p_value']:.4f}")
    print(f"Triage (Gamma)     : Shape = {triage_params['shape']:.3f}, Scale = {triage_params['scale']:.3f} | K-S p-val = {triage_gof['p_value']:.4f}")
