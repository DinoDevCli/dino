# Roadmap

Shipped: local-first proof engine, export contracts, proof index, Early Access Team Keys, fail-closed leakage scan.

## Developer Mode

`dino --dev` relaxes `EMPTY_SCAN_ROOTS` so local iteration is not blocked by a missing scan root. Other leakage rules still fail. Production (no `--dev`) stays fail-closed.

Further relaxations stay out of the default path.

## Later

- One-time Proof Pack license after Early Access ([`LICENSING.md`](LICENSING.md))
- More dashboard starter kits (Metabase / Grafana) alongside [`examples/superset/`](../examples/superset/)
