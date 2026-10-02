# Shoot or Keep the Ball? A Held-Out Causal Audit of Shot Selection

Code and results for our MIT Sloan Sports Analytics Conference 2027 research paper
submission. Abstract: [`soccer_causal_inference_mit_ssac_27.pdf`](soccer_causal_inference_mit_ssac_27.pdf).

When players shot, did it pay off compared with keeping the ball the way players in the
same situation typically did? We estimate the effect of shooting on the shots taken (ATT)
with a doubly robust estimator, cross-fitted by match, using StatsBomb open event and 360
data. The outcome is the first goal within 15 seconds (+1 scored, −1 conceded, 0 otherwise).
The design was fixed on Euro 2020 and 2024 (102 matches) and run once on World Cup 2022
(64 matches).

## Main result (World Cup 2022, held out)

| | |
|---|---|
| Shots / other decisions | 1,228 / 20,532 |
| Net scoring rate after shots / estimated had they kept the ball | 10.7% / 7.7% |
| **Effect of shooting** (raw gap: 8.4) | **+3.1 pp** (95% CI 0.7 to 5.5) |
| Euro 2020 + 2024 (development) | +1.8 pp (−0.2 to 3.8) |
| Clustering by opponent | −0.3 to 6.4 |
| Hidden-confounding tipping point | Γ ≈ 1.35 |

Full report tables: [`results/run_of_record/full/report/`](results/run_of_record/full/report/).

## Reproduce

StatsBomb data cannot be redistributed, so [`data/`](data/) holds manifests pinning every
file (URL, size, sha256) to
[`hudl/open-data@4b73468`](https://github.com/hudl/open-data/tree/4b73468fc5b0f1950f9f66fada70ad3a4f9327cb).

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt xgboost==3.2.0
export PYTHONPATH=src

python scripts/fetch_data.py --out data/public_statsbomb_causal   # optional: inspect the pinned files
python -m unittest discover -s tests/public_causal                 # tests
python scripts/validate_public_causal.py --output-dir data/public_statsbomb_causal/runs/my-run/manifests
python scripts/run_public_causal.py --phase full --profile submission --device cuda \
  --study-root data/public_statsbomb_causal --run-id my-run \
  --bootstrap-target 200 --bootstrap-max-attempts 300 \
  --simulation-datasets 50 --simulation-bootstrap-target 0 --null-reps 50 \
  --workers 4 --threads 1
```

The runner downloads and checksum-verifies the pinned files itself and writes its own
source manifests, so no manual manifest step is needed.

## Layout

| Path | Contents |
|---|---|
| `src/PublicCausal/`, `scripts/` | pipeline, runner, post-hoc analyses |
| `results/models/` | study notebook |
| `results/run_of_record/` | report of the run of record |
| `results/posthoc_tier12/` | post-hoc analyses |
| `docs/img` | StatsBomb logo |
| `tests/public_causal/` | tests |

## Data and license

<img src="docs/img/statsbomb_logo.png" alt="StatsBomb" width="200">

Data provided by StatsBomb (Hudl) under the
[StatsBomb Public Data User Agreement](https://github.com/hudl/open-data/blob/master/LICENSE.pdf).
Code is MIT licensed ([`LICENSE`](LICENSE)).
