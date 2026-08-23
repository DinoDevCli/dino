# Production-grade E2E simulation

Simulates a real risk/fraud team using Dino on a multi-step Python pipeline.

```
pipeline/extract.py → transform.py → model.py → report.py
                 ↑
            run.py (orchestrator)
```

```bash
pytest tests/simulation -q
# or focused:
pytest tests/simulation/test_production_simulation.py -q
```

Covers: full proof→export→index, HTTP/S3 export, 10× determinism,
Early Access keys (issue/activate/expire), free mode, 10k-row stress, failures.
