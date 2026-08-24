# Superset starter kit — not a Dino product

Dino does not ship a dashboard. This YAML maps `proof_index.json` rows into charts
you can recreate in **your** Apache Superset (or adapt to Metabase / Grafana).

1. Flatten `archive/proof_index.json` → a table (`proofs[]`).
2. Import or recreate the charts in `drift_dashboard.yaml`.

See [`docs/INTEGRATION_DASHBOARDS.md`](../../docs/INTEGRATION_DASHBOARDS.md).
