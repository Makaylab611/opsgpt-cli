
import os, sys, argparse, yaml, time, subprocess, shlex, json, re, pathlib

HISTORY = os.path.expanduser("~/.opsgpt/history.log")

def log_event(payload):
    os.makedirs(os.path.dirname(HISTORY), exist_ok=True)
    with open(HISTORY, "a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": time.time(), **payload}) + "\n")

# Simple intent parser (no network). Optionally, future: call LLM if OPENAI_API_KEY is set.
def parse_intent(text):
    t = text.lower().strip()
    if "restart" in t and ("db" in t or "database" in t or "postgres" in t):
        return "restart_database"
    if "restart" in t and ("batch" in t or "autosys" in t or "scheduler" in t):
        return "restart_batch"
    if ("failed" in t and "job" in t) and ("yesterday" in t or "last night" in t):
        return "show_failed_jobs_last_night"
    # fallback: echo the string as a "command" to show safety
    return None

def load_actions(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["actions"]

def run_command(cmd, apply=False):
    if not apply:
        print(f"[dry-run] {cmd}")
        return 0, ""
    # Real execution
    try:
        res = subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True)
        return res.returncode, (res.stdout or "") + (res.stderr or "")
    except Exception as e:
        return 1, str(e)

def main():
    ap = argparse.ArgumentParser(description="OpsGPT CLI")
    ap.add_argument("query", help="natural-language request in quotes")
    ap.add_argument("--actions", default="actions.yaml")
    ap.add_argument("--apply", action="store_true", help="execute instead of dry-run")
    args = ap.parse_args()

    actions = load_actions(args.actions)
    intent = parse_intent(args.query)
    if not intent:
        print("Could not map your request to a known action. Edit actions.yaml to add one.")
        log_event({"query": args.query, "intent": None, "status": "unmapped"})
        sys.exit(2)

    action = actions.get(intent)
    if not action:
        print(f"Intent '{intent}' is not defined in actions.yaml")
        log_event({"query": args.query, "intent": intent, "status": "missing_action"})
        sys.exit(2)

    rc, out = run_command(action["command"], apply=args.apply)
    print(out.strip())
    log_event({"query": args.query, "intent": intent, "cmd": action["command"], "apply": args.apply, "rc": rc})

if __name__ == "__main__":
    main()
