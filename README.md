# OpsGPT — Natural-Language Ops Assistant (CLI)

Turn plain English into **safe, auditable ops actions** using a YAML action map. Dry-run by default; execute only when you pass `--apply`. Includes a tiny log query tool for incident triage.

## Why it’s useful
- **Safety first:** dry-run prints the exact command before any change.
- **Configurable:** edit `actions.yaml` to fit any environment.
- **Auditable:** every run logs intent + command to `~/.opsgpt/history.log`.
- **Practical:** “show failed jobs from last night” against sample logs.

## Quickstart
```bash
python -m venv .venv && .\.venv\Scripts\activate   # Windows
pip install -r requirements.txt

# Dry-run (safe)
python opsgpt.py "restart the database"
python opsgpt.py "show me failed jobs from last night"

# Execute (only when safe)
python opsgpt.py --apply "restart batch service"
