# 📊 Site Reliability Engineering (SRE) & Service Level Framework

This document defines the Service Level Indicators (SLIs), Service Level Objectives (SLOs), Error Budgets, CloudWatch Dashboards, and Metric Alarms for the **Rolex Price API SaaS Platform**.

---

## 🎯 Service Level Indicators (SLIs) & Objectives (SLOs)

Reliability metrics are tracked natively using AWS CloudWatch:

| Dimension | Indicator (SLI) | Target SLO | Measurement Window | Monitoring Metric |
| :--- | :--- | :--- | :--- | :--- |
| **Availability** | Ratio of non-5XX responses to total API requests | **99.9%** | Rolling 30 Days | `AWS/Lambda Errors` & `AWS/ApiGateway 5XXError` |
| **Latency (p95)** | End-to-end request duration at API Gateway / Lambda | **< 500ms** | Rolling 30 Days | `AWS/Lambda Duration (p95)` |
| **Latency (p99)** | End-to-end request duration at API Gateway / Lambda | **< 1000ms** | Rolling 30 Days | `AWS/Lambda Duration (p99)` |
| **Error Rate** | Proportion of unhandled server exceptions | **< 0.1%** | 24 Hours | `AWS/Lambda Errors / Invocations` |
| **Throttling Rate**| Proportion of requests rejected due to concurrency limits | **0.00%** | 5 Minutes | `AWS/Lambda Throttles` |

---

## 📉 Error Budget & Burn Rate Policy

- **Monthly Error Budget**: For a 99.9% availability SLO, the allowable error budget is **0.1%** (approx. 43.2 minutes of total downtime per 30-day month).
- **Fast Burn Alert**: Triggers an immediate critical alert if 2% of the error budget is consumed in a 1-hour window.
- **Slow Burn Alert**: Triggers a notification if 5% of the error budget is consumed in a 6-hour window.
- **Budget Exhaustion**: If the 30-day error budget drops below 0%, feature deployments are automatically paused to prioritize platform stability.

---

## 🖥️ Operational CloudWatch Dashboard

The infrastructure provisions an automated CloudWatch Dashboard (`rolex-price-api-dev-dashboard`) via Terraform:

```
┌──────────────────────────────────────────────┬──────────────────────────────────────────────┐
│  Widget 1: Lambda Invocations & Errors        │  Widget 2: Lambda Execution Duration         │
│  - Invocations (Sum, 60s)                     │  - Avg Duration (ms)                         │
│  - Errors (Sum, 60s) [Red]                    │  - p95 Duration (ms) [Orange]                │
│  - Throttles (Sum, 60s) [Orange]              │  - p99 Duration (ms) [Red]                   │
└──────────────────────────────────────────────┴──────────────────────────────────────────────┘
```

---

## 🔔 CloudWatch Metric Alarms & Metric Rationale

| Alarm Name | Trigger Condition | Evaluation Period | Metric Rationale |
| :--- | :--- | :--- | :--- |
| `lambda_errors` | `Errors >= 1` | 1 period (5 mins) | **Errors**: Detects unhandled exceptions or runtime failures in FastAPI Lambda execution. |
| `lambda_throttles` | `Throttles >= 1` | 1 period (5 mins) | **Throttles**: Indicates account-level concurrency limits hit or burst capacity exhausted. |
| `lambda_high_latency` | `Duration (p95) > 1000ms` | 2 periods (10 mins) | **Latency**: Identifies severe cold starts, payload serialization delays, or network bottlenecks. |

### Why Each Metric Matters
1. **Invocations**: Tracks overall API traffic volume and request spikes.
2. **Errors**: Immediate signal of application code bugs or unhandled 500 internal server errors.
3. **Duration**: Measures user experience and latency SLAs; high duration directly impacts AWS billing cost.
4. **Throttles**: Prevents silent drops when concurrent request limits are exceeded.
