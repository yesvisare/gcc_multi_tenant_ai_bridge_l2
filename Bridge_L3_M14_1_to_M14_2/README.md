# Bridge: M14.1 → M14.2 Validation

## Purpose

This bridge validates your readiness to move from:
- **M14.1:** Monitoring & Observability
- **M14.2:** Incident Management & Blast Radius

**Type:** Readiness Validation

**The Critical Gap:** Detection doesn't equal containment. The Black Friday 2024 case study demonstrates this: one GCC detected analytics failure in 4 minutes but couldn't contain it—cascade spread to 47 business units, ₹6.2 crore loss, 3 Fortune 500 client escalations. M14.2 closes this gap with 60-second automatic blast radius isolation.

---

## What This Bridge Validates

### Readiness Checks (5 total)

#### 1. **Tenant-Aware Metrics**
   - **Pass Criteria:**
     - ✓ Prometheus configuration file exists with multi-tenant scrape configs
     - ✓ Metrics include `tenant_id` label in all application services
     - ✓ At least 50 distinct tenant IDs are present in metrics
     - ✓ Core metrics (request_count, error_rate, latency) are tenant-tagged
   - **Purpose:** Enables per-tenant monitoring and blast radius detection in M14.2

#### 2. **Drill-Down Dashboards**
   - **Pass Criteria:**
     - ✓ Grafana dashboard JSON files exist for multi-tenant views
     - ✓ Dashboards support tenant_id variable for filtering
     - ✓ Navigation flows from platform-level to tenant-specific without context switching
     - ✓ Key panels show: request volume, error rates, latency P50/P95/P99 per tenant
   - **Purpose:** Supports rapid incident triage during blast radius events

#### 3. **Distributed Tracing**
   - **Pass Criteria:**
     - ✓ OpenTelemetry SDK instrumented in all services (5+ microservices)
     - ✓ Tenant context propagated via trace headers
     - ✓ Spans include tenant_id attribute
     - ✓ Tracing backend (Jaeger/Tempo) configured to receive tenant-tagged traces
   - **Purpose:** Enables trace-level isolation for incident root cause analysis

#### 4. **SLA Budget Tracking**
   - **Pass Criteria:**
     - ✓ Error budget calculation logic implemented per tenant
     - ✓ Alerts configured for 80% error budget consumption
     - ✓ SLA targets defined (e.g., 99.9% uptime, <500ms P95 latency)
     - ✓ Historical budget burn rate tracking enabled
   - **Purpose:** Informs incident priority calculation (P0/P1/P2) in M14.2

#### 5. **Detection Speed Achievement**
   - **Pass Criteria:**
     - ✓ Automated alerting rules defined for critical conditions
     - ✓ Alert notification channels configured (PagerDuty, Slack, email)
     - ✓ Detection speed measured and documented (target: <5 minutes)
     - ✓ Baseline comparison established (before: manual, after: automated)
   - **Purpose:** Fast detection (3 min) enables 60-second containment window in M14.2

---

## How to Run

### Prerequisites
- Completed M14.1 (Monitoring & Observability)
- Python 3.9+
- Jupyter Notebook

### Steps

**Windows (PowerShell):**
```powershell
cd Bridge_L3_M14_1_to_M14_2
$env:PYTHONPATH = "$PWD"
jupyter notebook
```

**Mac/Linux:**
```bash
cd Bridge_L3_M14_1_to_M14_2
export PYTHONPATH="$PWD"
jupyter notebook
```

**Then:**
1. Open `Bridge_L3_M14_1_to_M14_2_Readiness.ipynb`
2. Run all cells (`Cell → Run All`)
3. Check results for each of the 5 validation checks

---

## Pass Criteria

**To proceed to M14.2, you must:**
- ✓ All 5 checks pass
- ✓ No critical gaps (✗)
- ✓ Understand how M14.1 observability enables M14.2 containment

**If checks fail:**
1. Read failure messages (they include actionable fixes)
2. Complete missing work from M14.1
3. Re-run this bridge notebook

---

## Common Issues

### Issue: Missing Prometheus configuration
**Symptoms:** `✗ Missing: prometheus.yml`
**Fix:** Export your Prometheus configuration to the project root. Ensure it includes tenant_id labels in scrape configs.

### Issue: No Grafana dashboards found
**Symptoms:** `✗ Missing: grafana/dashboards directory`
**Fix:**
1. Create `grafana/dashboards/` directory
2. Export Grafana dashboards as JSON files
3. Place them in this directory

### Issue: OpenTelemetry not instrumented
**Symptoms:** Cannot answer "Is tenant_id propagated across services?"
**Fix:**
1. Review M14.1 distributed tracing module
2. Instrument each microservice with OpenTelemetry SDK
3. Add tenant_id to span attributes

### Issue: SLA budgets not defined
**Symptoms:** Cannot specify uptime/latency targets per tenant tier
**Fix:**
1. Define SLA targets for Platinum/Gold/Silver tiers
2. Implement error budget calculations in Prometheus/Grafana
3. Configure 80% consumption alerts

### Issue: Detection speed not measured
**Symptoms:** Cannot verify <5 minute mean-time-to-detection
**Fix:**
1. Review M14.1 alerting configuration
2. Test alert delivery end-to-end
3. Measure time from anomaly injection to notification

---

## Time Estimate

- **First time:** 20-30 minutes
- **If all checks pass:** 10-15 minutes
- **If rework needed:** 30-60 minutes (return to M14.1)

---

## Support

**If stuck:**
- Review M14.1 materials (Monitoring & Observability)
- Check failure messages in notebook (they include fixes)
- Reach out: support@techvoyagehub.com

---

## Next Steps

**After passing all 5 checks:**
→ Proceed to **M14.2: Incident Management & Blast Radius**

**Module M14.2 will cover:**

M14.2 transforms your M14.1 detection into automatic containment:

1. **Blast Radius Detector** — Monitors all 50 tenants every 10 seconds; triggers on >50% error threshold
2. **Per-Tenant Circuit Breakers** — Opens after 5 consecutive failures; 60-second recovery timeout; protects 49 healthy tenants from 1 failing tenant
3. **Incident Priority Calculator** — P0/P1/P2 classification based on tenant tier + affected count
4. **Automated Notification System** — 5-minute alert window; PagerDuty/Opsgenie/ServiceNow integration
5. **Runbook Templates** — 10+ pre-built playbooks for multi-tenant failure scenarios

**Business Impact:**
- **Cost:** ₹5 crore platform outage → ₹10 lakh contained incident (50× reduction)
- **Speed:** 45-minute manual response → 60-second automatic isolation
- **Career:** Platform engineer (₹18-22L) → Reliability engineer with incident mgmt (₹22-28L)

**You're ready because:**
- Tenant-aware metrics enable blast radius calculation
- Drill-down dashboards support rapid triage
- Distributed tracing pinpoints failure origin
- SLA budgets inform priority classification
- Fast detection (3 min) allows 60-second containment
