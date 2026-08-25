# License unlock (Proof Pack)

**Current phase: Early Access is open — any team can request a key. No checkout.**

| Pack | Access |
|------|--------|
| Free (scan) | Forever |
| Proof | Free Team Key via [dinodevcli@gmail.com](mailto:dinodevcli@gmail.com) or [GitHub issue](https://github.com/DinoDevCli/dino/issues/new?title=Early%20Access%20Request) |

```bash
pip install "git+https://github.com/DinoDevCli/dino.git@v0.3.2"
dino scan leakage ./tests/e2e/pipe.py          # free forever
dino upgrade --pack proof --key YOUR_TEAM_KEY  # Early Access
dino proof doctor
```

Early Access keys are HMAC-signed (`dinoea.v1.*`) with expiry. Maintainers issue them with:

```bash
dino issue-key --team risk-lab --days 90
```

Engine only — dashboards are external. Website: https://dinodevcli.github.io/dino/

---

## Deferred: Lemon Squeezy (post–Early Access)

Commercial Lemon Squeezy license activation remains in the CLI as a fallback path
after Early Access Team Keys. **Do not advertise checkout or prices during Early Access.**

When pricing returns:

1. Create Lemon products with license keys
2. Customers: `dino upgrade --pack proof --key <lemon_key>`
3. CLI calls `POST /v1/licenses/activate` and writes `~/.dino/license.json`

### Dev / CI without Lemon

Use Early Access keys, or set `DINO_LICENSE_ALLOWLIST` / offline fixtures as documented in tests.
