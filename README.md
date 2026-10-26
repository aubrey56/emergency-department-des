# Discrete Event Simulation & Output Analysis of Emergency Department Operations

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Applied Statistics](https://img.shields.io/badge/Applied%20Statistics-BSc%20Honours-green.svg)](#)

## 📌 Project Overview
This repository implements a **Stochastic Discrete Event Simulation (DES)** of an Emergency Department (ED) queueing network to optimize resource allocation under constrained budgets. 

Using empirical arrival and service logs, the project demonstrates end-to-end statistical modeling: from **Maximum Likelihood Estimation (MLE)** and **Kolmogorov-Smirnov goodness-of-fit testing** to **Variance Reduction via Common Random Numbers (CRN)** and **Paired Hypothesis Testing**.

---

## 🎓 Curriculum & Statistical Methodology Mapping

This project applies core techniques from the **BSc Honours in Applied Statistics** degree curriculum:

| Simulation Pipeline Stage | Applied Statistics Module | Applied Methodology |
| :--- | :--- | :--- |
| **Input Modeling** | `HSTA239` Estimation Techniques | Maximum Likelihood Estimation (MLE) for parametric distribution fitting |
| **Model Verification** | `HSTA235` Hypothesis Testing | Kolmogorov-Smirnov (K-S) Goodness-of-Fit testing ($\alpha = 0.05$) |
| **Stochastic Engine** | `HSTA133` Probability Theory I | Non-Homogeneous Poisson Processes & Inverse Transform Sampling |
| **Queue Architecture** | `HSTA240` Operations Research | Multi-server $M/M/c$ queuing theory dynamics |
| **Experimental Design** | `HSTA231` Design & Design Issues | Factorial experimental design & Common Random Numbers (CRN) |
| **Output Analysis** | `HSTA235` / `HSTA237` Time Series & Inference | Welch's warm-up period truncation & Paired $t$-tests |

---

## 🔬 Key Statistical Findings

### 1. Input Distribution Fitting
Empirical triage times were fitted against theoretical distributions using MLE. A Kolmogorov-Smirnov test confirmed that a Gamma distribution provides a statistically valid fit:
* **Fitted Distribution:** $\text{Gamma}(\alpha = 2.481, \beta = 4.137)$
* **K-S Statistic:** $0.0321$
* **$p$-value:** $0.6390 \gg 0.05$ (Fail to reject $H_0$; distribution validated)

### 2. Staffing Optimization Experiment
We evaluated two competing staffing policies under a fixed operational budget:
* **Option A:** 2 Triage Nurses, 2 Treatment Doctors
* **Option B:** 1 Triage Nurse, 3 Treatment Doctors

Using $n = 30$ independent replications with Common Random Numbers (CRN):

$$\text{Paired } t\text{-test Result: } t = 8.421, \quad p = 1.42 \times 10^{-9}$$

**Decision:** Reject $H_0$. Adding doctor capacity (Option B) produces a statistically significant reduction in overall patient length-of-stay compared to adding triage capacity.

---

## 🛠️ Project Structure & Execution

### Installation

```bash
git clone [https://github.com/aubreymoyo/emergency-department-des.git](https://github.com/aubreymoyo/emergency-department-des.git)
cd emergency-department-des
pip install -r requirements.txt
