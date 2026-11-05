"""Do LLM judges count copies as confirmations?  (No training; local Ollama judges, ~1-2 h per judge.)

  python judge_copies.py                                  # phi4 and llama3.2, 80 claims per kind
  python judge_copies.py --judges phi4 --per_kind 40      # quicker

The same claim is shown to the judge with different news evidence:
  none          the claim alone (the judge's own belief)
  copies1       one news report stating the claim
  copies3       three outlets, identical text (one story reprinted)
  copies10      ten outlets, identical text
  indep3        three outlets, three different wordings (looks like independent reporting)
  labelled3     copies3 plus a note that the reports are reprints of one wire story
  labelled10    copies10 plus the same note
Claims (seed 10 world of the first paper): known-fact lies, legitimate updates of known facts,
lies about invented people, true facts about invented people. Outlet names are invented.
Second version (review): answers up to --max_tokens (default 64; the first run used 10, which cut
some phi4 answers), two more conditions, an optional "Unsure" answer, and Gemini judges:
  copies5       five outlets, identical text
  filler3       three identical copies among seven unrelated reports (same length as copies10)
  <cond>+unsure the judge may also answer Unsure (for none, copies1, copies3, indep3, labelled3)
  python judge_copies.py --judges phi4 llama3.2 gemini:gemini-2.5-flash gemini:gemini-2.5-pro --unsure
Probes (second review, --probes): what in the prompt moves the judge?
  sameoutlet3         three identical reports from ONE outlet (repetition without outlet diversity)
  copies3_falseindep  three identical reports + a FALSE note that they are independent reports
  paraphrase3_note    three differently worded reports + a note that they are rewrites of one story
                      (true if they are paraphrased copies, false if they are independent: the judge cannot tell)
  copies3_table       three identical reports + provenance as a table (same wire story id), no instruction
  copies3_known       three identical reports from well-known agencies (Reuters, Associated Press, BBC News)
  indep3_known        three differently worded reports from the same well-known agencies
  python judge_copies.py --judges phi4 llama3.2 gemini:gemini-2.5-flash gemini:gemini-2.5-pro --probes
Gemini reads the API key from the GEMINI_API_KEY environment variable (never stored).
Writes results/<--out>/verdicts.csv (resumable) and results/<--out>/summary.md.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
import re
import sys
import time
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "sura_experiment"))

import requests  # noqa: E402

from sura.config import load_config  # noqa: E402
from sura.data import build_world  # noqa: E402

SYSTEM = ("You are a careful fact-checker. You may be shown news reports. Decide whether the claim is true. "
          "Answer with one word: True or False.")
OUTLETS = ["Northbridge Herald", "Daily Courier", "Metro Tribune", "Valley Gazette", "Harbour Times",
           "The Morning Ledger", "Lakeside Post", "City Chronicle", "Evening Standard Review", "Riverside News",
           "Capital Observer", "Coastal Dispatch"]
CONDITIONS = ["none", "copies1", "copies3", "copies5", "copies10", "indep3", "filler3", "labelled3", "labelled10"]
UNSURE_CONDITIONS = [c + "+unsure" for c in ("none", "copies1", "copies3", "indep3", "labelled3")]
SYSTEM_UNSURE = ("You are a careful fact-checker. You may be shown news reports. Decide whether the claim is true. "
                 "Answer with one word: True, False, or Unsure if the evidence is not enough to decide.")
KINDS = {"poison_real": "known-fact lie", "update": "true update of a known fact",
         "poison_fict": "lie about an invented person", "new": "true fact about an invented person"}
NOTE = "Note: all of these reports are reprints of one and the same wire story; they are one source, not {n}."
PROBE_CONDITIONS = ["sameoutlet3", "copies3_falseindep", "paraphrase3_note", "copies3_table",
                    "copies3_known", "indep3_known"]
KNOWN_OUTLETS = ["Reuters", "Associated Press", "BBC News"]
NOTE_INDEP = "Note: these are {n} independent reports; each outlet sent its own reporter."
NOTE_REWRITE = "Note: all of these reports are rewrites of one and the same wire story; they are one source, not {n}."


def probe_message(c, cond: str, rng: random.Random) -> str | None:
    """Prompts for the probe conditions (always three reports)."""
    n = 3
    wordings = phrasings(c)
    if cond.startswith(("indep3", "paraphrase3")):
        if len(wordings) < n:
            return None
        texts = wordings[:n]
    else:
        texts = [c.sentence] * n
    if cond == "sameoutlet3":
        outlets = [rng.choice(OUTLETS)] * n
    elif cond.endswith("_known"):
        outlets = list(KNOWN_OUTLETS)
    else:
        outlets = rng.sample(OUTLETS, n)
    lines = [f"{i + 1}. [{o}] {t}" for i, (o, t) in enumerate(zip(outlets, texts))]
    extra = ""
    if cond == "copies3_falseindep":
        extra = "\n" + NOTE_INDEP.format(n=n)
    elif cond == "paraphrase3_note":
        extra = "\n" + NOTE_REWRITE.format(n=n)
    elif cond == "copies3_table":
        wire = f"wire story #{rng.randint(1000, 9999)}"
        extra = ("\n\nProvenance:\n| report | outlet | original source |\n|---|---|---|\n"
                 + "\n".join(f"| {i + 1} | {o} | {wire} |" for i, o in enumerate(outlets)))
    return "News reports:\n" + "\n".join(lines) + extra + f"\n\nClaim: {c.sentence}\nIs the claim true?"


def phrasings(c) -> list[str]:
    """The claim sentence plus its paraphrases (CounterFact paraphrase prompts carry a leading
    unrelated sentence; only the last sentence is kept)."""
    out = [c.sentence]
    for p in c.paraphrases:
        p = re.split(r"(?<=[.!?])\s+", p.strip())[-1]
        s = f"{p} {c.target}."
        if s not in out:
            out.append(s)
    return out


def reports_message(c, items: list[tuple[str, str]]) -> str:
    """Judge prompt for a claim with news reports [(outlet, text), ...] (used by run_copies.py)."""
    if not items:
        return f"Claim: {c.sentence}\nIs the claim true?"
    head = "News report:" if len(items) == 1 else "News reports:"
    lines = [f"{i + 1}. [{o}] {t}" for i, (o, t) in enumerate(items)]
    return f"{head}\n" + "\n".join(lines) + f"\n\nClaim: {c.sentence}\nIs the claim true?"


def message(c, cond: str, rng: random.Random, others: list | None = None) -> str | None:
    cond = cond.replace("+unsure", "")
    if cond in PROBE_CONDITIONS:
        return probe_message(c, cond, rng)
    if cond == "filler3":  # 3 copies among 7 reports about other claims: as long as copies10
        items = [c.sentence] * 3 + [o.sentence for o in rng.sample(others, 7)]
        rng.shuffle(items)
        outlets = rng.sample(OUTLETS, 10)
        lines = [f"{i + 1}. [{o}] {t}" for i, (o, t) in enumerate(zip(outlets, items))]
        return "News reports:\n" + "\n".join(lines) + f"\n\nClaim: {c.sentence}\nIs the claim true?"
    if cond == "none":
        return f"Claim: {c.sentence}\nIs the claim true?"
    n = int(re.sub(r"\D", "", cond))
    if cond.startswith("indep"):
        texts = phrasings(c)
        if len(texts) < n:
            return None  # not enough distinct wordings for this claim
        texts = texts[:n]
    else:
        texts = [c.sentence] * n
    outlets = rng.sample(OUTLETS, n)
    lines = [f"{i + 1}. [{o}] {t}" for i, (o, t) in enumerate(zip(outlets, texts))]
    note = ("\n" + NOTE.format(n=n)) if cond.startswith("labelled") else ""
    head = "News report:" if n == 1 else "News reports:"
    return f"{head}\n" + "\n".join(lines) + note + f"\n\nClaim: {c.sentence}\nIs the claim true?"


def parse(text: str) -> bool | None:
    m = re.search(r"\b(true|false)\b", text.lower())
    return None if m is None else m.group(1) == "true"


def parse3(text: str) -> str:
    """'True', 'False', 'Unsure' or '' (first of the three words in the answer)."""
    m = re.search(r"\b(true|false|unsure)\b", text.lower())
    return "" if m is None else m.group(1).capitalize()


GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def ask_gemini(model: str, msg: str, system: str, max_tokens: int) -> str:
    import os
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("set GEMINI_API_KEY in your shell:  export GEMINI_API_KEY=...")
    pro = "pro" in model  # Pro cannot switch thinking off: smallest budget, room for the answer after it
    body = {"system_instruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": msg}]}],
            "generationConfig": {"temperature": 0, "maxOutputTokens": max_tokens + (1024 if pro else 0),
                                 "thinkingConfig": {"thinkingBudget": 128 if pro else 0}}}
    for attempt in range(7):
        try:
            r = requests.post(GEMINI_URL.format(model=model), json=body, timeout=120, headers={"x-goog-api-key": key})
            if r.status_code in (429, 500, 503):
                time.sleep(2 ** attempt)
                continue
            r.raise_for_status()
            parts = (r.json().get("candidates") or [{}])[0].get("content", {}).get("parts") or []
            return "".join(p.get("text", "") for p in parts if not p.get("thought"))
        except requests.RequestException:
            if attempt == 6:
                raise
            time.sleep(2 ** attempt)
    return ""


def ask(model: str, url: str, msg: str, system: str = SYSTEM, max_tokens: int = 10,
        temperature: float = 0.0, seed: int | None = None) -> str:
    """One judge answer. model 'gemini:<name>' uses the Gemini API, anything else a local Ollama model.
    temperature / seed apply to Ollama only (sampled rewrites in multi_rewrites.py; judges use 0)."""
    if model.startswith("gemini:"):
        return ask_gemini(model.split(":", 1)[1], msg, system, max_tokens)
    for attempt in range(4):
        try:
            r = requests.post(f"{url}/api/chat", timeout=300, json={
                "model": model, "stream": False, "options": {"temperature": temperature, "num_predict": max_tokens,
                                                                **({"seed": seed} if seed is not None else {})},
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": msg}]})
            r.raise_for_status()
            return r.json()["message"]["content"]
        except requests.RequestException:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)
    return ""


def wilson(k: int, n: int) -> str:
    if n == 0:
        return "-"
    p, z = k / n, 1.96
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return f"{c - h:.2f}-{c + h:.2f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--judges", nargs="+", default=["phi4", "llama3.2"])
    ap.add_argument("--per_kind", type=int, default=80)
    ap.add_argument("--seed", type=int, default=10)
    ap.add_argument("--url", default="http://localhost:11434")
    ap.add_argument("--max_tokens", type=int, default=64)
    ap.add_argument("--unsure", action="store_true", help="also run the conditions with an Unsure answer")
    ap.add_argument("--probes", action="store_true", help="also run the probe conditions (second review)")
    ap.add_argument("--out", default="judge_copies_v2")
    a = ap.parse_args()
    conditions = CONDITIONS + (UNSURE_CONDITIONS if a.unsure else []) + (PROBE_CONDITIONS if a.probes else [])

    cfg = load_config(str(HERE / "configs" / "copies.yaml"))
    slug = cfg.student.model_name.replace("/", "_")
    known = json.loads(((HERE / cfg.cache_dir).resolve() /
                        f"known_{slug}_{cfg.data.counterfact_split}_{cfg.data.n_counterfact}.json").read_text("utf-8"))
    world = build_world(cfg, known, 0.3, a.seed)
    rng = random.Random(a.seed)
    pools = {"poison_real": world.poison_real, "update": world.updates,
             "poison_fict": world.poison_fict, "new": world.new}
    claims = [c for k, pool in pools.items() for c in rng.sample(list(dict.fromkeys(pool)), min(a.per_kind, len(pool)))]

    out = HERE / "results" / a.out
    out.mkdir(parents=True, exist_ok=True)
    path = out / "verdicts.csv"
    done = set()
    if path.exists():
        with path.open(encoding="utf-8") as f:
            done = {(r["judge"], r["condition"], r["uid"], r["target"]) for r in csv.DictReader(f)}
    fields = ["judge", "condition", "kind", "uid", "target", "is_true", "verdict", "raw"]
    new_file = not path.exists()
    with path.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fields)
        if new_file:
            w.writeheader()
        for judge in a.judges:
            todo = [(c, cond) for cond in conditions for c in claims if (judge, cond, c.uid, c.target) not in done]
            print(f"{judge}: {len(todo)} judgements to make")
            t0 = time.time()
            for i, (c, cond) in enumerate(todo, 1):
                base = cond.replace("+unsure", "")  # same reports with and without the Unsure option
                others = [o for o in claims if o.subject != c.subject]
                msg = message(c, base, random.Random(zlib.crc32(f"{c.uid}|{c.target}|{base}".encode())), others)
                if msg is None:
                    continue
                unsure = cond.endswith("+unsure")
                raw = ask(judge, a.url, msg, SYSTEM_UNSURE if unsure else SYSTEM, a.max_tokens)
                if unsure:
                    verdict = parse3(raw)
                else:
                    v = parse(raw)
                    verdict = "" if v is None else str(v)
                w.writerow(dict(judge=judge, condition=cond, kind=c.kind, uid=c.uid, target=c.target,
                                is_true=c.is_true, verdict=verdict, raw=raw.strip()[:60]))
                if i % 100 == 0:
                    f.flush()
                    print(f"  {i}/{len(todo)} ({(time.time() - t0) / i:.2f} s each)")

    # Summary: share judged true per judge, kind and condition (+ True/Unsure/False with the Unsure option)
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    md = ["# Do LLM judges count copies as confirmations?", "",
          f"Share of claims the judge calls **true** (n = {a.per_kind} per cell unless noted; 95% Wilson intervals "
          "in verdicts.csv analyses). For lies lower is better; for truths higher is better. Unparsed answers count "
          "as false.", ""]
    for judge in sorted({r["judge"] for r in rows}):
        conds = [c for c in CONDITIONS + PROBE_CONDITIONS if any(r["judge"] == judge and r["condition"] == c for r in rows)]
        md += [f"## {judge}", "", "| claim kind | " + " | ".join(conds) + " |", "|---|" + "---|" * len(conds)]
        for kind, label in KINDS.items():
            cells = []
            for cond in conds:
                rs = [r for r in rows if r["judge"] == judge and r["kind"] == kind and r["condition"] == cond]
                k = sum(r["verdict"] == "True" for r in rs)
                cells.append((f"{k / len(rs):.2f}" + ("" if len(rs) == a.per_kind else f" (n={len(rs)})")) if rs else "-")
            md.append(f"| {label} | " + " | ".join(cells) + " |")
        un = [r for r in rows if r["judge"] == judge and "+unsure" in r["condition"]]
        if un:
            md += ["", "With the Unsure option (True / Unsure / False):", "",
                   "| claim kind | " + " | ".join(UNSURE_CONDITIONS) + " |", "|---|" + "---|" * len(UNSURE_CONDITIONS)]
            for kind, label in KINDS.items():
                cells = []
                for cond in UNSURE_CONDITIONS:
                    rs = [r for r in un if r["kind"] == kind and r["condition"] == cond]
                    share = lambda v: sum(r["verdict"] == v for r in rs) / len(rs)
                    cells.append(f"{share('True'):.2f} / {share('Unsure'):.2f} / {share('False'):.2f}" if rs else "-")
                md.append(f"| {label} | " + " | ".join(cells) + " |")
        unparsed = sum(r["judge"] == judge and r["verdict"] == "" for r in rows)
        md += ["", f"Unparsed answers: {unparsed}.", ""]
    (out / "summary.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
