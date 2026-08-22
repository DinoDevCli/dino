# Examples

## HAR

```bash
dino har canonicalize 'https://cdn.example.com/users/99?utm_source=x' --method POST
# POST:https://cdn.example.com/users/{id}

dino har noise 'https://foo.cloudfront.net/app.js'
# is_noise true (cdn + static)
```

## Brain graph verify

```bash
dino brain analyze ./dino/common
dino brain verify --repo ./dino
```

Same repo, same `overall_quality_score` and `graph_hash` on every run.

## SealRun capsule

```bash
dino sealrun run execute --output-dir ./out/exec --command echo ok
dino sealrun run replay --capsule ./out/exec/capsule.json --output-dir ./out/exec
dino sealrun run doctor --output-dir ./out/doctor
```

`./out/doctor/result.json` is overwritten in place. No `run_0001` directories.

## Leakage

```bash
echo 'from intelligence.alpha_evolution.engine_v13.economics import x' > /tmp/leak.py
dino alpha leakage-scan /tmp/leak.py
# exit 1, rule LEAKY_IMPORT
```

## Compliance

```bash
dino compliance sbom --root . --output /tmp/sbom.json
dino compliance dashboard /tmp/dash --root ./dino
```
