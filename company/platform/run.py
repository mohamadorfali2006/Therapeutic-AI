"""Therapeutic-AI company runtime — CLI for operating the agent-based company.

Lets leadership plan sprints, dispatch tasks to departments, track status,
record Regulated-AI gates, and emit sprint reports. Persistent state in
`company/platform/state.json` (git-tracked, human-reviewable).

Command groups:
  sprint   plan|list|open|close
  task     add|list|start|done|block|unblock
  gate     run|mark|<task-id>

Requires: Python 3 stdlib only (json, argparse, datetime, pathlib).
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

PLATFORM_DIR = Path(__file__).parent
STATE_FILE = PLATFORM_DIR / "state.json"

DEFAULT_STATE = {
    "company": "Therapeutic-AI",
    "product": "Drug Discovery Engine (DDE)",
    "constitution": "../00-OPERATING-MODEL.md",
    "departments": [
        "leadership", "ai-research", "cdd", "wetlab", "platform-eng",
        "regulated-ai", "regulatory", "data", "business",
    ],
    "sprints": [],
    "next_task_seq": 1,
}


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _load() -> dict:
    if not STATE_FILE.exists():
        return json.loads(json.dumps(DEFAULT_STATE))
    with open(STATE_FILE, encoding="utf-8") as fh:
        return json.load(fh)


def _save(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2)


def _current_sprint(state: dict) -> dict | None:
    for s in state["sprints"]:
        if s["status"] == "active":
            return s
    return None


def _validate_dept(state: dict, dept: str) -> None:
    if dept not in state["departments"]:
        print(f"error: unknown department '{dept}'. Known: {', '.join(state['departments'])}")
        sys.exit(2)


# ---------------------------------------------------------------- sprint ----
def cmd_sprint(args) -> None:
    state = _load()
    action = args.action
    if action == "plan":
        sprint = {
            "id": f"S{len(state['sprints']) + 1}",
            "name": args.name,
            "goal": args.goal,
            "status": "active",
            "created_at": _utcnow(),
            "closed_at": None,
            "tasks": [],
            "gates": [],
        }
        state["sprints"].append(sprint)
        _save(state)
        print(f"planned {sprint['id']} '{sprint['name']}' (active)")
    elif action == "list":
        for s in state["sprints"]:
            n_done = sum(1 for t in s["tasks"] if t["status"] == "done")
            print(f"{s['id']:>4}  {s['status']:<8} {s['name']:<28} done={n_done}/{len(s['tasks'])}")
    elif action == "close":
        sprint = _current_sprint(state)
        if sprint is None:
            print("error: no active sprint")
            sys.exit(2)
        pending = [t for t in sprint["tasks"] if t["status"] != "done"]
        if pending:
            print(f"warning: closing sprint with {len(pending)} task(s) not done")
        sprint["status"] = "closed"
        sprint["closed_at"] = _utcnow()
        _save(state)
        print(f"closed {sprint['id']}")
    else:
        print("error: unknown sprint action")
        sys.exit(2)


# ------------------------------------------------------------------ task ----
def cmd_task(args) -> None:
    state = _load()
    sprint = _current_sprint(state)
    if sprint is None and args.action != "list":
        print("error: no active sprint (use: sprint plan ...)")
        sys.exit(2)
    action = args.action
    if action == "list":
        for s in state["sprints"]:
            if sprint and s["id"] != sprint["id"]:
                continue
            if not s["tasks"]:
                if not sprint:
                    print(f"{s['id']}: (no tasks)")
                continue
            print(f"== {s['id']} {s['name']} ==")
            for t in s["tasks"]:
                owner = t.get("owner", "?")
                print(f"  {t['id']:<8} {t['status']:<9} [{t['dept']:<12}] {t['title']}  -> {owner}")
    elif action == "add":
        _validate_dept(state, args.dept)
        seq = state["next_task_seq"]
        task = {
            "id": f"T{seq}",
            "title": args.title,
            "dept": args.dept,
            "owner": args.owner or f"{args.dept} department",
            "status": "todo",
            "priority": args.priority,
            "outputs": [],
            "evidence": [],
            "created_at": _utcnow(),
        }
        state["next_task_seq"] = seq + 1
        sprint["tasks"].append(task)
        _save(state)
        print(f"added {task['id']} to {sprint['id']} [{args.dept}]: {args.title}")
    elif action == "start":
        _set_task_status(state, sprint, args.id, "in_progress")
        print(f"started {args.id}")
    elif action == "done":
        task = _find_task(sprint, args.id)
        gates = [g for g in sprint["gates"] if g["task_id"] == args.id and g["pass"]]
        if task and task["status"] == "in_progress" and not gates:
            print(f"error: {args.id} not done — Regulated-AI gate must pass first")
            sys.exit(2)
        _set_task_status(state, sprint, args.id, "done")
        print(f"done {args.id} (gated)")
    elif action == "block":
        task = _set_task_status(state, sprint, args.id, "blocked")
        print(f"blocked {args.id}: {args.reason}")
    else:
        print("error: unknown task action")
        sys.exit(2)


def _find_task(sprint, task_id):
    for t in sprint["tasks"]:
        if t["id"] == task_id:
            return t
    return None


def _set_task_status(state, sprint, task_id, status):
    task = _find_task(sprint, task_id)
    if task is None:
        print(f"error: no task {task_id}")
        sys.exit(2)
    task["status"] = status
    _save(state)
    return task


# ------------------------------------------------------------------ gate ----
def cmd_gate(args) -> None:
    state = _load()
    sprint = _current_sprint(state)
    if sprint is None:
        print("error: no active sprint")
        sys.exit(2)
    task = _find_task(sprint, args.id)
    if task is None:
        print(f"error: no task {args.id}")
        sys.exit(2)
    record = {
        "task_id": args.id,
        "pass": bool(args.pass_),
        "verdict": args.verdict or ("approved" if args.pass_ else "rejected"),
        "reviewer": "regulated-ai",
        "timestamp": _utcnow(),
        "evidence": args.evidence or "",
    }
    sprint["gates"].append(record)
    _save(state)
    print(f"gate {'PASS' if args.pass_ else 'FAIL'} recorded for {args.id}")


def cmd_status(args) -> None:
    state = _load()
    sprint = _current_sprint(state) or (state["sprints"][-1] if state["sprints"] else None)
    if sprint is None:
        print("company: no sprints yet")
        return
    print(f"Company    : {state['company']}")
    print(f"Product    : {state['product']}")
    print(f"Sprint     : {sprint['id']} '{sprint['name']}' [{sprint['status']}]")
    print(f"Goal       : {sprint['goal']}")
    print()
    print(f"{'ID':<8}{'status':<11}{'dept':<13}{'title':<36}owner")
    for t in sprint["tasks"]:
        gates = [g for g in sprint["gates"] if g["task_id"] == t["id"]]
        g = ("[gated]" if any(x["pass"] for x in gates)
             else "[FAIL]" if any(not x["pass"] for x in gates) else "")
        print(f"{t['id']:<8}{t['status']:<11}{t['dept']:<13}{t['title']:<36}{t['owner']} {g}")
    blocks = [t for t in sprint["tasks"] if t["status"] == "blocked"]
    if blocks:
        print(f"\nBlockers: {', '.join(t['id'] for t in blocks)}")


def cmd_report(args) -> None:
    state = _load()
    sprint = _current_sprint(state) or (state["sprints"][-1] if state["sprints"] else None)
    if sprint is None:
        print("no sprints")
        return
    lines = [
        "# Company Sprint Report",
        "",
        f"- **Sprint:** {sprint['id']} — {sprint['name']}",
        f"- **Goal:** {sprint['goal']}",
        f"- **Status:** {sprint['status']}",
        f"- **Generated:** {_utcnow()}",
        "",
        "## Tasks",
        "",
    ]
    for t in sprint["tasks"]:
        gates = [g for g in sprint["gates"] if g["task_id"] == t["id"]]
        gate_line = ""
        evidence = []
        if gates:
            latest = gates[-1]
            gate_line = f" - (gate {'PASS' if latest['pass'] else 'FAIL'})"
            if latest.get("evidence"):
                evidence.append(latest["evidence"])
        for g in gates:
            if g.get("verdict") and g["verdict"] not in ("approved", "rejected"):
                evidence.append(g["verdict"])
        ev = "\n".join(f"- {e}" for e in evidence) or "- _no gate evidence recorded_"
        lines.append(f"### {t['id']} - {t['title']} ({t['dept']})")
        lines.append(f"- Status: {t['status']}. Owner: {t['owner']}{gate_line}")
        lines.append("Evidence:")
        lines.append(ev)
        lines.append("")
    out = "\n".join(lines)
    print(out)
    if args.out:
        Path(args.out).write_text(out, encoding="utf-8")
        print(f"\n(wrote {args.out})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Therapeutic-AI company runtime")
    sub = parser.add_subparsers(dest="group", required=True)

    sp = sub.add_parser("sprint")
    sp.add_argument("action", choices=["plan", "list", "close"])
    sp.add_argument("--name", default="Unnamed sprint")
    sp.add_argument("--goal", default="")
    sp.set_defaults(handler=cmd_sprint)

    tk = sub.add_parser("task")
    tk.add_argument("action", choices=["add", "list", "start", "done", "block"])
    tk.add_argument("--id")
    tk.add_argument("--dept")
    tk.add_argument("--title")
    tk.add_argument("--owner")
    tk.add_argument("--priority", default="medium")
    tk.add_argument("--reason", default="")
    tk.set_defaults(handler=cmd_task)

    gt = sub.add_parser("gate")
    gt.add_argument("id")
    gt.add_argument("--pass", dest="pass_", action="store_true")
    gt.add_argument("--verdict")
    gt.add_argument("--evidence")
    gt.set_defaults(handler=cmd_gate)

    st = sub.add_parser("status")
    st.set_defaults(handler=cmd_status)

    rp = sub.add_parser("report")
    rp.add_argument("--out")
    rp.set_defaults(handler=cmd_report)

    args = parser.parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()