# Monitoring & Reliability — Campus IT Helpdesk (25RP19452-NIYONKURU)

This document summarizes the in-cluster monitoring, alerting and logging setup and provides quick runbook commands for incident response.

## Components Deployed

- Prometheus: metrics collection and alert evaluation (namespace: `25rp19452-niyonkuru`).
- Grafana: dashboards and visualization (datasource pre-configured to Prometheus).
- Loki: log aggregation endpoint (recommended to pair with `promtail` for log shipping).

## Key Configuration

- Prometheus scrapes the helpdesk application via the headless service: `helpdesk-service-headless:5000` (metrics path: `/metrics`).
- Basic alerts are provided in the `prometheus-rules` ConfigMap:
  - `HelpdeskTargetDown`: fires when the helpdesk target reports `up == 0` for 1 minute.
  - `PrometheusInstanceDown`: fires when Prometheus itself is not `up` for 2 minutes.

## How to Access

- Port-forward Prometheus:

```bash
kubectl port-forward svc/prometheus-service 9090:9090 -n 25rp19452-niyonkuru
# then open http://localhost:9090 (Status → Targets, Alerts)
```

- Port-forward Grafana:

```bash
kubectl port-forward svc/grafana-service 3000:3000 -n 25rp19452-niyonkuru
# then open http://localhost:3000 (admin/admin)
```

- Loki listens on `loki-service:3100` in-cluster. To query logs from Grafana, add a panel using Loki datasource pointed at `http://loki-service:3100` (Grafana provisioning already uses the Prometheus datasource; Loki must be added manually in the UI or via provisioning if desired).

## Quick Incident Runbook

1. Check cluster & pods:

```bash
kubectl get pods,svc -n 25rp19452-niyonkuru
```

2. Inspect failing pod:

```bash
kubectl describe pod <pod-name> -n 25rp19452-niyonkuru
kubectl logs <pod-name> -n 25rp19452-niyonkuru
```

3. Check events and recent actions (helpful for mount/PV/PVC issues):

```bash
kubectl get events -n 25rp19452-niyonkuru --sort-by='.lastTimestamp'
kubectl get pv,pvc -n 25rp19452-niyonkuru
kubectl describe pvc helpdesk-pvc -n 25rp19452-niyonkuru
```

4. Redeploy or restart a component if stuck:

```bash
kubectl rollout restart deployment/<deployment-name> -n 25rp19452-niyonkuru
kubectl delete pod <pod-name> -n 25rp19452-niyonkuru
```

## Next Steps / Recommendations

- Deploy `promtail` (DaemonSet) to collect container logs and forward to Loki. I can add a tested promtail manifest.
- Integrate Alertmanager and configure notification receivers (Slack/email/PagerDuty) for critical alerts.
- Push the application Docker image to a registry (Docker Hub or GHCR) so the `helpdesk-app` pods can pull and reach `Running` state; this enables end-to-end monitoring and alerts validation.

---

If you want, I will:
- add a `promtail` DaemonSet and example configuration,
- add Alertmanager with a sample Slack/Email receiver (you'll need to provide endpoint/credentials),
- or push and tag the Docker image and update the manifest so the helpdesk pods come up.
