# 📊 Site Reliability Engineering (SRE) & Service Level Framework

This document defines the Service Level Indicators (SLIs), Service Level Objectives (SLOs), Error Budgets, and Incident Management procedures for the **Rolex Price API SaaS Platform**.

---

## 🎯 Service Level Objectives (SLOs)

We define target service performance across key reliability dimensions:

| Service Aspect | Indicator (SLI) | Target SLO | Measurement Window |
| :--- | :--- | :--- | :--- |
| **API Availability** | Successful HTTP requests (`2xx` / `4xx` vs `5xx`) | **99.9%** | Rolling 30 Days |
| **Latency (P95)** | End-to-end request duration at API Gateway | **< 250ms** | Rolling 30 Days |
| **Latency (P99)** | End-to-end request duration at API Gateway | **< 500ms** | Rolling 30 Days |
| **Database Read Errors**| DynamoDB System Error Count (`SystemErrors`) | **< 0.01%** | 24 Hours |

---

## 📉 Error Budget & Burn Rate Policy

- **Error Budget**: For a 99.9% uptime SLO, the allowable unreliability budget is **0.1%** (approx. 43.2 minutes of downtime per month).
- **Fast Burn Alert**: Triggered if 2% of the error budget is consumed in a 1-hour window (critical PagerDuty alert).
- **Slow Burn Alert**: Triggered if 5% of the error budget is consumed in 6 hours (warning Slack alert).
- **Budget Exhaustion**: If the 30-day error budget drops below 0%, feature deployments are automatically suspended to prioritize reliability fixes.

---

## 🔔 Observability & Alert Thresholds

1. **Structured Logging**: All Python loggers output structured JSON formatted with standard context keys (`timestamp`, `level`, `correlation_id`, `path`, `status_code`, `latency_ms`).
2. **CloudWatch Metrics**: Custom metric filters track `UnhandledExceptionCount`, `DynamoDBConditionCheckFailed`, and `APIColdStartDuration`.
3. **Synthetic Canaries**: AWS CloudWatch Synthetics canary pinging `GET /health` every 60 seconds from multi-region locations.
