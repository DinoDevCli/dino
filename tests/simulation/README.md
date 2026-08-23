# Production-grade E2E simulation

Simulates a real risk/fraud team using Dino on a multi-step Python pipeline.

```
pipeline/extract.py → transform.py → model.py → report.py
                 ↑
            run.py (orchestrator)
```

## One-command demo

```bash
cd tests/simulation
make demo          # seal v1+v2, compare, check golden/
make golden-update # refresh golden/demo_excerpts.json
```

## Pytest suite

```bash
pytest tests/simulation -q
```

Covers: full proof→export→index, HTTP/S3 export, 10× determinism,
Early Access keys (issue/activate/expire), free mode, 10k-row stress, failures.
