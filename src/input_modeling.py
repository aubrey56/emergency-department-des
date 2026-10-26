"""
input_modeling.py
-----------------
Module for fitting probability distributions to empirical hospital logs 
and conducting Goodness-of-Fit hypothesis testing.

Module Mapping: HSTA239 (Estimation Techniques), HSTA235 (Hypothesis Testing)
"""

import numpy as np
import scipy.stats as stats
import pandas as pd
from typing import Dict, Tuple, Any

class InputModeler:
    def __init__(self, seed: int = 42):
        np.random.seed(seed)

    def fit_gamma_distribution(self, data: np.ndarray) -> Tuple[Dict[str, float], Dict[str, float]]:
        """
        Fits a Gamma distribution using MLE and conducts K-S Goodness-of-Fit test.
        """
        # MLE Parameter Estimation (HSTA239)
        alpha_hat, loc_hat, beta_hat = stats.gamma.fit(data, floc=0)
        
        # Kolmogorov-Smirnov Test (HSTA235)
        ks_stat, p_value = stats.kstest(data, 'gamma', args=(alpha_hat, loc_hat, beta_hat))
        
        params = {"shape": alpha_hat, "scale": beta_hat}
        gof = {"ks_stat": ks_stat, "p_value": p_value, "valid": p_value > 0.05}
        
        return params, gof

    def fit_exponential_distribution(self, data: np.ndarray) -> Tuple[Dict[str, float], Dict[str, float]]:
        """
        Fits an Exponential distribution for Inter-Arrival Times (Poisson Process).
        """
        loc_hat, scale_hat = stats.expon.fit(data, floc=0)
        ks_stat, p_value = stats.kstest(data, 'expon', args=(loc_hat, scale_hat))
        
        params = {"scale": scale_hat}
        gof = {"ks_stat": ks_stat, "p_value": p_value, "valid": p_value > 0.05}
        
        return params, gof

    def fit_lognormal_distribution(self, data: np.ndarray) -> Tuple[Dict[str, float], Dict[str, float]]:
        """
        Fits a Lognormal distribution for doctor consultation durations.
        """
        s_hat, loc_hat, scale_hat = stats.lognorm.fit(data, floc=0)
        ks_stat, p_value = stats.kstest(data, 'lognorm', args=(s_hat, loc_hat, scale_hat))
        
        params = {"s": s_hat, "scale": scale_hat}
        gof = {"ks_stat": ks_stat, "p_value": p_value, "valid": p_value > 0.05}
        
        return params, gof


if __name__ == "__main__":
    # Generate representative empirical data sample
    np.random.seed(42)
    sample_triage_data = np.random.gamma(shape=2.5, scale=4.0, size=500)
    
    modeler = InputModeler()
    params, gof = modeler.fit_gamma_distribution(sample_triage_data)
    
    print("=== INPUT MODELING & FIT RESULTS ===")
    print(f"Fitted Parameters : Shape (Alpha) = {params['shape']:.4f}, Scale (Beta) = {params['scale']:.4f}")
    print(f"K-S Statistic     : {gof['ks_stat']:.4f}")
    print(f"p-value           : {gof['p_value']:.4f}")
    print(f"Model Validated   : {gof['valid']} (Fail to reject H0)")
