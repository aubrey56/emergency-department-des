"""
des_engine.py
-------------
Discrete Event Simulation engine for Emergency Department queue dynamics.

Module Mapping: HSTA133 (Probability Theory), HSTA240 (Operations Research)
"""

import simpy
import numpy as np
from typing import List, Dict, Any

class EmergencyDepartmentSim:
    def __init__(self, env: simpy.Environment, config: Dict[str, Any]):
        self.env = env
        self.config = config
        
        # Resources (M/M/c and M/G/c queue capacity)
        self.nurses = simpy.Resource(env, capacity=config['num_nurses'])
        self.doctors = simpy.Resource(env, capacity=config['num_doctors'])
        
        # Performance Tracking
        self.system_times: List[float] = []

    def patient_flow(self):
        arrival_time = self.env.now
        
        # Stage 1: Triage (Fitted Gamma Distribution)
        with self.nurses.request() as req:
            yield req
            triage_duration = np.random.gamma(
                shape=self.config['triage_shape'], 
                scale=self.config['triage_scale']
            )
            yield self.env.timeout(triage_duration)

        # Stage 2: Doctor Consultation (Fitted Lognormal Distribution)
        with self.doctors.request() as req:
            yield req
            doc_duration = np.random.lognormal(
                mean=np.log(self.config['doc_scale']), 
                sigma=self.config['doc_s']
            )
            yield self.env.timeout(doc_duration)

        # System Length of Stay
        self.system_times.append(self.env.now - arrival_time)

    def arrival_generator(self):
        while True:
            # Inter-Arrival Times (Exponential Distribution / Poisson Process)
            iat = np.random.exponential(scale=self.config['iat_scale'])
            yield self.env.timeout(iat)
            self.env.process(self.patient_flow())


def run_single_replication(config: Dict[str, Any], sim_time: float = 480.0, seed: int = None) -> float:
    """Runs a single simulation replication and returns average system time."""
    if seed is not None:
        np.random.seed(seed)
        
    env = simpy.Environment()
    sim = EmergencyDepartmentSim(env, config)
    
    env.process(sim.arrival_generator())
    env.run(until=sim_time)
    
    return float(np.mean(sim.system_times)) if sim.system_times else 0.0


if __name__ == "__main__":
    test_config = {
        'num_nurses': 2,
        'num_doctors': 2,
        'iat_scale': 5.2,
        'triage_shape': 2.481,
        'triage_scale': 4.137,
        'doc_s': 0.5,
        'doc_scale': 10.0
    }
    
    mean_time = run_single_replication(test_config, seed=42)
    print(f"Single Replication Mean System Time: {mean_time:.2f} minutes")
