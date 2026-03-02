#!/usr/bin/env python3
"""
enrich_cv.py — Add themes, concepts, and collaborators to cv-data.js
via the Claude API, producing cv-data-enriched.js.

Usage (from Timeline-JEL/ root):
    data/cv-data/.venv/bin/python data/cv-data/enrich_cv.py              # full run
    data/cv-data/.venv/bin/python data/cv-data/enrich_cv.py --no-cache   # ignore cache
    data/cv-data/.venv/bin/python data/cv-data/enrich_cv.py --dry-run    # estimate only
    data/cv-data/.venv/bin/python data/cv-data/enrich_cv.py --test       # 5 entries only
    data/cv-data/.venv/bin/python data/cv-data/enrich_cv.py --groups="Documentaries,Film Screenings"

Requires:  ANTHROPIC_API_KEY environment variable
Output:    data/cv-data/cv-data-enriched.js
Cache:     data/cv-data/enrich-cache.json  (saves after every batch; safe to interrupt)
"""

import hashlib, json, os, re, sys, time
from pathlib import Path

import anthropic

# ── Paths ──────────────────────────────────────────────────────────────────────
DIR      = Path(__file__).parent
DATA_IN  = DIR / "cv-data.js"
DATA_OUT = DIR / "cv-data-enriched.js"
CACHE    = DIR / "enrich-cache.json"

# ── Config ─────────────────────────────────────────────────────────────────────
MODEL      = "claude-haiku-4-5-20251001"  # fast + cheap for batch extraction
BATCH_SIZE = 20

# Seed theme vocabulary — encourages consistent terms across the whole CV
SEED_THEMES = [
    "Indigenous digital sovereignty",
    "Indigenous futures",
    "Electronic literature",
    "Computational poetry",
    "AI and creativity",
    "Digital storytelling",
    "Cultural technology",
    "Aboriginal territories in cyberspace",
    "Generative media",
    "Interactive installation",
    "Mobile media",
    "Language revitalization",
    "Game design",
    "Machine learning",
    "New media art",
    "Indigenous pedagogy",
    "Settler colonialism and technology",
    "Research-creation",
    "Computational media",
    "Sound and music",
    "Community engagement",
    "Curatorial practice",
    "Indigenous methodologies",
    "Digital infrastructure",
    "Collaboration and co-creation",
]

# ── Load helpers ───────────────────────────────────────────────────────────────

def load_data():
    text = DATA_IN.read_text(encoding='utf-8')
    start = text.index('[')
    end   = text.rindex(']') + 1
    return json.loads(text[start:end])


def entry_key(e):
    """Stable 16-char hash key for an entry — used as cache key."""
    sig = f"{e.get('group','')}/{e.get('start date','')}/{e.get('headline','')[:80]}"
    return hashlib.md5(sig.encode()).hexdigest()[:16]


def load_cache():
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding='utf-8'))
    return {}


def save_cache(cache):
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding='utf-8')


# ── Prompt ─────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = f"""You are a research metadata analyst examining the academic CV of Jason Lewis, \
an Indigenous (Mohawk/Hawaiian) professor of Computation Arts and media artist at Concordia University.

Your task: extract structured metadata from CV entries.

For each entry return exactly these fields:
  themes        — 1–4 broad research/creative themes (prefer terms from the seed vocabulary below,
                  but add new ones when the work clearly falls outside it)
  concepts      — 2–6 specific keywords, methods, technologies, or named works
  collaborators — named people explicitly mentioned as co-creators, co-authors, co-investigators,
                  or students (for supervision entries: use the student name)

Seed theme vocabulary (use these terms where applicable):
{json.dumps(SEED_THEMES, indent=2)}

Rules:
- Return ONLY a JSON array, one object per entry, in the same order as the input
- Each object must have exactly: {{"themes": [...], "concepts": [...], "collaborators": [...]}}
- Arrays may be empty [] if nothing applies
- For supervision entries (PhD, Masters, etc.): collaborators = [student name],
  themes = inferred research area where possible
- Themes: 3–7 words each. Concepts: 1–4 words each.
- No explanation, no markdown fence — output raw JSON only"""


def build_user_message(batch):
    parts = ["Analyze these CV entries and return a JSON array:\n"]
    for i, e in enumerate(batch):
        year    = e.get('start date', '')[:4]
        group   = e.get('group', '')
        headline = e.get('headline', '').strip()
        desc    = e.get('description', '').strip()
        org     = e.get('org', '').strip()
        program = e.get('program', '').strip()

        line = f"{i+1}. [{group}] {year}"
        if org:
            line += f" | {org}"
        line += f"\n   Headline: {headline}"
        if desc:
            line += f"\n   Description: {desc[:400]}"
        if program:
            line += f"\n   Program: {program}"
        parts.append(line)
    return '\n\n'.join(parts)


# ── API call ───────────────────────────────────────────────────────────────────

def enrich_batch(client, batch):
    """Send one batch to Claude; return list of {themes, concepts, collaborators}."""
    msg = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_user_message(batch)}],
    )
    raw = msg.content[0].text.strip()
    # Strip markdown code fences if the model adds them
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)
    result = json.loads(raw)
    if not isinstance(result, list) or len(result) != len(batch):
        raise ValueError(f"Expected {len(batch)} results, got {len(result)}: {raw[:200]}")
    return result


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    argv = sys.argv[1:]
    no_cache    = '--no-cache' in argv
    dry_run     = '--dry-run'  in argv
    test_mode   = '--test'     in argv

    only_groups = None
    for a in argv:
        if a.startswith('--groups='):
            only_groups = {g.strip() for g in a.split('=', 1)[1].split(',')}

    # Check API key early
    if not dry_run and not os.environ.get('ANTHROPIC_API_KEY'):
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.")
        print("  Add it to ~/.zshrc:  export ANTHROPIC_API_KEY=\"sk-ant-...\"")
        sys.exit(1)

    entries = load_data()
    cache   = {} if no_cache else load_cache()
    client  = anthropic.Anthropic() if not dry_run else None

    # Attach stable keys
    for e in entries:
        e['_key'] = entry_key(e)

    # Filter to entries needing enrichment
    to_enrich = [
        e for e in entries
        if e['_key'] not in cache
        and (only_groups is None or e.get('group') in only_groups)
    ]

    print(f"Loaded {len(entries)} entries | {len(cache)} cached | {len(to_enrich)} to enrich")
    if only_groups:
        print(f"Group filter: {only_groups}")
    if test_mode:
        to_enrich = to_enrich[:5]
        print(f"Test mode: processing first 5 entries only")

    if dry_run:
        total_chars = sum(
            len(e.get('headline', '')) + len(e.get('description', ''))
            for e in to_enrich
        )
        batches = (len(to_enrich) + BATCH_SIZE - 1) // BATCH_SIZE
        print(f"Dry run: {len(to_enrich)} entries | ~{total_chars:,} input chars | {batches} batches")
        print(f"Model: {MODEL}")
        return

    if not to_enrich:
        print("Nothing to do — all entries already cached.")
    else:
        batches = [to_enrich[i:i+BATCH_SIZE] for i in range(0, len(to_enrich), BATCH_SIZE)]
        print(f"Processing {len(batches)} batches (model: {MODEL})\n")

        for i, batch in enumerate(batches):
            groups_in_batch = sorted({e.get('group', '') for e in batch})
            print(f"  Batch {i+1}/{len(batches)} ({len(batch)} entries: {', '.join(groups_in_batch)})", end='', flush=True)
            try:
                results = enrich_batch(client, batch)
                for e, r in zip(batch, results):
                    cache[e['_key']] = {
                        'themes':        [t for t in r.get('themes', [])        if isinstance(t, str)],
                        'concepts':      [c for c in r.get('concepts', [])      if isinstance(c, str)],
                        'collaborators': [c for c in r.get('collaborators', []) if isinstance(c, str)],
                    }
                print(" ✓")
                save_cache(cache)  # save after every batch — safe to interrupt
            except Exception as ex:
                print(f" ✗  ERROR: {ex}")
            # Brief pause between batches
            if i < len(batches) - 1:
                time.sleep(0.3)

    # Merge enrichment into entries and strip temp key
    enriched = []
    enriched_count = 0
    for e in entries:
        key = e.pop('_key')
        hit = cache.get(key, {})
        e['themes']        = hit.get('themes', [])
        e['concepts']      = hit.get('concepts', [])
        e['collaborators'] = hit.get('collaborators', [])
        if e['themes'] or e['concepts'] or e['collaborators']:
            enriched_count += 1
        enriched.append(e)

    # Write output
    DATA_OUT.write_text(
        "// Generated by enrich_cv.py — re-run to refresh enrichment.\n"
        "window.__TIMELINE_DATA__ = "
        + json.dumps(enriched, ensure_ascii=False, indent=2)
        + ";\n",
        encoding='utf-8',
    )
    print(f"\nWrote {len(enriched)} entries ({enriched_count} enriched)  →  {DATA_OUT}")


if __name__ == '__main__':
    main()
