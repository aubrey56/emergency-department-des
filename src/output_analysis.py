"""
output_analysis.py
------------------
Statistical output analysis, variance reduction, and hypothesis testing.

Module Mapping: HSTA231 (Design of Experiments), HSTA235 (Hypothesis Testing)
"""

import numpy as np
import scipy.stats as stats
from des_engine import run_single_replication
from typing import Dict, Tuple, List, Any

class OutputAnalyzer:
    def __init__(self, base_config: Dict[str, Any], replications: int = 30):
        self.base_config = base_config
        self.replications = replications

    def compare_policies(
        self, 
        policy_a: Dict[str, int], 
        policy_b: Dict[str, int]
    ) -> Dict[str, Any]:
        """
        Compares two staffing configurations using Common Random Numbers (CRN)
        and a paired t-test.
        """
        results_a: List[float] = []
        results_b: List[float] = []

        config_a = {**self.base_config, **policy_a}
        config_b = {**self.base_config, **policy_b}

        # Run replications with Common Random Numbers (CRN)
        for seed in range(self.replications):
            results_a.append(run_single_replication(config_a, seed=seed))
            results_b.append(run_single_replication(config_b, seed=seed))

        # Paired t-test (HSTA235)
        t_stat, p_val = stats.ttest_rel(results_a, results_b)

        # 95% Confidence Intervals
        mean_a, ci_a = self._calc_ci(results_a)
        mean_b, ci_b = self._calc_ci(results_b)

        return {
            "policy_a": {"mean": mean_a, "ci": ci_a, "raw": results_a},
            "policy_b": {"mean": mean_b, "ci": ci_b, "raw": results_b},
            "hypothesis_test": {
                "t_stat": t_stat,
                "p_value": p_val,
                "statistically_significant": p_val < 0.05
            }
        }

    @staticmethod
    def _calc_ci(data: List[float], confidence: float = 0.95) -> Tuple[float, Tuple[float, float]]:
        mean = float(np.mean(data))
        sem = stats.sem(data)
        margin = sem * stats.t.ppf((1 + confidence) / 2.0, len(data) - 1)
        return mean, (mean - margin, mean + margin)


if __name__ == "__main__":
    base_params = {
        'iat_scale': 5.2,
        'triage_shape': 2.481,
        'triage_scale': 4.137,
        'doc_s': 0.5,
        'doc_scale': 10.0
    }

    analyzer = OutputAnalyzer(base_params, replications=30)
    
    policy_a = {'num_nurses': 2, 'num_doctors': 2}  # Option A
    policy_b = {'num_nurses': 1, 'num_doctors': 3}  # Option B

    report = analyzer.compare_policies(policy_a, policy_b)

    print("=== EXPERIMENTAL OUTPUT ANALYSIS ===")
    print(f"Policy A (2 Nurses, 2 Doctors): Mean = {report['policy_a']['mean']:.2f} mins, 95% CI = ({report['policy_a']['ci'][0]:.2f}, {report['policy_a']['ci'][1]:.2f})")
    print(f"Policy B (1 Nurse, 3 Doctors) : Mean = {report['policy_b']['mean']:.2f} mins, 95% CI = ({report['policy_b']['ci'][0]:.2f}, {report['policy_b']['ci'][1]:.2f})")
    print(f"Paired t-statistic: {report['hypothesis_test']['t_stat']:.4f}")
    print(f"p-value           : {report['hypothesis_test']['p_value']:.4e}")
    print(f"Significant Diff  : {report['hypothesis_test']['statistically_significant']}")
