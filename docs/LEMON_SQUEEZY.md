# Lemon Squeezy setup (Dino Proof Pack)

Payment + license keys for the paid **Proof** pack.

## Store products

Create two products (one-time, license keys enabled):

| Product | Price | Activations | Notes |
|---------|-------|-------------|-------|
| Dino Indie | €49 | 1–3 seats | Variant for solo / small |
| Dino Team | €39 / seat | Match seat count | Or one product with quantity |

In Lemon Squeezy:

1. **Products → New** → enable **Generate license keys**
2. Set activation limit (Indie: `1`, Team: seat count)
3. **Share → Buy** → copy the checkout URL  
   Form: `https://YOURSTORE.lemonsqueezy.com/checkout/buy/VARIANT_ID`

## Website env

In Vercel / `website/.env.local`:

```bash
NEXT_PUBLIC_LEMONSQUEEZY_CHECKOUT_INDIE=https://YOURSTORE.lemonsqueezy.com/checkout/buy/XXXXXXXX
NEXT_PUBLIC_LEMONSQUEEZY_CHECKOUT_TEAM=https://YOURSTORE.lemonsqueezy.com/checkout/buy/YYYYYYYY
```

If unset, Indie/Team CTAs fall back to mailto contact. Lemon.js is already loaded for overlay checkout (`.lemonsqueezy-button`).

## Customer unlock

```bash
pip install "git+https://github.com/DinoDevCli/dino.git@v0.3.0"
dino upgrade --pack proof --key PASTE_LICENSE_KEY_HERE
dino proof doctor
```

The CLI calls Lemon Squeezy `POST /v1/licenses/activate` (no API token required for License API). On success it writes `~/.dino/license.json`.

## Dev / CI without Lemon

```bash
export DINO_OFFLINE_LICENSE_KEYS=dev-key-1
dino upgrade --pack proof --key dev-key-1
```

Or (local only): `DINO_LICENSE_SKIP_REMOTE=1`.

## Checklist before going live

- [ ] Indie + Team products created with license keys
- [ ] Checkout URLs in Vercel env
- [ ] Test purchase → key email → `dino upgrade --pack proof --key …`
- [ ] Confirm activation limit matches seats
