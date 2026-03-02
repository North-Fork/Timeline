#!/usr/bin/env python3
"""
enrich_cv.py — Add themes, concepts, and collaborators to cv-data.js
via the Claude API, producing cv-data-enriched.js.

Usage (from Timeline-JEL/ root):
    data/cv-data/.venv/bin/python data/cv-data/enrich_cv.py                        # full run
    data/cv-data/.venv/bin/python data/cv-data/enrich_cv.py --no-cache             # ignore cache
    data/cv-data/.venv/bin/python data/cv-data/enrich_cv.py --dry-run              # estimate only
    data/cv-data/.venv/bin/python data/cv-data/enrich_cv.py --test                 # 5 entries only
    data/cv-data/.venv/bin/python data/cv-data/enrich_cv.py --groups="Books/Chapters,Journal Articles"
    data/cv-data/.venv/bin/python data/cv-data/enrich_cv.py --pdf-dir="/path/to/pdfs"
    data/cv-data/.venv/bin/python data/cv-data/enrich_cv.py --pdf-dir="/path/to/pdfs" --index-pdfs

PDF support:
    --pdf-dir=PATH   Folder of PDFs to match against CV entries (Books/Chapters, Journal Articles, Honors)
    --index-pdfs     Re-scan the PDF folder and rebuild pdf-index.json (run once, or when PDFs change)
    PDF text is cached in data/cv-data/pdf-index.json — matched text is included in the enrichment prompt.

Requires:  ANTHROPIC_API_KEY environment variable
Output:    data/cv-data/cv-data-enriched.js
Cache:     data/cv-data/enrich-cache.json  (saves after every batch; safe to interrupt)
"""

import difflib, hashlib, json, os, re, sys, time
from pathlib import Path

import anthropic

# ── Paths ──────────────────────────────────────────────────────────────────────
DIR       = Path(__file__).parent
DATA_IN   = DIR / "cv-data.js"
DATA_OUT  = DIR / "cv-data-enriched.js"
CACHE     = DIR / "enrich-cache.json"
PDF_INDEX = DIR / "pdf-index.json"

# ── Config ─────────────────────────────────────────────────────────────────────
MODEL      = "claude-haiku-4-5-20251001"
BATCH_SIZE = 20
PDF_CHARS  = 1500   # max chars of PDF text to include per entry (keep prompts under rate limit)
PDF_MATCH_THRESHOLD = 0.35   # minimum similarity score for a PDF match
PDF_BATCH_SIZE = 5   # smaller batches when PDF text is included

# Groups where PDFs are likely to exist
PDF_GROUPS = {'Books/Chapters', 'Journal Articles', 'Honors'}

# Seed theme vocabulary
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

# ── Data helpers ───────────────────────────────────────────────────────────────

def load_data():
    text = DATA_IN.read_text(encoding='utf-8')
    start = text.index('[')
    end   = text.rindex(']') + 1
    return json.loads(text[start:end])


def entry_key(e):
    sig = f"{e.get('group','')}/{e.get('start date','')}/{e.get('headline','')[:80]}"
    return hashlib.md5(sig.encode()).hexdigest()[:16]


def load_cache():
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding='utf-8'))
    return {}


def save_cache(cache):
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding='utf-8')


# ── PDF helpers ────────────────────────────────────────────────────────────────

def normalize_for_match(s):
    """Lowercase, strip punctuation and common stop words — used for fuzzy matching."""
    s = s.lower()
    s = re.sub(r'[^\w\s]', ' ', s)
    stop = {'a','an','the','and','or','of','in','on','at','to','for','with',
            'by','from','is','as','into','that','this','it','its'}
    words = [w for w in s.split() if w not in stop and len(w) > 1]
    return ' '.join(words)


def extract_pdf_text(pdf_path):
    """Extract first PDF_CHARS of text from a PDF file."""
    try:
        import pypdf
        reader = pypdf.PdfReader(str(pdf_path))
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
            if len(text) >= PDF_CHARS:
                break
        return text[:PDF_CHARS].strip()
    except Exception as e:
        return f"[PDF extraction error: {e}]"


def build_pdf_index(pdf_dir):
    """Scan pdf_dir, extract text from all PDFs, save to pdf-index.json."""
    pdf_dir = Path(pdf_dir)
    pdfs = list(pdf_dir.glob('**/*.pdf')) + list(pdf_dir.glob('**/*.PDF'))
    print(f"Indexing {len(pdfs)} PDFs in {pdf_dir} ...")
    index = {}
    for i, pdf in enumerate(pdfs):
        print(f"  [{i+1}/{len(pdfs)}] {pdf.name}", end='', flush=True)
        text = extract_pdf_text(pdf)
        index[pdf.name] = {
            'path':      str(pdf),
            'norm_name': normalize_for_match(pdf.stem),
            'text':      text,
        }
        print(f" ({len(text)} chars)")
    PDF_INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Saved PDF index → {PDF_INDEX}")
    return index


def load_pdf_index():
    if PDF_INDEX.exists():
        return json.loads(PDF_INDEX.read_text(encoding='utf-8'))
    return {}


def find_pdf_match(headline, pdf_index):
    """Fuzzy-match a CV headline against indexed PDF filenames. Returns text or None."""
    if not pdf_index:
        return None
    norm_headline = normalize_for_match(headline)
    if not norm_headline:
        return None

    best_score = 0
    best_text  = None
    best_name  = None

    for name, info in pdf_index.items():
        score = difflib.SequenceMatcher(
            None, norm_headline, info['norm_name']
        ).ratio()
        if score > best_score:
            best_score = score
            best_text  = info['text']
            best_name  = name

    if best_score >= PDF_MATCH_THRESHOLD:
        return best_name, best_text
    return None, None


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


def build_user_message(batch, pdf_index):
    parts = ["Analyze these CV entries and return a JSON array:\n"]
    for i, e in enumerate(batch):
        year     = e.get('start date', '')[:4]
        group    = e.get('group', '')
        headline = e.get('headline', '').strip()
        desc     = e.get('description', '').strip()
        org      = e.get('org', '').strip()
        program  = e.get('program', '').strip()

        line = f"{i+1}. [{group}] {year}"
        if org:
            line += f" | {org}"
        line += f"\n   Headline: {headline}"
        if desc:
            line += f"\n   Description: {desc[:400]}"
        if program:
            line += f"\n   Program: {program}"

        # Attach PDF text if available for this group
        if pdf_index and group in PDF_GROUPS:
            pdf_name, pdf_text = find_pdf_match(headline, pdf_index)
            if pdf_text:
                line += f"\n   PDF ({pdf_name}): {pdf_text[:PDF_CHARS]}"

        parts.append(line)
    return '\n\n'.join(parts)


# ── API call ───────────────────────────────────────────────────────────────────

def enrich_batch(client, batch, pdf_index, retries=3):
    """Call Claude API with retry on rate-limit errors."""
    for attempt in range(retries):
        try:
            msg = client.messages.create(
                model=MODEL,
                max_tokens=2048,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": build_user_message(batch, pdf_index)}],
            )
            raw = msg.content[0].text.strip()
            raw = re.sub(r'^```(?:json)?\s*', '', raw)
            raw = re.sub(r'\s*```$', '', raw)
            result = json.loads(raw)
            if not isinstance(result, list) or len(result) != len(batch):
                raise ValueError(f"Expected {len(batch)} results, got {len(result)}: {raw[:200]}")
            return result
        except Exception as ex:
            if '429' in str(ex) and attempt < retries - 1:
                wait = 65 * (attempt + 1)
                print(f"\n    Rate limit — waiting {wait}s before retry {attempt+2}/{retries}...", end='', flush=True)
                time.sleep(wait)
            else:
                raise


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    argv = sys.argv[1:]
    no_cache    = '--no-cache'    in argv
    dry_run     = '--dry-run'     in argv
    test_mode   = '--test'        in argv
    do_index    = '--index-pdfs'  in argv

    only_groups = None
    pdf_dir     = None
    for a in argv:
        if a.startswith('--groups='):
            only_groups = {g.strip() for g in a.split('=', 1)[1].split(',')}
        if a.startswith('--pdf-dir='):
            pdf_dir = Path(a.split('=', 1)[1])

    # Check API key early (not needed for --index-pdfs only)
    if not dry_run and not do_index and not os.environ.get('ANTHROPIC_API_KEY'):
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.")
        print("  Add it to ~/.zshrc:  export ANTHROPIC_API_KEY=\"sk-ant-...\"")
        sys.exit(1)

    # Build or load PDF index
    pdf_index = {}
    if pdf_dir:
        if not pdf_dir.is_dir():
            print(f"ERROR: --pdf-dir path not found: {pdf_dir}")
            sys.exit(1)
        if do_index or not PDF_INDEX.exists():
            pdf_index = build_pdf_index(pdf_dir)
        else:
            pdf_index = load_pdf_index()
            print(f"Loaded PDF index: {len(pdf_index)} files (use --index-pdfs to rebuild)")
        if do_index and dry_run:
            return  # just indexing, nothing more to do

    entries = load_data()
    cache   = {} if no_cache else load_cache()
    client  = anthropic.Anthropic() if not dry_run else None

    for e in entries:
        e['_key'] = entry_key(e)

    to_enrich = [
        e for e in entries
        if e['_key'] not in cache
        and (only_groups is None or e.get('group') in only_groups)
    ]

    pdf_matches = 0
    if pdf_index:
        for e in to_enrich:
            if e.get('group') in PDF_GROUPS:
                _, txt = find_pdf_match(e.get('headline', ''), pdf_index)
                if txt:
                    pdf_matches += 1

    print(f"Loaded {len(entries)} entries | {len(cache)} cached | {len(to_enrich)} to enrich")
    if pdf_index:
        print(f"PDF index: {len(pdf_index)} files | {pdf_matches} matches for pending entries")
    if only_groups:
        print(f"Group filter: {only_groups}")
    if test_mode:
        to_enrich = to_enrich[:5]
        print(f"Test mode: first 5 entries only")

    if dry_run:
        total_chars = sum(
            len(e.get('headline', '')) + len(e.get('description', ''))
            for e in to_enrich
        )
        batches = (len(to_enrich) + BATCH_SIZE - 1) // BATCH_SIZE
        print(f"Dry run: {len(to_enrich)} entries | ~{total_chars:,} chars | {batches} batches")
        print(f"Model: {MODEL}")
        return

    if not to_enrich:
        print("Nothing to do — all entries already cached.")
    else:
        # Use smaller batches for entries that will have PDF text attached
        def batch_size_for(e):
            if pdf_index and e.get('group') in PDF_GROUPS:
                _, txt = find_pdf_match(e.get('headline', ''), pdf_index)
                return PDF_BATCH_SIZE if txt else BATCH_SIZE
            return BATCH_SIZE

        batches = []
        i = 0
        while i < len(to_enrich):
            bs = batch_size_for(to_enrich[i])
            batches.append(to_enrich[i:i+bs])
            i += bs

        print(f"Processing {len(batches)} batches (model: {MODEL})\n")

        for i, batch in enumerate(batches):
            groups_in_batch = sorted({e.get('group', '') for e in batch})
            print(f"  Batch {i+1}/{len(batches)} ({len(batch)} entries: {', '.join(groups_in_batch)})", end='', flush=True)
            try:
                results = enrich_batch(client, batch, pdf_index)
                for e, r in zip(batch, results):
                    cache[e['_key']] = {
                        'themes':        [t for t in r.get('themes', [])        if isinstance(t, str)],
                        'concepts':      [c for c in r.get('concepts', [])      if isinstance(c, str)],
                        'collaborators': [c for c in r.get('collaborators', []) if isinstance(c, str)],
                    }
                print(" ✓")
                save_cache(cache)
            except Exception as ex:
                print(f" ✗  ERROR: {ex}")
            if i < len(batches) - 1:
                pause = 8 if len(batch) <= PDF_BATCH_SIZE else 0.3
                time.sleep(pause)

    # Merge enrichment into output
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
