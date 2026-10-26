# Emergency Department Raw Data Dictionary

This folder contains simulated and empirical emergency department operational logs used for input modeling.

### Schema (`emergency_department_logs_raw.csv`)

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `patient_id` | `STRING` | Unique identifier for each arriving patient |
| `arrival_timestamp` | `DATETIME` | Time when the patient checked in at the ED desk |
| `triage_start` | `DATETIME` | Timestamp when triage nurse began evaluation |
| `triage_end` | `DATETIME` | Timestamp when triage nurse completed evaluation |
| `doctor_assigned` | `DATETIME` | Timestamp when physician began treatment |
| `discharge_timestamp` | `DATETIME` | Timestamp when patient completed treatment and left |
| `acuity_level` | `INTEGER` | Patient triage severity score (1 = Urgent, 5 = Non-urgent) |
