
import argparse, datetime as dt, sys, re, json, os
LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "sample_logs", "jobs.log")

def parse_time(s):
    if s.lower().startswith("yesterday"):
        # crude bounds for demo; assumes local tz day offsets
        today = dt.date.today()
        y = today - dt.timedelta(days=1)
        return dt.datetime.combine(y, dt.time.fromisoformat("00:00"))
    try:
        return dt.datetime.fromisoformat(s)
    except Exception:
        # accept "YYYY-mm-dd HH:MM"
        try:
            return dt.datetime.strptime(s, "%Y-%m-%d %H:%M")
        except Exception:
            raise SystemExit("Unsupported time format")

def load():
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            # 2025-08-01 01:23:45 job=NightlyETL status=FAIL
            yield line.strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", required=True)
    ap.add_argument("--until", required=True)
    ap.add_argument("--status", default="FAIL")
    args = ap.parse_args()
    since = parse_time(args.since)
    until = parse_time(args.until) + dt.timedelta(seconds=59)

    rx = re.compile(r"^(?P<ts>[\d\-: ]+) job=(?P<job>[A-Za-z0-9_]+) status=(?P<status>[A-Z]+)")
    out = []
    for ln in load():
        m = rx.match(ln)
        if not m: continue
        ts = dt.datetime.fromisoformat(m.group("ts"))
        if since <= ts <= until and m.group("status") == args.status:
            out.append({"ts": m.group("ts"), "job": m.group("job"), "status": m.group("status")})
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
