"""Download the exact StatsBomb open-data files used by the study and verify them.

The raw files are not redistributed here (StatsBomb Public Data User Agreement,
clause 1.2.1). Instead, data/*_data_manifest.json pin every file to upstream
commit 4b73468fc5b0f1950f9f66fada70ad3a4f9327cb with its byte count and sha256.

Usage:
    python scripts/fetch_data.py --out data/public_statsbomb_causal
    python scripts/fetch_data.py --out data/public_statsbomb_causal --cohort development

Files land at <out>/<path> (e.g. <out>/raw/data/three-sixty/3857254.json), the
layout expected by src/PublicCausal/data.py. Existing files with the right hash
are kept; any mismatch stops the script.
"""
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def sha256(payload):
    return hashlib.sha256(payload).hexdigest()


def fetch(url, retries=3):
    for attempt in range(retries):
        try:
            request = Request(url, headers={"User-Agent": "public360-causal-research/1"})
            with urlopen(request, timeout=90) as response:
                return response.read()
        except OSError as exc:
            if attempt == retries - 1:
                raise
            print(f"retry {attempt + 1} {url}: {exc}", file=sys.stderr)
            time.sleep(2 ** attempt)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--cohort", choices=("development", "confirmation", "all"), default="all")
    args = parser.parse_args()
    cohorts = ["development", "confirmation"] if args.cohort == "all" else [args.cohort]
    entries = {}
    for cohort in cohorts:
        manifest = json.loads((ROOT / "data" / f"{cohort}_data_manifest.json").read_text())
        for row in manifest["files"]:
            entries[row["path"]] = row
    done = 0
    for path, row in sorted(entries.items()):
        target = args.out / path
        if target.exists() and sha256(target.read_bytes()) == row["sha256"]:
            done += 1
            continue
        payload = fetch(row["url"])
        if len(payload) != row["bytes"] or sha256(payload) != row["sha256"]:
            sys.exit(f"checksum mismatch for {row['url']}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        done += 1
        print(f"[{done}/{len(entries)}] {path}")
    print(f"verified {done} files under {args.out}")


if __name__ == "__main__":
    main()
