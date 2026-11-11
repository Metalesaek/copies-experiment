"""Real carriers for the learning stream: every report is a REAL news article with the claim inserted,
and the REAL detectors decide which chain it belongs to (review: "the stream draws detector errors at
measured rates instead of running the detection pipeline on real texts").

  python real_carriers.py --prepare      # once, CPU, ~15-30 min: CC-News texts + spaCy facts -> data/carriers.jsonl
  python run_copies.py --set copies.carriers=real --attacks copy paraphrase adaptive collusion \
      --systems chains_k judge_all judge_chains --seeds 10 --tag real_v1

Carriers (all texts boilerplate-stripped as in check_copies.py --strip, first 2,500 characters):
  true claim, one chain     a real CC-News copy chain (origin + its real reprints by other outlets) whose
                            size is drawn from the measured chain sizes (size 1 = an article nobody copied)
  true claim, 2-3 chains    chains 1 and 2: the two articles of a same-event pair that BOTH authors labelled
                            independent (data/labels_indep_set.csv), each with its real reprints if it has any;
                            chain 3: an unrelated article
  lie, copy attack          a real chain with at least attack_copies + 1 outlets (real reprints, real edits)
  lie, paraphrase/adaptive  a real phi4 copy network (origin + 10 rewrites; adaptive = with invented details),
                            data/multi_rewrites.jsonl
  lie, collusion            an independent same-event pair: two outlets that do not copy each other
The claim sentence is inserted after the first line of every carrier: copies of a chain repeat their
origin's wording; rewrites (paraphrase, adaptive) use another wording of the claim.

Detection (no probabilities): reports of one claim are processed in time order. A report joins the chain
of the first earlier report it matches, else it starts a new chain:
  text            5-gram Jaccard >= copies.jaccard_threshold (0.6)
  text+novelty    text, or entity novelty < copies.novelty_threshold (0.4) against the earlier report
DETECTOR_STATS holds what the detector did in the last stream built (printed and saved by run_copies.py).
data/carriers.jsonl contains article text: do not publish it.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import random
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
CARRIERS = HERE / "data" / "carriers.jsonl"
MAX_CHARS = 2500
PER_SIZE = 300          # chains kept per chain size (all chains of attack size are kept)
N_SINGLES = 3000        # articles that nobody copied
DETECTOR_STATS: dict = {}


# ---------------------------------------------------------------- prepare (once, needs CC-News + spaCy)

def prepare(attack_size: int, seed: int = 0):
    import pandas as pd
    from check_copies import boilerplate_lines, load, strip
    from novelty_test import spacy_facts

    rng = random.Random(seed)
    chains = pd.read_csv(HERE / "data" / "copy_chains_strip.csv")
    chains["day"] = pd.to_datetime(chains.date, errors="coerce")
    size = chains.groupby("chain").domain.nunique()
    keep = []
    for s, ids in size.groupby(size):
        ids = sorted(ids.index)
        keep += ids if s >= attack_size else rng.sample(ids, min(PER_SIZE, len(ids)))
    keep = set(keep)
    pairs = pd.read_csv(HERE / "data" / "labels_indep_set.csv")
    pairs = pairs[(pairs.label_author1 == "independent") & (pairs.label_author2 == "independent")]
    nets = [json.loads(x) for x in (HERE / "data" / "multi_rewrites.jsonl").read_text(encoding="utf-8").splitlines()]
    chain_of = dict(zip(chains.url, chains.chain))

    df = load(None, 0)
    lines = boilerplate_lines(df.sample(min(200_000, len(df)), random_state=0).text)
    want = set(chains[chains.chain.isin(keep)].url) | set(pairs.url_a) | set(pairs.url_b) | {r["url"] for r in nets}
    for u in list(set(pairs.url_a) | set(pairs.url_b)):   # reprints of the pair articles
        if u in chain_of:
            want |= set(chains[chains.chain == chain_of[u]].url)
    in_chains = set(chains.url)
    singles = [u for u in df.url.sample(frac=1.0, random_state=seed) if u not in in_chains][:N_SINGLES]
    want |= set(singles)
    text = {}
    for u, t in zip(df.url, df.text):
        if u in want and u not in text:
            text[u] = strip(t, lines)[:MAX_CHARS]
    print(f"{len(text)} carrier articles")

    def ordered(chain_id):   # origin first: earliest date, then the order in the file
        c = chains[chains.chain == chain_id].sort_values("day", kind="stable").drop_duplicates("domain")
        return [u for u in c.url if u in text]

    records = []
    for cid in sorted(keep):
        urls = ordered(cid)
        if len(urls) >= 2:
            records.append(dict(kind="chain", id=str(cid), texts=[text[u] for u in urls]))
    for u in singles:
        if u in text:
            records.append(dict(kind="single", id=u, texts=[text[u]]))
    for p in pairs.itertuples():
        if p.url_a in text and p.url_b in text:
            side = []
            for u in (p.url_a, p.url_b):
                rest = [v for v in ordered(chain_of[u]) if v != u] if u in chain_of else []
                side.append([text[u]] + [text[v] for v in rest])
            records.append(dict(kind="pair", id=str(p.item), texts=side[0], texts_b=side[1]))
    for attack in ("paraphrase", "adaptive"):
        for u in sorted({r["url"] for r in nets if r["attack"] == attack}):
            cs = sorted((r for r in nets if r["attack"] == attack and r["url"] == u), key=lambda r: int(r["copy"]))
            if u in text:
                records.append(dict(kind=f"net_{attack}", id=u, texts=[text[u]] + [r["text"][:MAX_CHARS] for r in cs]))

    all_texts = sorted({t for r in records for t in r["texts"] + r.get("texts_b", [])})
    facts = dict(zip(all_texts, spacy_facts(all_texts)))
    with CARRIERS.open("w", encoding="utf-8") as f:
        for r in records:
            r["facts"] = [sorted(facts[t]) for t in r["texts"]]
            if "texts_b" in r:
                r["facts_b"] = [sorted(facts[t]) for t in r["texts_b"]]
            f.write(json.dumps(r) + "\n")
    count = defaultdict(int)
    for r in records:
        count[r["kind"]] += 1
    print(f"wrote {CARRIERS}: {dict(count)}")


# ---------------------------------------------------------------- stream with real carriers

@dataclasses.dataclass(frozen=True)
class Article:
    body: str
    facts: frozenset


class Pool:
    def __init__(self, path: Path):
        self.by_size, self.singles, self.pairs, self.nets = defaultdict(list), [], [], defaultdict(list)
        for line in path.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            arts = [Article(t, frozenset(f)) for t, f in zip(r["texts"], r["facts"])]
            if r["kind"] == "chain":
                self.by_size[len(arts)].append(arts)
            elif r["kind"] == "single":
                self.singles.append(arts)
            elif r["kind"] == "pair":
                self.pairs.append((arts, [Article(t, frozenset(f)) for t, f in zip(r["texts_b"], r["facts_b"])]))
            else:
                self.nets[r["kind"][4:]].append(arts)
        self.sizes = sorted(self.by_size)

    def chain(self, n: int, rng) -> list[Article]:
        """A real chain with n articles (the closest available size)."""
        if n <= 1:
            return rng.choice(self.singles)
        s = min(self.sizes, key=lambda x: (abs(x - n), -x))
        return rng.choice(self.by_size[s])

    def big_chain(self, n: int, rng) -> list[Article]:
        big = [c for s in self.sizes if s >= n for c in self.by_size[s]]
        if not big:
            raise SystemExit(f"no real chain with {n} outlets in {CARRIERS}")
        return rng.choice(big)[:n]


_POOL: Pool | None = None
_CLAIM_FACTS: dict[str, frozenset] = {}


def pool(C) -> Pool:
    global _POOL
    if _POOL is None:
        _POOL = Pool(HERE / getattr(C, "carrier_file", "data/carriers.jsonl"))
    return _POOL


def claim_facts(sentence: str) -> frozenset:
    if sentence not in _CLAIM_FACTS:
        from novelty_test import spacy_facts
        _CLAIM_FACTS[sentence] = frozenset(spacy_facts([sentence])[0])
    return _CLAIM_FACTS[sentence]


def insert(a: Article, sentence: str) -> Article:
    head, _, tail = a.body.partition("\n")
    return Article(f"{head}\n{sentence}\n{tail}" if tail else f"{head} {sentence}", a.facts | claim_facts(sentence))


def detect(reports, C) -> list:
    """Assign seen_chain with the real detectors, claim by claim, in stream (time) order."""
    from measure_detector import jaccard
    from novelty_test import novelty
    use_novelty = getattr(C, "detector", "text+novelty") == "text+novelty"
    j_t, n_t = getattr(C, "jaccard_threshold", 0.6), getattr(C, "novelty_threshold", 0.4)
    earlier = defaultdict(list)          # claim -> [(article, seen_chain, true_chain)]
    st = defaultdict(int)
    out = []
    for r in reports:                    # already sorted by time
        k = (r.claim.uid, r.claim.target)
        seen = None
        for a, s, true in earlier[k]:
            if jaccard(a.body, r.article.body) >= j_t:
                seen, how = s, "text"
                break
        if seen is None and use_novelty:
            for a, s, true in earlier[k]:
                if novelty(a.facts, r.article.facts) < n_t:
                    seen, how = s, "novelty"
                    break
        lie = "lie" if not r.claim.is_true else "true"
        if seen is None:
            seen = f"{r.chain}|seen{len({s for _, s, _ in earlier[k]})}"
            if r.is_copy:
                st[f"{lie}_copies_missed"] += 1
        else:
            linked_true = {t for _, s2, t in earlier[k] if s2 == seen}
            if r.chain in linked_true:
                st[f"{lie}_copies_linked_{how}"] += 1 if r.is_copy else 0
            else:
                st[f"{lie}_independent_merged_{how}"] += 1
        if r.is_copy:
            st[f"{lie}_copies"] += 1
        else:
            st[f"{lie}_chain_origins"] += 1
        earlier[k].append((r.article, seen, r.chain))
        out.append(dataclasses.replace(r, seen_chain=seen))
    DETECTOR_STATS.clear()
    DETECTOR_STATS.update(st)
    return out


def build_reports_real(world, C, sample_size, attack: str, seed: int) -> list:
    from copies_world import Report
    from judge_copies import OUTLETS, phrasings
    P = pool(C)
    rng = random.Random(seed * 1009 + 17)
    car_rng = random.Random(seed * 1039 + 13)   # separate stream: carriers do not change the times
    out_rng = random.Random(seed * 1013 + 5)
    n_chains, w_chains = zip(*[(int(k), float(v)) for k, v in C.truth_chains])
    claims = list(dict.fromkeys(world.new + world.updates + world.poison_fict + world.poison_real))
    reports = []
    for c in claims:
        start = rng.uniform(0, C.horizon_days)
        if c.is_true:
            n = rng.choices(n_chains, w_chains)[0]
            if n == 1:
                chains = [(P.chain(sample_size(rng), car_rng), False)]
            else:
                a, b = car_rng.choice(P.pairs)
                chains = [(a, False), (b, False)] + [(car_rng.choice(P.singles), False) for _ in range(n - 2)]
        elif attack == "copy":
            chains = [(P.big_chain(C.attack_copies + 1, car_rng), False)]
        elif attack in ("paraphrase", "adaptive"):
            chains = [(car_rng.choice(P.nets[attack])[:C.attack_copies + 1], True)]
        elif attack == "collusion":
            a, b = car_rng.choice(P.pairs)
            chains = [([a[0]], False), ([b[0]], False)] + \
                     [(car_rng.choice(P.singles), False) for _ in range(C.collusion_chains - 2)]
        else:
            raise ValueError(f"unknown attack {attack}")
        words = phrasings(c)
        for k, (arts, reworded) in enumerate(chains):
            cid = f"{c.uid}|{c.target}|{k}"
            t0 = start + rng.uniform(0, C.chain_spread_days)
            text = words[k % len(words)]
            reports.append(Report(c, cid, cid, False, t0, out_rng.choice(OUTLETS), text, insert(arts[0], text)))
            for j, art in enumerate(arts[1:]):
                w = words[(j + 1) % len(words)] if reworded else text
                reports.append(Report(c, cid, cid, True, t0 + rng.uniform(0, C.copy_spread_days),
                                      out_rng.choice(OUTLETS), w, insert(art, w)))
    reports.sort(key=lambda r: r.time)
    return detect(reports, C)


def stats_line(stats: dict) -> str:
    def share(a, b):
        return f"{stats.get(a, 0)}/{stats.get(b, 0)}"
    linked = lambda x: stats.get(f"{x}_copies_linked_text", 0) + stats.get(f"{x}_copies_linked_novelty", 0)
    merged = lambda x: stats.get(f"{x}_independent_merged_text", 0) + stats.get(f"{x}_independent_merged_novelty", 0)
    return (f"detector: lie copies linked {linked('lie')}/{stats.get('lie_copies', 0)}, "
            f"true copies linked {linked('true')}/{stats.get('true_copies', 0)}, "
            f"independent chains merged: true {merged('true')}/{stats.get('true_chain_origins', 0)}, "
            f"lie {merged('lie')}/{stats.get('lie_chain_origins', 0)} (missed lie copies {share('lie_copies_missed', 'lie_copies')})")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prepare", action="store_true")
    ap.add_argument("--attack_size", type=int, default=11, help="outlets needed for a copy-attack chain")
    a = ap.parse_args()
    if a.prepare:
        prepare(a.attack_size)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
