#!/usr/bin/env python3
"""
Fetch Jason Edward Lewis's published CV Google Docs and convert to cv-data.js.

Accepts up to three published Google Doc URLs:
  URL 1 (primary, required)  — Research-Creation CV
  URL 2 (optional)           — Funding CV
  URL 3 (optional)           — Teaching & Service CV

If URL 2 or 3 fail to fetch they are skipped with a warning; only URL 1 is
required.  This makes the script usable by anyone with a single-document CV.

Usage:
    python3 fetch_cv_from_gdoc.py               # uses all three hardcoded defaults
    python3 fetch_cv_from_gdoc.py <url1>        # research-creation only
    python3 fetch_cv_from_gdoc.py <url1> <url2> <url3>

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


# ── Default Google Doc URLs ───────────────────────────────────────────────────
DEFAULT_URLS = [
    # 1. Research-Creation (primary — required)
    "https://docs.google.com/document/d/e/"
    "2PACX-1vRIeY4A3fbqJj29GP2yT0FpJkoPOLiLVqaOqPuIUDuJOjXLGwM0jEuS2WGb_daBLY8dCEuooURhz-5D/pub",
    # 2. Funding (optional)
    "https://docs.google.com/document/d/e/"
    "2PACX-1vTitfLMisxZ3NcqdLOIsf4Bsj_qSuMfuj6vh2N3d86ZjHyy4FlXx0cRIgGWdEhoerPLjs7rgVn75XNL/pub",
    # 3. Teaching & Service (optional)
    "https://docs.google.com/document/d/e/"
    "2PACX-1vQXdHyfjF3YivP2hM8Tf81qiasZymZKN4edMZFK3Rp7cq1O__opAvx0iFqdvK-xFzH5duKBb4Eo3Xt6/pub",
]

TODAY = date.today()

# ── Output sort order (mirrors generate_cv_xlsx.py GRP_ORDER) ────────────────
GRP_ORDER = [
    "Employment", "Honors", "Education",
    "Creative Works", "Books/Chapters", "Journal Articles",
    "Keynotes", "Conference Presentations", "Invited Publications", "Invited Lectures",
    "Policy Papers", "Op-Ed", "Artist's Books", "Poetry",
    "Solo Exhibitions", "Group Exhibitions",
    "Film Screenings", "Commissions", "Curatorial", "Visiting Artist", "Productions",
    "Residencies", "Residency Organizer",
    "Documentaries", "Websites",
    "Press Coverage", "Academic Reviews", "Symposia Organized",
    "Funding (PI)", "Funding (Co-I)", "Funding (Internal)",
    "Courses Taught",
    "Postdoc", "PhD", "Masters", "Grad Certificate", "Undergraduate",
    "Service",
]

# ── Section heading text → internal group name ───────────────────────────────
# Keys are lowercased, whitespace-collapsed, and Roman-numeral prefixes removed.
SECTION_MAP = {
    # ── Research-Creation doc ─────────────────────────────────────────────
    'employment history':           'Employment',
    'education':                    'Education',
    'honors and awards':            'Honors',
    'books':                        'Books/Chapters',
    'book chapters':                'Books/Chapters',
    'journal articles & conference proceedings (refereed)': 'Journal Articles',
    'journal articles & conference proceedings':            'Journal Articles',
    'journal articles and conference proceedings':          'Journal Articles',
    'conference / symposia presentations (refereed)':       'Conference Presentations',
    'conference / symposia presentations':                  'Conference Presentations',
    'keynote, plenary, and special guest speaker':          'Keynotes',
    'invited publications':                                 'Invited Publications',
    'invited lectures / artist talks / panels':             'Invited Lectures',
    "artist's books and exhibition publications":           "Artist's Books",
    "artist\u2019s books and exhibition publications":      "Artist's Books",
    'policy papers, governmental presentations, reviews & consultations': 'Policy Papers',
    'exhibitions - solo':           'Solo Exhibitions',
    'exhibitions - group':          'Group Exhibitions',
    'film screenings':              'Film Screenings',
    'commissions':                  'Commissions',
    'poetry publication & performances': 'Poetry',
    'curatorial':                   'Curatorial',
    'visiting artist & master classes': 'Visiting Artist',
    'producer / executive producer': 'Productions',
    'major works':                  'Creative Works',
    'residencies':                  'Residencies',
    'residency organizer':          'Residency Organizer',
    'documentaries':                'Documentaries',
    'websites':                     'Websites',
    'op-ed':                        'Op-Ed',
    'press coverage / interviews / documentaries':     'Press Coverage',
    'press coverage / interviews / documentar ies':    'Press Coverage',  # line-break artifact variant
    'academic review & textbook inclusion':        'Academic Reviews',
    'symposium, workshop, and lecture series organizer or lead': 'Symposia Organized',
    'promotion review / peer reviewer / jury member / expert assessor': 'Service',

    # ── Funding doc ───────────────────────────────────────────────────────
    'as pi/lead':                            'Funding (PI)',
    'as co-investigator':                    'Funding (Co-I)',
    'research/creation funding - internal':  'Funding (Internal)',

    # ── Teaching & Service doc ────────────────────────────────────────────
    'courses taught':                            'Courses Taught',
    'postdoctoral fellow advisor':               'Postdoc',
    'doctoral thesis advising':                  'PhD',
    'master thesis advising - supervisor':       'Masters',
    'master thesis advising':                    'Masters',
    'graduate certificate advising - supervisor':'Grad Certificate',
    'graduate certificate advising':             'Grad Certificate',
    'undergraduate research assistants':         'Undergraduate',
    # Service sub-sections
    'department chair, coordinator, director':   'Service',
    'departmental, unit committees':             'Service',
    'faculty committees':                        'Service',
    'university committees':                     'Service',
    'external committees':                       'Service',
}

SUPERVISION_GROUPS = {'Postdoc', 'PhD', 'Masters', 'Grad Certificate', 'Undergraduate'}

# Headings that should stop parsing (entries not wanted in any group)
RESET_SECTIONS = {
    'independent study',
    'end-of-term group evaluation',
    'internship supervising',
    'graduate research assistants',
}

MONTHS = {
    'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,
    'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12,
    'january':1,'february':2,'march':3,'april':4,'june':6,
    'july':7,'august':8,'september':9,'october':10,'november':11,'december':12,
}


# ── Date parsing ──────────────────────────────────────────────────────────────

def fmt(y, m=1, d=1):
    return f"{m:02d}/{d:02d}/{y:04d}"

def yy4(yy):
    """2-digit year → 4-digit (pivot: ≤29 → 2000s, else 1900s)."""
    return 2000 + yy if yy <= 29 else 1900 + yy

def parse_date_range(s):
    s = s.strip()
    s = re.sub(r'[\u2013\u2014]', '-', s)
    s = re.sub(r'\s*-\s*', '-', s)

    # YYYY-present  (Teaching & Service doc format)
    m = re.match(r'^(\d{4})-present$', s, re.I)
    if m:
        return fmt(int(m.group(1))), fmt(TODAY.year, TODAY.month, TODAY.day)

    # M.YY-present
    m = re.match(r'^(\d{1,2})\.(\d{2,4})-present$', s, re.I)
    if m:
        yr = int(m.group(2))
        return fmt(yr if yr > 100 else yy4(yr), int(m.group(1))), \
               fmt(TODAY.year, TODAY.month, TODAY.day)

    # Entries with month names
    if re.search(r'[A-Za-z]', s):
        if s.lower() == 'present':
            d = fmt(TODAY.year, TODAY.month, TODAY.day)
            return d, d
        m = re.match(r'^([A-Za-z]+)\.?\s+\d{1,2}-\d{1,2},?\s*(\d{4})$', s)
        if m:
            mon = MONTHS.get(m.group(1).lower()[:3])
            if mon:
                d = fmt(int(m.group(2)), mon)
                return d, d
        m = re.match(r'^(\d{1,2})\s+([A-Za-z]+),?\s*(\d{4})$', s)
        if m:
            mon = MONTHS.get(m.group(2).lower()[:3])
            if mon:
                return fmt(int(m.group(3)), mon, int(m.group(1))), \
                       fmt(int(m.group(3)), mon, int(m.group(1)))
        m = re.match(r'^([A-Za-z]+)\.?\s+(\d{1,2}),?\s*(\d{4})$', s)
        if m:
            mon = MONTHS.get(m.group(1).lower()[:3])
            if mon:
                return fmt(int(m.group(3)), mon, int(m.group(2))), \
                       fmt(int(m.group(3)), mon, int(m.group(2)))
        m = re.match(r'^([A-Za-z]+)\.?\s+(\d{4})$', s)
        if m:
            mon = MONTHS.get(m.group(1).lower()[:3])
            if mon:
                d = fmt(int(m.group(2)), mon)
                return d, d
        return None, None

    # M.YY or M.YY-M.YY
    m = re.match(r'^(\d{1,2})\.(\d{2,4})-(present|\d{1,2}\.\d{2,4})$', s, re.I)
    if m:
        yr = int(m.group(2))
        start = fmt(yr if yr > 100 else yy4(yr), int(m.group(1)))
        ep = m.group(3)
        if ep.lower() == 'present':
            end = fmt(TODAY.year, TODAY.month, TODAY.day)
        else:
            em = re.match(r'^(\d{1,2})\.(\d{2,4})$', ep)
            ey = int(em.group(2)) if em else 0
            end = fmt(ey if ey > 100 else yy4(ey), int(em.group(1))) if em else start
        return start, end

    m = re.match(r'^(\d{1,2})\.(\d{2,4})$', s)
    if m:
        yr = int(m.group(2))
        d  = fmt(yr if yr > 100 else yy4(yr), int(m.group(1)))
        return d, d

    # YYYY-YY (abbreviated end, same century)
    m = re.match(r'^(\d{4})-(\d{2})$', s)
    if m:
        sy = int(m.group(1))
        ey = (sy // 100) * 100 + int(m.group(2))
        return fmt(sy), fmt(ey, 6, 30)

    # YYYY-YYYY
    m = re.match(r'^(\d{4})-(\d{4})$', s)
    if m:
        return fmt(int(m.group(1))), fmt(int(m.group(2)))

    # YYYY (single)
    m = re.match(r'^(\d{4})$', s)
    if m:
        d = fmt(int(m.group(1)))
        return d, d

    return None, None


# ── Text splitting ────────────────────────────────────────────────────────────

def split_date_prefix(text):
    """
    Split a line into (date_candidate, rest).
    Google Docs uses \xa0 runs or multiple spaces as a visual tab separator.
    Returns (None, text) if no separator found.
    """
    # Non-breaking space run (standard Google Docs)
    m = re.match(r'^(.+?)[\xa0]{2,}(.*)', text, re.DOTALL)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    # Tab character
    if '\t' in text:
        parts = text.split('\t', 1)
        if parts[0].strip():
            return parts[0].strip(), parts[1].strip()
    # 3+ regular spaces
    m = re.match(r'^(.+?)\s{3,}(.*)', text, re.DOTALL)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return None, text


def extract_title(text):
    """Pull out a title: prefers quoted text, falls back to first sentence."""
    m = re.search(r'["\u201c]([^"\u201d]{4,})["\u201d]', text)
    if m:
        return m.group(1).strip()
    parts = re.split(r'(?<=[a-z\)])[.;]', text, maxsplit=1)
    return parts[0].strip()[:200] if parts else text[:200]


# ── Supervision headline normalisation ───────────────────────────────────────

ROLE_MAP = {
    'supervisor':           '',             # primary — no qualifier shown
    'co-supervisor':        'Co-supervisor',
    'co supervisor':        'Co-supervisor',
    'secondary':            'Secondary',
    'secondary supervisor': 'Secondary',
    'committee':            'Committee',
    'committee member':     'Committee',
}

def normalize_supervision(text, group):
    """
    Normalise a supervision entry parsed from the Google Doc.
    Returns (headline, description).

    Handles:
      "Juliet Mackie (supervisor) / Thesis title"    → "Juliet Mackie",              "Thesis title"
      "Jessica Barudin (co-supervisor) / ..."        → "Jessica Barudin (Co-supervisor)", "..."
      "Tarcisio Cataldi Tegani (committee) / ..."    → "Tarcisio Cataldi Tegani (Committee)", "..."
      "Melemaikalani Moniz - Postdoctoral Fellow..."  → "Melemaikalani Moniz",         "Postdoctoral Fellow..."
      "Destiny Chescappio"                           → "Destiny Chescappio",           ""
      "Joanna Pederson / Augmented Reality: ..."     → "Joanna Pederson",             "Augmented Reality: ..."
    """
    # Postdoc: split name from role description at first " - "
    if group == 'Postdoc':
        m = re.match(r'^(.+?)\s*[-\u2013]\s*(.+)$', text)
        if m:
            return m.group(1).strip(), m.group(2).strip()
        return text, ''

    # Split off thesis title at " / "
    thesis = ''
    if ' / ' in text:
        parts = text.split(' / ', 1)
        text  = parts[0].strip()
        thesis = parts[1].strip()

    # Extract trailing parenthetical role qualifier
    m = re.search(r'\s*\(([^)]+)\)\s*$', text)
    if m:
        role_raw = m.group(1).lower().strip()
        if role_raw in ROLE_MAP:
            name      = text[:m.start()].strip()
            qualifier = ROLE_MAP[role_raw]
            headline  = f"{name} ({qualifier})" if qualifier else name
            return headline, thesis

    return text, thesis


# ── HTML parsing ─────────────────────────────────────────────────────────────

def parse_doc(html):
    soup  = BeautifulSoup(html, 'html.parser')
    rows  = []
    group = None
    last  = None

    for tag in soup.find_all(['h1','h2','h3','h4','h5','h6','p','li']):
        raw  = tag.get_text(' ')
        text = raw.strip()
        if not text or len(text) < 2:
            continue

        # ── Section heading ───────────────────────────────────────────────
        if tag.name in ('h1','h2','h3','h4','h5','h6'):
            key = re.sub(r'[\s\xa0]+', ' ', text.lower()).strip().rstrip(':')
            # Normalise spaces before punctuation: "presentations , reviews" → "presentations, reviews"
            key = re.sub(r'\s+([,;:])', r'\1', key)
            # Strip leading Roman-numeral prefix: "iia.", "iv.", "ii b .", etc.
            # Allow optional spaces around the letter suffix and dot.
            key = re.sub(r'^[ivxlc]+\s*[a-z]?\s*\.\s*', '', key)
            if key in SECTION_MAP:
                group = SECTION_MAP[key]
                last  = None
                print(f"  [{group}]")
            elif key in RESET_SECTIONS:
                # Explicitly unrecognised sub-section — stop parsing until next known heading
                group = None
            # Always skip heading tags (don't parse them as entries)
            continue

        if group is None:
            continue

        raw_tag = tag.get_text('')   # no separator — preserves \xa0 runs

        # ── Strategy 1: date prefix + separator ──────────────────────────
        date_candidate, rest = split_date_prefix(raw_tag)

        if date_candidate:
            dc = date_candidate.replace('\xa0', '').strip()
            # Strip "YYYY / SEASON" course-schedule prefix → just "YYYY"
            dc = re.sub(r'^(\d{4})\s*/\s*\w+$', r'\1', dc)
            start, end = parse_date_range(dc)
            if start:
                rest_clean = rest.replace('\xa0', ' ').strip()
                rest_clean = re.sub(r'\s*\{[^}]*\}\s*$', '', rest_clean).strip()

                headline = rest_clean
                desc     = ''

                if group in SUPERVISION_GROUPS:
                    headline, desc = normalize_supervision(rest_clean, group)

                row = {
                    'start date':  start,
                    'end date':    end or start,
                    'headline':    headline,
                    'description': desc,
                    'project':     '',
                    'group':       group,
                }
                rows.append(row)
                last = row
                continue

        # ── Strategy 2: continuation line ────────────────────────────────
        clean          = re.sub(r'[\xa0\s]+', ' ', text).strip()
        clean_no_indent = clean.lstrip()
        has_year       = bool(re.search(r'\b(19|20)\d{2}\b', clean_no_indent))

        if (last and last['group'] == group
                and not has_year and len(clean_no_indent) < 150
                and group not in SUPERVISION_GROUPS):
            addition = re.sub(r'\s*\{[^}]*\}\s*', ' ', clean_no_indent).strip()
            if addition:
                sep = '  ' if last['description'] else ''
                last['description'] = last['description'] + sep + addition
            continue

        # ── Strategy 3: bibliography — year extraction ────────────────────
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
                'project':     '',
                'group':       group,
            }
            rows.append(row)
            last = row

    return rows


# ── Dimension derivation (mirrors generate_cv_xlsx.py derive_cv_dimensions) ──

def derive_dimensions(rows):
    """
    Enrich each row dict with org, program, funding_group, category_group.
    Mutates rows in-place and returns the list.
    """
    early_career_orgs = [
        ('Arts Alliance Laboratory', 'Arts Alliance Laboratory'),
        ('Arts Alliance Ventures',   'Arts Alliance Ventures'),
        ('Interval Research',        'Interval Research Corporation'),
        ('Fitch',                    'Fitch, Inc.'),
        ('Lollapalooza',             "Lollapalooza '94 Tour"),
        ('Carnegie Research Fellow', 'Institute for Research on Learning'),
        ('Stanford University',      'Stanford University'),
    ]
    edu_orgs = [
        ('Royal College of Art', 'Royal College of Art'),
        ('Freie Universität',    'Freie Universität Berlin'),
        ('Stanford University',  'Stanford University'),
    ]
    agencies = [
        ('Social Sciences and Humanities Research Council', 'Social Sciences and Humanities Research Council'),
        ('Natural Sciences and Engineering Research Council','Natural Sciences and Engineering Research Council'),
        ('Canada First Research Excellence Fund',           'Canada First Research Excellence Fund'),
        ('New Frontiers in Research Fund',                  'New Frontiers in Research Fund'),
        ('Pierre Elliott Trudeau Foundation',               'Pierre Elliott Trudeau Foundation'),
        ('Fonds de recherche',                              'Fonds de recherche du Québec'),
        ('Fonds québécois',                                 'Fonds de recherche du Québec'),
        ('MacArthur Foundation',                            'The MacArthur Foundation'),
        ('Schmidt Family Foundation',                       'Schmidt Family Foundation'),
        ('Canada Foundation for Innovation',                'Canada Foundation for Innovation'),
        ('Canada Council for the Arts',                     'Canada Council for the Arts'),
        ('Hexagram Institute',                              'Hexagram Institute'),
        ('Heritage Canada',                                 'Heritage Canada'),
        ('Hewitt Foundation',                               'Hewitt Foundation'),
        ('Kanaeokana Network',                              'Kanaeokana Network'),
        ('Indigenous Screen Office',                        'Indigenous Screen Office'),
        ('Arts Council of England',                         'Arts Council of England'),
        ('McConnell Family Foundation',                     'J. W. McConnell Family Foundation'),
        ('Montalvo Arts Center',                            'Montalvo Arts Center'),
        ('Fine Arts-Engineering Seed Grants',               'Fine Arts-Engineering'),
        ('Fine Arts Faculty',                               'Fine Arts'),
        ('Office of Research',                              'Office of Research'),
        ('Jarislowsky Institute',                           'Jarislowsky Institute'),
        ('Concordia University',                            'Concordia University'),
    ]
    funding_group_map = {
        'Social Sciences and Humanities Research Council':  'Tri-council',
        'Natural Sciences and Engineering Research Council':'Tri-council',
        'Canada First Research Excellence Fund':            'Tri-council',
        'Canada Foundation for Innovation':                 'Tri-council',
        'New Frontiers in Research Fund':                   'Tri-council',
        'Fine Arts':                                        'Concordia',
        'Fine Arts-Engineering':                            'Concordia',
        'Office of Research':                               'Concordia',
        'Jarislowsky Institute':                            'Concordia',
        'Concordia University':                             'Concordia',
    }
    category_group_map = {
        'Undergraduate':           'Supervision',
        'Grad Certificate':        'Supervision',
        'Masters':                 'Supervision',
        'PhD':                     'Supervision',
        'Postdoc':                 'Supervision',
        'Creative Works':          'Art',
        'Solo Exhibitions':        'Art',
        'Group Exhibitions':       'Art',
        'Productions':             'Art',
        "Artist's Books":          'Art',
        'Books/Chapters':          'Dissemination',
        'Journal Articles':        'Dissemination',
        'Keynotes':                'Dissemination',
        'Conference Presentations':'Dissemination',
        'Invited Publications':    'Dissemination',
        'Invited Lectures':        'Dissemination',
        'Policy Papers':           'Dissemination',
        'Funding (PI)':            'Funding',
        'Funding (Co-I)':          'Funding',
        'Funding (Internal)':      'Funding',
    }

    for row in rows:
        group    = row['group']
        headline = row['headline']
        desc     = row['description']
        org = program = role = funding_group = ''
        category_group = category_group_map.get(group, '')

        if group == 'Education':
            for keyword, institution in edu_orgs:
                if keyword in headline:
                    org = institution
                    break

        elif group == 'Employment':
            org = 'Concordia University'
            for keyword, institution in early_career_orgs:
                if keyword in headline:
                    org = institution
                    break

        elif group in ('Funding (PI)', 'Funding (Co-I)', 'Funding (Internal)'):
            for keyword, agency in agencies:
                if keyword in desc:
                    program = agency
                    break
            funding_group = funding_group_map.get(program, '')
            if group == 'Funding (PI)':
                if 'Artist.' in desc:
                    role = 'Artist'
                elif 'Research Director' in desc:
                    role = 'Research Director'
                elif 'Fellow' in headline:
                    role = 'Fellow'
                elif 'Co-lead' in desc:
                    role = 'Co-lead'
                elif 'Co-grant holder' in desc:
                    role = 'Co-grant Holder'
                else:
                    role = 'Primary Investigator'
            elif group == 'Funding (Co-I)':
                role = 'Core Applicant' if 'Core Applicant' in desc else 'Co-investigator'
            else:
                role = 'Internal'

        row['org']           = org
        row['program']       = program
        row['project']       = role if role else row.get('project', '')
        row['funding_group'] = funding_group
        row['category_group']= category_group

    return rows


# ── Fetch ─────────────────────────────────────────────────────────────────────

def fetch_url(url, required=True):
    """Fetch a URL and return HTML string, or None if optional and fetch fails."""
    print(f"\nFetching: {url}")
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urlopen(req, timeout=30) as resp:
            return resp.read().decode('utf-8')
    except URLError as e:
        if required:
            sys.exit(f"Fetch failed (primary URL — cannot continue): {e}")
        print(f"  ⚠  Skipped (fetch failed): {e}")
        return None


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    if args:
        urls     = args[:3]
        required = [True] + [False] * (len(urls) - 1)
    else:
        urls     = DEFAULT_URLS
        required = [True, False, False]

    all_rows = []
    for i, (url, req) in enumerate(zip(urls, required)):
        html = fetch_url(url, required=req)
        if html is None:
            continue
        print()
        rows = parse_doc(html)
        if i == 0:                        # Research-Creation doc → mark for public build
            for r in rows:
                r['_research'] = True
        all_rows.extend(rows)

    # Enrich with org / program / funding_group / category_group
    all_rows = derive_dimensions(all_rows)

    # ── Clean up Documentaries: strip leading org prefix ("Obx Labs.") ────────
    _obx_pfx = re.compile(r'^obx\s*labs\.\s*', re.IGNORECASE)
    for row in all_rows:
        if row.get('group') != 'Documentaries':
            continue
        desc = row.get('description', '')
        desc_clean = _obx_pfx.sub('', desc).strip()
        if desc_clean != desc:                      # prefix was present
            row['headline']    = extract_title(desc_clean)
            row['description'] = desc_clean

    # Split off Research-Creation rows before removing the marker
    research_rows = [r for r in all_rows if r.get('_research')]
    for r in all_rows:
        r.pop('_research', None)

    # Sort by canonical group order
    sort_key = lambda r: GRP_ORDER.index(r['group']) if r['group'] in GRP_ORDER else 99
    all_rows.sort(key=sort_key)
    research_rows.sort(key=sort_key)

    # Summary
    counts = {}
    for r in all_rows:
        counts[r['group']] = counts.get(r['group'], 0) + 1
    print(f"\nTotal: {len(all_rows)} entries across {len(counts)} groups:")
    for g in GRP_ORDER:
        if g in counts:
            print(f"  {g:45s} {counts[g]:3d}")
    unlisted = [g for g in counts if g not in GRP_ORDER]
    for g in sorted(unlisted):
        print(f"  {g:45s} {counts[g]:3d}  ← unlisted group")

    base = Path(__file__).parent

    dst = base / "cv-data.js"
    dst.write_text(
        "// Generated by fetch_cv_from_gdoc.py — re-run to refresh from Google Docs.\n"
        "// Contains all three CV sections (Research-Creation, Funding, Teaching & Service).\n"
        "window.__TIMELINE_DATA__ = "
        + json.dumps(all_rows, ensure_ascii=False, indent=2)
        + ";\n",
        encoding='utf-8',
    )
    print(f"\nWrote {len(all_rows)} rows  →  {dst}")

    dst_pub = base / "cv-data-public.js"
    dst_pub.write_text(
        "// Generated by fetch_cv_from_gdoc.py — re-run to refresh from Google Docs.\n"
        "// Contains Research-Creation CV only (public-facing build).\n"
        "window.__TIMELINE_DATA__ = "
        + json.dumps(research_rows, ensure_ascii=False, indent=2)
        + ";\n",
        encoding='utf-8',
    )
    print(f"Wrote {len(research_rows)} rows  →  {dst_pub}  (Research-Creation only)")


if __name__ == '__main__':
    main()
