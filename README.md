
# OpsGPT — Natural-Language Ops Assistant (CLI)

Turn plain English into safe, auditable ops actions using a YAML action map.
Works locally (no keys needed) with a rule-based intent parser. If you set `OPENAI_API_KEY`,
it can optionally call the OpenAI API for better intent parsing.

## Why this is cool
- **Dry-run by default** (prints the *exact* commands it would run).
- **YAML action mapping** so you can tailor commands for any environment.
- **Built-in queries** against sample logs, e.g. *"show failed jobs from last night"*.
- **Audit trail**: every request + decision is logged to `~/.opsgpt/history.log`.

## Quickstart
```bash
cd opsgpt_cli
python -m venv .venv && source .venv/bin/activate  # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
python opsgpt.py "restart the database"
python opsgpt.py "show me failed jobs from last night"
python opsgpt.py --apply "restart batch service"   # actually executes mapped command
```

> ⚠️ For safety, `--apply` is required to execute; otherwise it's dry-run.

## Customize actions
Edit `actions.yaml`:
```yaml
actions:
  restart_database:
    desc: Restart Postgres service
    command: "echo systemctl restart postgresql"     # replace echo with real command
  restart_batch:
    desc: Restart batch scheduler
    command: "echo systemctl restart autosys"
  show_failed_jobs_last_night:
    desc: Query failed jobs from sample logs
    command: "python tools/query_logs.py --since 'yesterday 00:00' --until 'yesterday 23:59' --status FAIL"
```

## Tests
```bash
pytest -q
```
