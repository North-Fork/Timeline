#!/usr/bin/env python3
"""
Fetch Jason Edward Lewis's published CV Google Doc and convert to cv-data.js.

Usage:
    python3 fetch_cv_from_gdoc.py              # uses hardcoded default URL
    python3 fetch_cv_from_gdoc.py <url>        # use a different published-doc URL

Writes cv-data.js alongside this script.
Requires: pip3 install beautifulsoup4
"""
import json, re, sys
from datetime import date
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("beautifulsoup4 not found — install with:  pip3 install beautifulsoup4")

# ── Default Google Doc URL ───────────────────────────────────────────────────
DEFAULT_URL = (
    "https://docs.google.com/document/d/e/"
    "2PACX-1vRIeY4A3fbqJj29GP2yT0FpJkoPOLiLVqaOqPuIUDuJOjXLGwM0jEuS2WGb_daBLY8dCEuooURhz-5D"
    "/pub"
)

TODAY = date.today()

# ── Section heading text (lowercase) → internal group name ──────────────────
# The Google Doc uses <h1> for top-level and <h2> for sub-sections.
# Normalised to lowercase with extra whitespace collapsed.
SECTION_MAP = {
    # Top-level structured sections
    'employment history':                                               'Employment',
    'education':                                                        'Education',
    'honors and awards':                                                'Honors',

    # Research / Creation sub-sections
    'books':                                                            'Books',
    'book chapters':                                                    'Book Chapters',
    'journal articles & conference proceedings (refereed)':             'Journal Articles',
    'journal articles & conference proceedings':                        'Journal Articles',
    'journal articles and conference proceedings':                      'Journal Articles',
    'conference / symposia presentations (refereed)':                   'Conference Presentations',
    'conference / symposia presentations':                              'Conference Presentations',
    'keynote, plenary, and special guest speaker':                      'Keynotes',
    'invited publications':                                             'Invited Publications',
    'invited lectures / artist talks / panels':                         'Invited Lectures',
    "artist's books and exhibition publications":                       "Artist's Books",
    'symposium, workshop, and lecture series organizer or lead':        'Symposia Organized',
    'promotion review / peer reviewer / jury member / expert assessor': 'Service',
    'documentaries':                                                    'Documentaries',
    'websites':                                                         'Websites',
    'residencies':                                                      'Residencies',
    'residency organizer':                                              'Residency Organizer',
    'academic review & textbook inclusion':                             'Academic Reviews',
    'op-ed':                                                            'Op-Ed',
    'press coverage / interviews / documentaries':                      'Press Coverage',
    'policy papers, governmental presentations, reviews & consultations': 'Policy & Reports',

    # Creative works sub-sections
    'exhibitions - solo':   'Solo Exhibitions',
    'exhibitions - group':  'Group Exhibitions',
    'film screenings':      'Film Screenings',
    'commissions':          'Commissions',
    'poetry publication & performances': 'Poetry',
    'curatorial':           'Curatorial',
    'visiting artist & master classes':  'Visiting Artist',
    'producer / executive producer':     'Productions',
    'major works':                       'Creative Works',
}

PROJECT_MAP = {
    'Employment':             'Concordia',
    'Education':              'Early Career',
    'Honors':                 'Recognition',
    'Books':                  'Research',
    'Book Chapters':          'Research',
    'Journal Articles':       'Research',
    'Conference Presentations': 'Research',
    'Keynotes':               'IIF',
    'Invited Publications':   'Research',
    'Invited Lectures':       'Research',
    "Artist's Books":         'Creative',
    'Symposia Organized':     'Research',
    'Service':                'Research',
    'Documentaries':          'AbTeC',
    'Websites':               'Creative',
    'Residencies':            'Research',
    'Residency Organizer':    'Research',
    'Academic Reviews':       'Research',
    'Op-Ed':                  'Research',
    'Press Coverage':         'Research',
    'Policy & Reports':       'Research',
    'Solo Exhibitions':       'Creative',
    'Group Exhibitions':      'Creative',
    'Film Screenings':        'AbTeC',
    'Commissions':            'Creative',
    'Poetry':                 'Creative',
    'Curatorial':             'Creative',
    'Visiting Artist':        'Research',
    'Productions':            'AbTeC',
    'Creative Works':         'Creative',
}

MONTHS = {
    'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,
    'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12,
    'january':1,'february':2,'march':3,'april':4,'june':6,
    'july':7,'august':8,'september':9,'october':10,'november':11,'december':12,
}


# ── Date parsing ─────────────────────────────────────────────────────────────

def fmt(y, m=1, d=1):
    return f"{m:02d}/{d:02d}/{y:04d}"

def yy4(yy):
    """2-digit year → 4-digit (pivot: ≤29 → 2000s, else 1900s)."""
    return 2000 + yy if yy <= 29 else 1900 + yy

def parse_date_range(s):
    """
    Parse a date string that may be a range.
    Returns (start, end) as MM/DD/YYYY strings, or (None, None).

    Handles:
      M.YY or M.YYYY      e.g. "6.19", "9.2013", "5.2004"
      M.YY - M.YY         e.g. "6.08 - 5.14"
      M.YY - present      e.g. "6.14 - present"
      YYYY                e.g. "2025"
      YYYY-YY             e.g. "1994-97"  (abbreviated end, same century)
      YYYY-YYYY           e.g. "2012-15" treated as YYYY-YY when end < 100
      D Month, YYYY       e.g. "2 March, 2023"
      Month. D, YYYY      e.g. "Oct. 22, 2021"
      Month. D-D, YYYY    e.g. "Aug. 13-18, 2018"
      Month YYYY          e.g. "Feb 2014"
    """
    s = s.strip()
    # Normalise dash variants and surrounding spaces
    s = re.sub(r'[\u2013\u2014]', '-', s)
    s = re.sub(r'\s*-\s*', '-', s)

    # M.YY-present (must come before the letter check — "present" has letters)
    m = re.match(r'^(\d{1,2})\.(\d{2,4})-present$', s, re.I)
    if m:
        yr    = int(m.group(2))
        start = fmt(yr if yr > 100 else yy4(yr), int(m.group(1)))
        end   = fmt(TODAY.year, TODAY.month, TODAY.day)
        return start, end

    # ── Entries with month names ─────────────────────────────────────────────
    if re.search(r'[A-Za-z]', s):
        if s.lower() == 'present':
            d = fmt(TODAY.year, TODAY.month, TODAY.day)
            return d, d

        # "Month. D-D, YYYY"  (multi-day range)
        m = re.match(r'^([A-Za-z]+)\.?\s+\d{1,2}-\d{1,2},?\s*(\d{4})$', s)
        if m:
            mon = MONTHS.get(m.group(1).lower()[:3])
            if mon:
                d = fmt(int(m.group(2)), mon, 1)
                return d, d

        # "D Month, YYYY"
        m = re.match(r'^(\d{1,2})\s+([A-Za-z]+),?\s*(\d{4})$', s)
        if m:
            mon = MONTHS.get(m.group(2).lower()[:3])
            if mon:
                d = fmt(int(m.group(3)), mon, int(m.group(1)))
                return d, d

        # "Month. D, YYYY"
        m = re.match(r'^([A-Za-z]+)\.?\s+(\d{1,2}),?\s*(\d{4})$', s)
        if m:
            mon = MONTHS.get(m.group(1).lower()[:3])
            if mon:
                d = fmt(int(m.group(3)), mon, int(m.group(2)))
                return d, d

        # "Month YYYY"
        m = re.match(r'^([A-Za-z]+)\.?\s+(\d{4})$', s)
        if m:
            mon = MONTHS.get(m.group(1).lower()[:3])
            if mon:
                d = fmt(int(m.group(2)), mon, 1)
                return d, d

        return None, None

    # ── Numeric-only formats ─────────────────────────────────────────────────

    # M.YY-present  or  M.YY-M.YY  (handles M.YYYY too)
    m = re.match(r'^(\d{1,2})\.(\d{2,4})-(present|\d{1,2}\.\d{2,4})$', s, re.I)
    if m:
        yr = int(m.group(2))
        start_y = yr if yr > 100 else yy4(yr)
        start = fmt(start_y, int(m.group(1)))
        ep = m.group(3)
        if ep.lower() == 'present':
            end = fmt(TODAY.year, TODAY.month, TODAY.day)
        else:
            em = re.match(r'^(\d{1,2})\.(\d{2,4})$', ep)
            if em:
                ey = int(em.group(2))
                end = fmt(ey if ey > 100 else yy4(ey), int(em.group(1)))
            else:
                end = start
        return start, end

    # M.YY or M.YYYY  (single)
    m = re.match(r'^(\d{1,2})\.(\d{2,4})$', s)
    if m:
        yr = int(m.group(2))
        d  = fmt(yr if yr > 100 else yy4(yr), int(m.group(1)))
        return d, d

    # YYYY-YY  (abbreviated end year, same century as start)
    m = re.match(r'^(\d{4})-(\d{2})$', s)
    if m:
        start_y = int(m.group(1))
        end_yy  = int(m.group(2))
        end_y   = (start_y // 100) * 100 + end_yy
        return fmt(start_y), fmt(end_y, 6, 30)

    # YYYY-YYYY
    m = re.match(r'^(\d{4})-(\d{4})$', s)
    if m:
        return fmt(int(m.group(1))), fmt(int(m.group(2)))

    # YYYY  (single)
    m = re.match(r'^(\d{4})$', s)
    if m:
        d = fmt(int(m.group(1)))
        return d, d

    return None, None


# ── Text splitting ────────────────────────────────────────────────────────────

def split_nbsp(text):
    """
    Google Docs uses runs of non-breaking spaces (\xa0) as a visual tab to
    separate the date prefix from the entry description.
    Returns (date_candidate, rest) if the pattern is found, else (None, text).
    """
    # Must have at least 2 consecutive \xa0 characters
    m = re.match(r'^(.+?)[\xa0]{2,}(.*)', text, re.DOTALL)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return None, text


def extract_title(text):
    """
    For bibliography entries, try to pull out just the title.
    Prefers text in double-quotes; falls back to first sentence fragment.
    """
    m = re.search(r'["\u201c]([^"\u201d]{4,})["\u201d]', text)
    if m:
        return m.group(1).strip()
    parts = re.split(r'(?<=[a-z\)])[.;]', text, maxsplit=1)
    return parts[0].strip()[:200] if parts else text[:200]


# ── HTML parsing ─────────────────────────────────────────────────────────────

def parse_doc(html):
    soup  = BeautifulSoup(html, 'html.parser')
    rows  = []
    group = None
    last  = None   # last appended row (for multi-line continuation)

    for tag in soup.find_all(['h1','h2','h3','h4','h5','h6','p','li']):
        raw = tag.get_text(' ')        # keep internal spaces
        text = raw.strip()
        if not text or len(text) < 2:
            continue

        # ── Section heading? ─────────────────────────────────────────────────
        if tag.name in ('h1','h2','h3','h4','h5','h6'):
            key = re.sub(r'[\s\xa0]+', ' ', text.lower()).strip().rstrip(':')
            if key in SECTION_MAP:
                group = SECTION_MAP[key]
                last  = None
                print(f"  [{group}]")
            # Skip headings we don't recognise (e.g. 'Research / Creation')
            continue

        if group is None:
            continue

        # Normalise raw text: collapse internal \xa0 runs to a single space
        # EXCEPT the leading date-separator sequence, which we handle below.
        # We work on the raw tag text (preserving \xa0 for split_nbsp).
        raw_tag = tag.get_text('')   # no separator — preserves exact spacing

        # ── Strategy 1: date prefix + \xa0\xa0+ separator ─────────────────
        date_candidate, rest = split_nbsp(raw_tag)

        if date_candidate:
            # Clean up any stray \xa0 in the date candidate
            date_candidate = date_candidate.replace('\xa0', '').strip()
            start, end = parse_date_range(date_candidate)
            if start:
                # Clean up rest
                rest_clean = rest.replace('\xa0', ' ').strip()
                # Remove trailing junk like {link}, {text} etc.
                rest_clean = re.sub(r'\s*\{[^}]*\}\s*$', '', rest_clean).strip()
                row = {
                    'start date':  start,
                    'end date':    end or start,
                    'headline':    rest_clean,
                    'description': '',
                    'project':     PROJECT_MAP.get(group, ''),
                    'group':       group,
                }
                rows.append(row)
                last = row
                continue

        # ── Strategy 2: continuation line (degree, venue, etc.) ──────────
        # A short line with no year that immediately follows a dated entry
        # in the same section → append to previous entry's description.
        clean = re.sub(r'[\xa0\s]+', ' ', text).strip()
        # Remove leading runs of spaces/nbsp (indented continuation)
        clean_no_indent = clean.lstrip()
        has_year = bool(re.search(r'\b(19|20)\d{2}\b', clean_no_indent))

        if last and last['group'] == group and not has_year and len(clean_no_indent) < 150:
            addition = re.sub(r'\s*\{[^}]*\}\s*', ' ', clean_no_indent).strip()
            if addition:
                if last['description']:
                    last['description'] += '  ' + addition
                else:
                    last['description'] = addition
            continue

        # ── Strategy 3: bibliography entry — extract year from text ───────
        clean_full = re.sub(r'[\xa0]+', ' ', text).strip()
        clean_full = re.sub(r'\s*\{[^}]*\}\s*', ' ', clean_full).strip()

        years = re.findall(r'\b(19\d{2}|20\d{2})\b', clean_full)
        if years:
            year = int(years[-1])
            d    = fmt(year)
            row  = {
                'start date':  d,
                'end date':    d,
                'headline':    extract_title(clean_full),
                'description': clean_full,
                'project':     PROJECT_MAP.get(group, ''),
                'group':       group,
            }
            rows.append(row)
            last = row
        # If no year found, skip (e.g. pure continuation lines, empty cells)

    return rows


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    print(f"Fetching: {url}\n")

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urlopen(req, timeout=30) as resp:
            html = resp.read().decode('utf-8')
    except URLError as e:
        sys.exit(f"Fetch failed: {e}")

    rows = parse_doc(html)

    counts = {}
    for r in rows:
        counts[r['group']] = counts.get(r['group'], 0) + 1

    print(f"\nParsed {len(rows)} entries:")
    for g in sorted(counts):
        print(f"  {g:45s} {counts[g]:3d}")

    dst = Path(__file__).parent / "cv-data.js"
    dst.write_text(
        "// Generated by fetch_cv_from_gdoc.py — re-run to refresh from Google Doc.\n"
        "window.__TIMELINE_DATA__ = "
        + json.dumps(rows, ensure_ascii=False, indent=2)
        + ";\n",
        encoding='utf-8',
    )
    print(f"\nWrote {len(rows)} rows  →  {dst}")


if __name__ == '__main__':
    main()
