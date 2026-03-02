"""Generate cv.xlsx from Jason Edward Lewis CV data.

Sections parsed automatically from cv.txt:
  Books                                                        → Books/Chapters
  Book Chapters                                                → Books/Chapters
  Journal Articles & Conference Proceedings (Refereed)         → Journal Articles
  Conference / Symposia Presentations (Refereed)               → Conference Presentations
  Invited Publications                                         → Invited Publications
  Invited Lectures / Artist Talks / Panels                     → Invited Lectures
  Policy Papers, Governmental Presentations, Reviews & Consultations → Policy Papers
  Artist's Books and Exhibition Publications                   → Artist's Books
  Exhibitions - Solo                                           → Solo Exhibitions

Everything else stays hardcoded (Employment, Education, Honors, Creative Works,
Keynotes, Group Exhibitions, Productions, Funding PI/Co-I/Internal, Courses Taught,
Supervision, Service).
"""
import re
import calendar
import openpyxl
from openpyxl import Workbook
from pathlib import Path

wb = Workbook()
ws = wb.active
ws.title = "CV"

headers = ["start date", "end date", "headline", "description", "project", "group",
           "org", "program", "funding_group", "category_group"]
ws.append(headers)

PRESENT = "02/25/2026"

GRP_ORDER = [
    "Employment", "Honors", "Education", "Creative Works", "Books/Chapters",
    "Journal Articles", "Keynotes",
    "Conference Presentations", "Invited Publications", "Invited Lectures",
    "Policy Papers", "Artist's Books",
    "Solo Exhibitions", "Group Exhibitions", "Productions",
    "Funding (PI)", "Funding (Co-I)", "Funding (Internal)",
    "Courses Taught",
    "Undergraduate", "Grad Certificate", "Masters", "PhD", "Postdoc",
    "Service",
]

# ─── All known section headers in cv.txt (used to detect section boundaries) ───
ALL_CV_SECTIONS = [
    "Employment History",
    "Education",
    "Honors and Awards",
    "Research / Creation",
    "(student co-authors in bold)",
    "Books",
    "Book Chapters",
    "Journal Articles & Conference Proceedings (Refereed)",
    "Conference / Symposia Presentations (Refereed)",
    "Keynote, Plenary, and Special Guest Speaker",
    "Invited Publications",
    "Invited Lectures / Artist Talks / Panels",
    "Policy Papers, Governmental Presentations, Reviews & Consultations",
    "Artist\u2019s Books and Exhibition Publications",
    "Symposium, Workshop, and Lecture Series Organizer or Lead",
    "Promotion Review / Peer Reviewer / Jury Member / Expert Assessor",
    "Documentaries",
    "Websites",
    "Residencies",
    "Residency Organizer",
    "Academic Review & Textbook Inclusion",
    "Op-Ed",
    "Press Coverage / Interviews / Documentaries",
    "Exhibitions - Solo",
    "Exhibitions - Group",
    "Film Screenings",
    "Commissions",
    "Poetry Publication & Performances",
    "Curatorial",
    "Visiting Artist & Master Classes",
    "Journal Cover Image",
    "Producer / Executive Producer",
]

# Sections we want to parse → (cv.txt section header, group name for output)
PARSE_SECTIONS = {
    "Books": "Books/Chapters",
    "Book Chapters": "Books/Chapters",
    "Journal Articles & Conference Proceedings (Refereed)": "Journal Articles",
    "Conference / Symposia Presentations (Refereed)": "Conference Presentations",
    "Invited Publications": "Invited Publications",
    "Invited Lectures / Artist Talks / Panels": "Invited Lectures",
    "Policy Papers, Governmental Presentations, Reviews & Consultations": "Policy Papers",
    "Artist\u2019s Books and Exhibition Publications": "Artist's Books",
    "Exhibitions - Solo": "Solo Exhibitions",
}

# Month name → number (handles full + common abbreviations)
MONTH_MAP = {
    "january": 1, "jan": 1,
    "february": 2, "feb": 2,
    "march": 3, "mar": 3,
    "april": 4, "apr": 4,
    "may": 5,
    "june": 6, "jun": 6,
    "july": 7, "jul": 7,
    "august": 8, "aug": 8,
    "september": 9, "sep": 9, "sept": 9,
    "october": 10, "oct": 10,
    "november": 11, "nov": 11,
    "december": 12, "dec": 12,
}

# Seasons
SEASON_MAP = {
    "winter": (12, 1, 2),    # (start_month, mid, end_month) — spans year boundary
    "spring": (3, 4, 5),
    "summer": (6, 7, 8),
    "fall": (9, 10, 11),
    "autumn": (9, 10, 11),
}


def _fmt(m, d, y):
    """Format (month, day, year) as MM/DD/YYYY."""
    return f"{int(m):02d}/{int(d):02d}/{int(y):04d}"


def _last_day(m, y):
    """Last day of month m in year y."""
    return calendar.monthrange(int(y), int(m))[1]


def parse_date(text):
    """Extract (start_date, end_date) strings in MM/DD/YYYY from a CV entry.

    Priority order:
    1.  Same-month day-range: "July 26 - 31, 2026" / "Jun. 26-29, 2019"
    2.  Single month+day+year: "January 29, 2026" / "Mar. 20, 2018"
    3.  Two-month range+year: "Nov. 4 - Dec. 2, 2017" / "May - June 2015"
    4.  Month+year only: "November 2008" / "Nov. 2008"
    5.  Season+year: "Winter 2016" / "Summer 2005"
    6.  Year range: "2011-13" / "2011-2013"
    7.  Year-prefixed line: starts with 4-digit year
    8.  Bare year at end: "... Cambridge, MA: MIT Press, 2021."
    9.  In press / submitted → current year
    10. Any 4-digit year found anywhere
    """
    t = text.strip()

    # 9. In press / submitted
    if re.search(r'\b(in press|in Press|Revised and Submitted|Submitted)\b', t, re.I):
        curr_yr = 2026  # PRESENT year
        return (_fmt(1, 1, curr_yr), _fmt(12, 31, curr_yr))

    month_re = r'(?:' + '|'.join(MONTH_MAP.keys()) + r')\.?'

    # 1. Same-month day-range: "July 26 - 31, 2026" or "Jun. 26-29, 2019"
    pat1 = re.compile(
        r'(' + month_re + r')\s+(\d{1,2})\s*[-–]\s*(\d{1,2}),?\s+(\d{4})',
        re.I)
    m = pat1.search(t)
    if m:
        mo = MONTH_MAP[re.sub(r'\.', '', m.group(1)).lower()]
        d1, d2, yr = int(m.group(2)), int(m.group(3)), int(m.group(4))
        return (_fmt(mo, d1, yr), _fmt(mo, d2, yr))

    # 2. Single month+day+year: "January 29, 2026"
    pat2 = re.compile(r'(' + month_re + r')\s+(\d{1,2}),?\s+(\d{4})', re.I)
    m = pat2.search(t)
    if m:
        mo = MONTH_MAP[re.sub(r'\.', '', m.group(1)).lower()]
        d, yr = int(m.group(2)), int(m.group(3))
        return (_fmt(mo, d, yr), _fmt(mo, d, yr))

    # 3a. Two-month range with days: "Nov. 4 - Dec. 2, 2017"
    pat3a = re.compile(
        r'(' + month_re + r')\s*\.?\s*(\d{1,2})\s*[-–]\s*(' + month_re + r')\s*\.?\s*(\d{1,2}),?\s+(\d{4})',
        re.I)
    m = pat3a.search(t)
    if m:
        mo1 = MONTH_MAP[re.sub(r'\.', '', m.group(1)).lower()]
        d1  = int(m.group(2))
        mo2 = MONTH_MAP[re.sub(r'\.', '', m.group(3)).lower()]
        d2  = int(m.group(4))
        yr  = int(m.group(5))
        return (_fmt(mo1, d1, yr), _fmt(mo2, d2, yr))

    # 3b. Two-month range no days: "May - June 2015"
    pat3b = re.compile(
        r'(' + month_re + r')\s*[-–]\s*(' + month_re + r')\s+(\d{4})',
        re.I)
    m = pat3b.search(t)
    if m:
        mo1 = MONTH_MAP[re.sub(r'\.', '', m.group(1)).lower()]
        mo2 = MONTH_MAP[re.sub(r'\.', '', m.group(2)).lower()]
        yr  = int(m.group(3))
        return (_fmt(mo1, 1, yr), _fmt(mo2, _last_day(mo2, yr), yr))

    # 4. Month+year only: "November 2008" / "Nov. 2008"
    pat4 = re.compile(r'(' + month_re + r')\.?\s+(\d{4})', re.I)
    m = pat4.search(t)
    if m:
        mo = MONTH_MAP[re.sub(r'\.', '', m.group(1)).lower()]
        yr = int(m.group(2))
        return (_fmt(mo, 1, yr), _fmt(mo, _last_day(mo, yr), yr))

    # 5. Season+year: "Winter 2016" / "Summer 2005"
    pat5 = re.compile(r'\b(winter|spring|summer|fall|autumn)\s+(\d{4})\b', re.I)
    m = pat5.search(t)
    if m:
        season = m.group(1).lower()
        yr = int(m.group(2))
        months = SEASON_MAP[season]
        if season == 'winter':
            # Winter spans Dec of prev year → Feb of stated year
            return (_fmt(months[0], 1, yr - 1), _fmt(months[2], _last_day(months[2], yr), yr))
        return (_fmt(months[0], 1, yr), _fmt(months[2], _last_day(months[2], yr), yr))

    # 6. Year range: "2011-13" or "2011-2013"
    pat6 = re.compile(r'\b((?:19|20)\d{2})\s*[-–]\s*((?:19|20)?\d{2})\b')
    m = pat6.search(t)
    if m:
        yr1 = int(m.group(1))
        raw2 = m.group(2)
        if len(raw2) == 2:
            yr2 = int(str(yr1)[:2] + raw2)
        else:
            yr2 = int(raw2)
        return (_fmt(1, 1, yr1), _fmt(12, 31, yr2))

    # 7. Year-prefixed line: "2017    Some entry..."
    pat7 = re.compile(r'^((?:19|20)\d{2})\s+')
    m = pat7.match(t)
    if m:
        yr = int(m.group(1))
        # Try to refine with a month found anywhere in the line
        pat4b = re.compile(r'\b(' + month_re + r')\.?\s+', re.I)
        mm = pat4b.search(t)
        if mm:
            mo = MONTH_MAP[re.sub(r'\.', '', mm.group(1)).lower()]
            return (_fmt(mo, 1, yr), _fmt(mo, _last_day(mo, yr), yr))
        return (_fmt(1, 1, yr), _fmt(12, 31, yr))

    # 8. Bare year at end of text (last 4-digit year-like token)
    # e.g. "...Cambridge, MA: MIT Press, 2021."
    all_years = re.findall(r'\b((?:19|20)\d{2})\b', t)
    if all_years:
        yr = int(all_years[-1])
        return (_fmt(1, 1, yr), _fmt(12, 31, yr))

    return ("", "")


def strip_tags(text):
    """Remove {link}, {text}, {link 1| link 2}, {description | video} etc."""
    return re.sub(r'\{[^}]*\}', '', text).strip().rstrip(',').strip()


def extract_headline(text):
    """Extract a headline string from a CV entry line.

    Rules:
    - If text begins with a 4-digit year prefix (year-prefixed entries like
      Artist's Books), strip the year tab/space prefix, then take text up to
      the first '. ' or end (truncated to 120 chars).
    - If there is a quoted title "like this", use that.
    - Otherwise: first sentence (split on '. ') truncated to 120 chars.
    """
    t = strip_tags(text).strip()

    # Year-prefixed entry: e.g. "2013    P.o.E.M.M. The Album. Obx Labs..."
    year_prefix = re.match(r'^((?:19|20)\d{2})\s+(.+)', t)
    if year_prefix:
        rest = year_prefix.group(2).strip()
        # Take up to first '. ' boundary (whole sentence)
        first_sentence = re.split(r'\.\s', rest)[0]
        return first_sentence[:120].strip()

    # Quoted title
    quoted = re.search(r'"([^"]+)"', t)
    if quoted:
        title = quoted.group(1).rstrip('.,;').strip()
        return title[:120]

    # Fallback: first sentence
    first_sentence = re.split(r'\.\s', t)[0]
    return first_sentence[:120].strip()


def parse_cv_txt():
    """Parse cv.txt and return a list of 6-tuples:
    (start_date, end_date, headline, full_entry_text, project, group)

    Parses only the sections listed in PARSE_SECTIONS.
    """
    cv_path = Path(__file__).parent / "cv.txt"
    raw_text = cv_path.read_text(encoding='utf-8')

    # Build a set of all known section headers (stripped) for boundary detection
    known_headers = set(s.strip() for s in ALL_CV_SECTIONS)

    # Split the file into lines; collect non-empty logical entries per section
    lines = raw_text.splitlines()

    # Walk through lines to identify section blocks
    # A section header is a line that exactly matches (after stripping) a known header
    sections = {}      # section_name → [entry_text, ...]
    current_section = None

    for line in lines:
        stripped = line.strip()

        if stripped in known_headers:
            current_section = stripped
            if current_section not in sections:
                sections[current_section] = []
            continue

        # Skip blank lines between sections/entries
        if not stripped:
            continue

        # If we are inside a section we want to parse, collect entries
        if current_section in PARSE_SECTIONS:
            sections[current_section].append(stripped)

    # Now convert collected entries into row tuples
    rows = []
    for section_name, group_name in PARSE_SECTIONS.items():
        entries = sections.get(section_name, [])
        for entry_text in entries:
            start, end = parse_date(entry_text)
            headline = extract_headline(entry_text)
            description = strip_tags(entry_text)
            rows.append((start, end, headline, description, "", group_name))

    return rows


# ─────────────────────────────────────────────────────────────────────────────
# HARDCODED ROWS
# (Employment, Education, Honors, Creative Works, Keynotes, Group Exhibitions,
#  Productions, Funding PI/Co-I/Internal, Courses Taught, Supervision, Service)
# ─────────────────────────────────────────────────────────────────────────────

rows = [

    # ── EMPLOYMENT ─────────────────────────────────────────────────────────
    ("06/01/2019", PRESENT,
     "Special Advisor to the Provost, Indigenous Spaces and Donor Relations",
     "Concordia University, Montreal, QC",
     "Concordia", "Employment"),

    ("06/01/2014", PRESENT,
     "University Research Chair (Tier 1) in Computational Media and the Indigenous Future Imaginary",
     "Concordia University, Montreal, QC",
     "Concordia", "Employment"),

    ("06/01/2014", PRESENT,
     "Professor of Computation Arts",
     "Dept. of Design and Computation Arts, Faculty of Fine Arts, Concordia University",
     "Concordia", "Employment"),

    ("06/01/2008", "05/31/2014",
     "Associate Professor of Computation Arts",
     "Dept. of Design and Computation Arts, Faculty of Fine Arts, Concordia University",
     "Concordia", "Employment"),

    ("09/01/2008", "12/31/2013",
     "Director, Computation Arts Program",
     "Dept. of Design and Computation Arts, Faculty of Fine Arts, Concordia University",
     "Concordia", "Employment"),

    ("09/01/2002", "05/31/2007",
     "Assistant Professor of Computation Arts",
     "Dept. of Design and Computation Arts, Faculty of Fine Arts, Concordia University",
     "Concordia", "Employment"),

    ("09/01/1999", "08/31/2001",
     "Founder and Director of Research, Arts Alliance Laboratory",
     "San Francisco, CA",
     "Early Career", "Employment"),

    ("05/01/1997", "08/31/2003",
     "Advisor, Arts Alliance Ventures",
     "London, England",
     "Early Career", "Employment"),

    ("09/01/1996", "08/31/1999",
     "Member of Research Staff, Interval Research Corporation",
     "Palo Alto, CA",
     "Early Career", "Employment"),

    ("06/01/1995", "09/30/1995",
     "Interaction Designer, Fitch, Inc.",
     "San Francisco, CA",
     "Early Career", "Employment"),

    ("05/01/1994", "09/30/1994",
     "Conceptualizer, Associate Producer & Research Coordinator — Electric Carnival, Lollapalooza '94",
     "North American Tour",
     "Early Career", "Employment"),

    ("10/01/1993", "09/30/1994",
     "Interaction Designer, Interval Research Corporation",
     "Palo Alto, CA",
     "Early Career", "Employment"),

    ("09/01/1992", "09/30/1993",
     "Carnegie Research Fellow, Institute for Research on Learning",
     "Palo Alto, CA",
     "Early Career", "Employment"),

    ("04/01/1992", "06/30/1992",
     "Instructor, Stanford University — 'Critical Theories for an Electric Society'",
     "Undergraduate Special Course, Stanford, CA",
     "Early Career", "Employment"),

    # ── EDUCATION ──────────────────────────────────────────────────────────
    ("09/01/1994", "06/30/1997",
     "M.Phil. Design, Royal College of Art",
     "London, England",
     "Early Career", "Education"),

    ("09/01/1987", "06/30/1988",
     "Philosophy & Critical Theory, Freie Universität Berlin",
     "West Germany — DAAD Fellowship",
     "Early Career", "Education"),

    ("09/01/1985", "06/30/1991",
     "B.S. Symbolic Systems (Cognitive Science) + B.A. German Studies, Stanford University",
     "Palo Alto, CA",
     "Early Career", "Education"),

    # ── HONORS & AWARDS ────────────────────────────────────────────────────
    ("01/01/2025", "01/01/2025",
     "Jane Lombard Fellowship",
     "", "Recognition", "Honors"),

    ("01/01/2025", "01/01/2025",
     "SSHRC Impact Partnership Award",
     "Social Sciences and Humanities Research Council",
     "Recognition", "Honors"),

    ("01/01/2024", "01/01/2024",
     "SSHRC Impact Partnership Award Finalist",
     "", "Recognition", "Honors"),

    ("01/01/2023", "01/01/2023",
     "Outstanding Staff and Faculty Award, Concordia Alumni Association",
     "", "Recognition", "Honors"),

    ("01/01/2023", "01/01/2023",
     "American Indian Film Festival — Nominee, Best Animated Short (producer)",
     "", "Recognition", "Honors"),

    ("01/01/2022", "01/01/2022",
     "Provost Circle of Distinction, Concordia University",
     "", "Recognition", "Honors"),

    ("01/01/2021", "01/01/2021",
     "Fellow of the Royal Society of Canada",
     "", "Recognition", "Honors"),

    ("01/01/2021", "01/01/2021",
     "SAIO 50 for 50, Stanford American Indian Organization",
     "", "Recognition", "Honors"),

    ("01/01/2020", "01/01/2020",
     "Concordia University Research Chair Tier 1 (renewed)",
     "", "Recognition", "Honors"),

    ("01/01/2019", "01/01/2019",
     "IndieCade Festival — Nominee, Best Performance (producer)",
     "", "Recognition", "Honors"),

    ("01/01/2018", "01/01/2018",
     "MIT Press Resisting Reduction Essay Competition — Winner",
     "", "Recognition", "Honors"),

    ("01/01/2018", "01/01/2018",
     "Prix Ars Electronica — Honorary Mention",
     "", "Recognition", "Honors"),

    ("01/01/2015", "01/01/2015",
     "ELO Collection vol. 3 — Selection",
     "Electronic Literature Organization", "Recognition", "Honors"),

    ("01/01/2014", "01/01/2014",
     "Trudeau Foundation Fellowship",
     "", "Recognition", "Honors"),

    ("01/01/2014", "01/01/2014",
     "Concordia University Research Chair Tier 1",
     "", "Recognition", "Honors"),

    ("01/01/2014", "01/01/2014",
     "Great Concordians",
     "Concordia University", "Recognition", "Honors"),

    ("01/01/2014", "01/01/2014",
     "Inaugural Robert Coover Award — Best Work of Electronic Literature",
     "Electronic Literature Organization", "Recognition", "Honors"),

    ("01/01/2013", "01/01/2013",
     "imagineNATIVE Festival — Best New Media (producer)",
     "", "Recognition", "Honors"),

    ("01/01/2012", "01/01/2012",
     "Ashoka Changemakers Award, J.W. McConnell Family Foundation",
     "", "Recognition", "Honors"),

    ("01/01/2012", "01/01/2012",
     "Electronic Literature Organization — Jury Award",
     "", "Recognition", "Honors"),

    ("01/01/2011", "01/01/2011",
     "ELO Collection vol. 2 — Selection",
     "", "Recognition", "Honors"),

    ("01/01/2010", "01/01/2010",
     "imagineNATIVE Festival — Best New Media (producer)",
     "", "Recognition", "Honors"),

    ("01/01/2009", "01/01/2009",
     "imagineNATIVE Festival — Best New Media (producer)",
     "", "Recognition", "Honors"),

    ("01/01/2000", "01/01/2000",
     "Prix Ars Electronica — Honorary Mention",
     "Digital Language, FILE Festival", "Recognition", "Honors"),

    ("01/01/1994", "01/01/1994",
     "Royal College of Art Scholarship",
     "", "Recognition", "Honors"),

    ("01/01/1986", "01/01/1986",
     "Freie Universität – Stanford University DAAD Fellowship",
     "", "Recognition", "Honors"),

    # ── CREATIVE WORKS (P.o.E.M.M. + major installations) ─────────────────
    ("01/01/1995", "12/31/1995",
     "Aura",
     "Interactive installation. With E. Brechin and R. Strein. Mac OS, custom electronics, metal plinth, video projector, vellum.",
     "Creative", "Creative Works"),

    ("01/01/1996", "12/31/1996",
     "WordNozzle: Firehose",
     "Interactive installation. Mac OS, custom Lingo, firehose, nozzle, projection, custom electronics.",
     "Creative", "Creative Works"),

    ("01/01/1999", "12/31/1999",
     "I Know What You're Thinking",
     "Screen interactive. Mac OS, custom Lingo.",
     "Creative", "Creative Works"),

    ("01/01/2000", "12/31/2000",
     "ActiveText: The Installation",
     "With A. Weyers. Interactive installation. Windows OS, custom C++.",
     "Creative", "Creative Works"),

    ("01/01/2002", "12/31/2002",
     "Thanksgiving Address: Greetings to the Technological World",
     "Screen interactive. Flash, custom Actionscript. Co-created with S. T. Fragnito.",
     "AbTeC", "Creative Works"),

    ("01/01/2005", "12/31/2005",
     "Cityspeak",
     "Massively multi-user public space chat system. With B. Nadeau, M. Lévesque, E. Zananiri and L. Bellemare.",
     "Creative", "Creative Works"),

    ("01/01/2007", "12/31/2007",
     "What They Speak When They Speak To Me",
     "With B. Nadeau & E. Zananiri. Interactive touchwork. Windows OS, custom Java.",
     "Creative", "Creative Works"),

    ("01/01/2007", "12/31/2007",
     "Intralocutor",
     "With Y. Assogba, D. Bouchard, and B. Nadeau. Interactive installation. Windows OS, custom Java, projection.",
     "Creative", "Creative Works"),

    ("01/01/2010", "12/31/2010",
     "The Great Migration",
     "With B. Nadeau and C. Dupont. Interactive touchwork with large-scale print. Mac OS, custom Java.",
     "Creative", "Creative Works"),

    ("01/01/2010", "12/31/2010",
     "Migration (P.o.E.M.M.)",
     "With C. Dupont and B. Nadeau. Interactive touchwork poem for iPad/iPhone. iOS.",
     "Creative", "Creative Works"),

    ("01/01/2011", "12/31/2011",
     "White / Choice / Bastard (P.o.E.M.M.)",
     "Interactive touchwork poems. With C. Gratton, S. Maheu and B. Nadeau. iOS, Objective-C.",
     "Creative", "Creative Works"),

    ("01/01/2011", "12/31/2011",
     "No Choice About the Terminology",
     "With E. Zananiri and B. Nadeau. Interactive touchwork with large-scale print. Commissioned by imagineNATIVE.",
     "Creative", "Creative Works"),

    ("01/01/2012", "12/31/2012",
     "Rattlesnakes (P.o.E.M.M.)",
     "With S. Maheu and B. Nadeau. Interactive touchwork poem for iPad/iPhone. iOS, Objective-C.",
     "Creative", "Creative Works"),

    ("01/01/2012", "12/31/2012",
     "The Summer the Rattlesnakes Came",
     "With B. Nadeau. Interactive touchwork with large-scale print. Mac OS, custom Java.",
     "Creative", "Creative Works"),

    ("01/01/2013", "12/31/2013",
     "Death (P.o.E.M.M.)",
     "With S. Maheu and B. Nadeau. Interactive touchwork poem for iPad/iPhone. iOS, Objective-C.",
     "Creative", "Creative Works"),

    ("01/01/2013", "12/31/2013",
     "The World That Surrounds You Wants Your Death",
     "With B. Nadeau. Interactive touchwork with large-scale print. Mac OS, custom Java.",
     "Creative", "Creative Works"),

    # ── KEYNOTES ───────────────────────────────────────────────────────────
    ("03/02/2023", "03/02/2023",
     "Keynote: Future Imaginaries of Abundant Intelligences",
     "Interaction 23, Zürich, Switzerland.",
     "IIF", "Keynotes"),

    ("10/22/2021", "10/22/2021",
     "Keynote: Creating Future Imaginaries through Indigenous AI",
     "EPIC Conference 2021. Ethnopraxis in Industry.",
     "IIF", "Keynotes"),

    ("09/24/2021", "09/24/2021",
     "Keynote: 22nd-Century Proto-typing",
     "PIVOT 2021, Pluriversal Design SIG / OCAD University, Toronto, ON.",
     "IIF", "Keynotes"),

    ("01/23/2021", "01/23/2021",
     "Marshall McLuhan Lecture: Expansive, Embracing, Evolving — Beyond Impoverished Intelligences",
     "Transmediale Festival, Berlin, Germany.",
     "IIF", "Keynotes"),

    ("08/21/2019", "08/21/2019",
     "Keynote: Making Kin with the Machines",
     "With Suzanne Kite. MUTEK Festival, Montreal, QC.",
     "IIF", "Keynotes"),

    ("10/10/2018", "10/10/2018",
     "Keynote: White Supremacy — It's Not Just for People Anymore!",
     "Association of Internet Researchers (AoIR), UQAM, Montreal, QC.",
     "Research", "Keynotes"),

    ("08/13/2018", "08/18/2018",
     "Keynote: Mod Cyberspace, Mod the World!",
     "With Skawennati. Electronic Literature Organization Annual Conference, UQAM, Montreal, QC.",
     "Creative", "Keynotes"),

    ("10/31/2017", "10/31/2017",
     "Opening Keynote: Decolonizing Immersive Media",
     "Enterprising Culture Conference, CFC Media Lab, Corus Quay, Toronto, ON.",
     "IIF", "Keynotes"),

    ("10/28/2016", "10/28/2016",
     "Keynote: An Orderly Assemblage of Biases — Computation as Cultural Material",
     "Crossing Boundaries, University of Lethbridge, AB.",
     "Research", "Keynotes"),

    ("10/06/2016", "10/06/2016",
     "Keynote: Populating the Future Imaginary — Visualizing Indigenous Futures",
     "International Visual Literacy Association Annual Conference, Concordia University, Montreal, QC.",
     "IIF", "Keynotes"),

    ("02/01/2014", "02/28/2014",
     "Keynote: The P.o.E.M.M. Cycle — First Reflections",
     "New Oceania Literary Series, University of Hawai'i at Mānoa, Honolulu, HI.",
     "Creative", "Keynotes"),

    ("09/14/2013", "09/14/2013",
     "Talk: The Future Imaginary",
     "TEDxMontreal 2013, Société des Arts Technologiques, Montréal, QC.",
     "IIF", "Keynotes"),

    # ── GROUP EXHIBITIONS (selected) ───────────────────────────────────────
    ("09/17/2022", "12/11/2022",
     "Poets with a Video Camera: Videopoetry 1980–2020",
     "Surrey Art Gallery, Surrey, B.C. Curator: Tom Konyves.",
     "Creative", "Group Exhibitions"),

    ("04/23/2020", "06/21/2020",
     "Kahwatsiretátie: Teionkwariwaienna Tekariwaiennawahkòntie",
     "Biennale d'art contemporain autochtone, Montreal.",
     "AbTeC", "Group Exhibitions"),

    ("01/01/2016", "04/30/2016",
     "Electronic Literature: A Matter of Bits",
     "Stedman Gallery, Rutgers-Camden Center for the Arts, Camden NJ. Curator: Jim Brown.",
     "Creative", "Group Exhibitions"),

    ("06/01/2014", "09/30/2014",
     "Poetic Codings (San Jose ICA)",
     "San Jose Institute of Contemporary Art, San Jose, CA. Curator: Jody Zellen.",
     "Creative", "Group Exhibitions"),

    ("09/01/2013", "09/30/2013",
     "Les littératures numériques d'hier à demain",
     "Bibliothèque Nationale Française, Paris, France.",
     "Creative", "Group Exhibitions"),

    ("07/01/2013", "09/30/2013",
     "Signs for Sounds (Sunderland)",
     "Sunderland Museum and Art Gallery, Sunderland, U.K. Curator: Jeremy Theophilus.",
     "Creative", "Group Exhibitions"),

    ("06/01/2008", "08/31/2008",
     "SEND: Conversations in Evolving Media",
     "Institute for Contemporary Art, Portland, ME. Curator: Linda L. Lambertson.",
     "Creative", "Group Exhibitions"),

    ("07/01/2007", "08/31/2008",
     "Terminal Zero One",
     "International Terminal, Pearson International Airport, Toronto, ON. Year Zero One Collective.",
     "Creative", "Group Exhibitions"),

    ("09/01/2000", "08/31/2002",
     "Print on Screen",
     "Ars Electronica Center, Linz, Austria.",
     "Creative", "Group Exhibitions"),

    ("03/01/1995", "03/31/1995",
     "SelfStorage",
     "Curators: Laurie Anderson and Brian Eno. Art Angel, Wimberley, London, England.",
     "Creative", "Group Exhibitions"),

    # ── PRODUCTIONS (AbTeC / Skins) ────────────────────────────────────────
    ("09/01/2008", "06/30/2009",
     "Skins 1.0: Workshop on Aboriginal Storytelling and Video Game Design",
     "With Skawennati. Kahnawake Survival School, Kahnawake First Nation, QC.",
     "AbTeC", "Productions"),

    ("08/01/2011", "08/31/2011",
     "Skins 2.0: Summer Institute on Aboriginal Storytelling and Video Game Design",
     "With Skawennati. Concordia University, Montreal, QC.",
     "AbTeC", "Productions"),

    ("03/01/2012", "08/31/2012",
     "Skins 3.0: Extended Play",
     "With Skawennati. Concordia University & Kahnawake Education Centre.",
     "AbTeC", "Productions"),

    ("05/01/2013", "06/30/2013",
     "Skins 4.0: World Domination",
     "With Skawennati. Concordia University & Kahnawake Education Centre.",
     "AbTeC", "Productions"),

    ("07/01/2017", "08/31/2017",
     "Skins 5.0: Kanaeokana/He Au Hou — Making Mo'olelo Through Video Games",
     "With Skawennati. Hālau 'Īnana, Kamehameha Schools, Honolulu, HI.",
     "AbTeC", "Productions"),

    ("07/01/2017", "08/31/2017",
     "Skins 6.0: Making Mo'olelo Through Video Games 2",
     "With Skawennati. Hālau 'Īnana, Kamehameha Schools, Honolulu, HI.",
     "AbTeC", "Productions"),

    ("01/01/2009", PRESENT,
     "AbTeC Island",
     "Second Life island and exhibition venue. Aboriginal Territories in Cyberspace. Producer.",
     "AbTeC", "Productions"),

    ("01/01/2009", "12/31/2009",
     "Otsi:! Rise of the Kanien'keha:ka Legends",
     "Video game. Unreal Engine. Montreal: Aboriginal Territories in Cyberspace. Producer.",
     "AbTeC", "Productions"),

    ("01/01/2011", "12/31/2011",
     "The Adventure of Skahion:ati: Legend of the Stone Giants",
     "Video game. Unity 3D. Montreal: Aboriginal Territories in Cyberspace. Producer.",
     "AbTeC", "Productions"),

    ("01/01/2012", "12/31/2012",
     "Skahion:ati: Rise of the Kanien'keha:ka Legends",
     "Video game. Unity. Montreal: Aboriginal Territories in Cyberspace. Producer.",
     "AbTeC", "Productions"),

    ("01/01/2011", "12/31/2013",
     "TimeTraveller™ (Episodes I–IX)",
     "Machinima series with Skawennati. Second Life. Montreal: Aboriginal Territories in Cyberspace. Executive Producer.",
     "AbTeC", "Productions"),

    ("01/01/2013", "12/31/2013",
     "Ienién:te and the Peacemaker's Wampum",
     "Video game. Construct 2. Montreal: Aboriginal Territories in Cyberspace. Producer.",
     "AbTeC", "Productions"),

    ("01/01/2017", "12/31/2017",
     "He Ao Hou: A New World",
     "Video game. Unity. Honolulu and Montreal: Aboriginal Territories in Cyberspace. Producer.",
     "AbTeC", "Productions"),

    ("01/01/2017", "12/31/2017",
     "Wao Kanaka: In the Realm of the Humans",
     "Video game. Unity. Honolulu and Montreal: Aboriginal Territories in Cyberspace.",
     "AbTeC", "Productions"),

    ("01/01/2017", "12/31/2017",
     "The Peacemaker Returns / She Falls for Ages",
     "Machinima by Skawennati. Second Life. Montreal: Aboriginal Territories in Cyberspace. Executive Producer.",
     "AbTeC", "Productions"),

    ("01/01/2022", "12/31/2022",
     "When the Earth Began: The Way of the Skydwellers",
     "Film. Kanien'kehá:ka Onkwawén:na Raotitióhkwa Language and Cultural Center & AbTeC. Executive Producer.",
     "AbTeC", "Productions"),

    ("01/01/2022", "12/31/2022",
     "Past Future Forward: The Making of a Hawaiian Video Game",
     "Film. Director & Producer. Hawaiian International Film Festival (HIFF), Nov. 2022.",
     "AbTeC", "Productions"),

    # ── FUNDING (PI) — EXTERNAL ────────────────────────────────────────────
    ("11/24/2025", "11/24/2025",
     "Impact Partnership Award",
     "$50,000. Social Sciences and Humanities Research Council.",
     "Recognition", "Funding (PI)"),

    ("04/01/2025", "03/31/2029",
     "Transmediating Indigenous Art",
     "$378,974. Social Sciences and Humanities Research Council.",
     "Research", "Funding (PI)"),

    ("08/15/2024", "08/14/2026",
     "An Abundant Data Trust",
     "$284,000. The Schmidt Family Foundation — 11th Hour Project.",
     "AI", "Funding (PI)"),

    ("03/01/2023", "02/28/2029",
     "Abundant Intelligences: Expanding AI through Indigenous Knowledge Systems",
     "$22,830,281. New Frontiers in Research Fund.",
     "AI", "Funding (PI)"),

    ("06/01/2023", "05/30/2025",
     "Foundations of Abundant Intelligences",
     "$675,000. The MacArthur Foundation.",
     "AI", "Funding (PI)"),

    ("04/01/2023", "03/31/2029",
     "Partnership for Abundant Intelligences",
     "$2,499,875. Social Sciences and Humanities Research Council.",
     "AI", "Funding (PI)"),

    ("04/01/2023", "03/31/2029",
     "Indigenous Futures Research Centre",
     "$450,609. Canada Foundation for Innovation.",
     "IIF", "Funding (PI)"),

    ("01/01/2023", "07/01/2023",
     "Abundant Intelligences Residency 1",
     "$26,000. Montalvo Arts Center.",
     "AI", "Funding (PI)"),

    ("08/15/2022", "08/14/2023",
     "Abundant Intelligences: Year 01",
     "$98,000. The Schmidt Family Foundation — 11th Hour Project.",
     "AI", "Funding (PI)"),

    ("03/15/2022", "10/30/2022",
     "Abundant Intelligences",
     "$20,000. Social Sciences and Humanities Research Council.",
     "AI", "Funding (PI)"),

    ("04/01/2022", "03/03/2024",
     "L'art autochtone dans les environnements virtuels",
     "$221,905. Fonds de recherche Société et culture Québec.",
     "AbTeC", "Funding (PI)"),

    ("01/15/2022", "01/15/2025",
     "Expanding Skins Workshops on Aboriginal Storytelling in Digital Media",
     "$498,000. Hewitt Foundation.",
     "AbTeC", "Funding (PI)"),

    ("01/25/2021", "03/30/2022",
     "Building Capacity with the Skins Workshops",
     "$30,000. Indigenous Screen Office.",
     "AbTeC", "Funding (PI)"),

    ("03/01/2019", "12/31/2019",
     "Building Indigenous Capacity & Community in Digital Media Sectors",
     "$250,000. Canada Council for the Arts. Co-lead.",
     "AbTeC", "Funding (PI)"),

    ("01/15/2019", "06/01/2019",
     "Indigenous Protocol and Artificial Intelligence Workshops",
     "$49,026. Social Sciences and Humanities Research Council.",
     "AI", "Funding (PI)"),

    ("09/01/2018", "06/01/2019",
     "Indigenous Protocol and Artificial Intelligence Workshops",
     "$80,000. Canadian Institute for Advanced Research.",
     "AI", "Funding (PI)"),

    ("04/01/2018", "12/31/2018",
     "Skins 6.0: Kanaeokana — Workshop on Aboriginal Storytelling and Video Game Design",
     "$389,000. Kanaeokana Network (Hawaii).",
     "AbTeC", "Funding (PI)"),

    ("04/01/2017", "12/31/2017",
     "Skins 5.0: Kanaeokana — Workshop on Aboriginal Storytelling and Video Game Design",
     "$187,000. Kanaeokana Network (Hawaii).",
     "AbTeC", "Funding (PI)"),

    ("07/01/2016", "07/01/2017",
     "Blueberry Pie in the Martian Sky",
     "$60,000. Canada Council for the Arts. Research Director / Executive Producer. Artist: Scott Benesiinaabandan.",
     "AbTeC", "Funding (PI)"),

    ("04/01/2015", "03/31/2022",
     "Initiative for Indigenous Futures Partnership",
     "$2,491,613. Social Sciences and Humanities Research Council.",
     "IIF", "Funding (PI)"),

    ("06/01/2014", "05/31/2017",
     "Trudeau Fellowship",
     "$225,000. Pierre Elliott Trudeau Foundation.",
     "Recognition", "Funding (PI)"),

    ("06/01/2014", "11/03/2014",
     "Initiative for Indigenous Futures — Letter of Intent",
     "$20,000. Social Sciences and Humanities Research Council.",
     "IIF", "Funding (PI)"),

    ("07/01/2012", "09/30/2013",
     "The P.o.E.M.M. Cycle 6–10",
     "$58,000. Canada Council for the Arts. Artist.",
     "PoEMM", "Funding (PI)"),

    ("04/01/2012", "03/03/2015",
     "TyP3: Protocoles, Plateformes, et Publics pour textes digitaux",
     "$163,556. Fonds québécois de la recherche sur la société et la culture.",
     "Research", "Funding (PI)"),

    ("04/15/2012", "04/15/2013",
     "Skins Workshop",
     "$2,500. J. W. McConnell Family Foundation.",
     "AbTeC", "Funding (PI)"),

    ("04/01/2012", "12/30/2013",
     "Abstracted Pow Wow",
     "$59,000. Canada Council for the Arts. Research Director / Executive Producer. Artist: Scott Benesiinaabandan.",
     "AbTeC", "Funding (PI)"),

    ("04/01/2011", "03/30/2014",
     "Skins, Storytellers and Second Lives: A Partnership for Developing Aboriginal New Media",
     "$367,000. Social Sciences and Humanities Research Council.",
     "AbTeC", "Funding (PI)"),

    ("04/01/2010", "06/30/2011",
     "Words Found on an Empty Beach",
     "$38,000. Canada Council for the Arts. Artist.",
     "Creative", "Funding (PI)"),

    ("07/01/2010", "12/31/2010",
     "P.o.E.M.M. Cycle 1–5",
     "$55,000. Canada Council for the Arts. Artist.",
     "PoEMM", "Funding (PI)"),

    ("07/01/2009", "06/30/2010",
     "TimeTraveller™",
     "$60,000. Canada Council for the Arts. Research Director / Executive Producer. Artist: Skawennati Tricia Fragnito.",
     "AbTeC", "Funding (PI)"),

    ("07/01/2009", "06/30/2012",
     "Ecriture complex: nouveaux modèles pour la typographie informatique",
     "$95,000. Fonds québécois de la recherche sur la société et la culture.",
     "Research", "Funding (PI)"),

    ("04/01/2009", "03/31/2012",
     "Building Aboriginal Territories in Cyberspace",
     "$149,000. Fonds québécois de la recherche sur la société et la culture.",
     "AbTeC", "Funding (PI)"),

    ("04/01/2007", "03/31/2010",
     "Between Reading and Looking: Writing-Designing-Programming with Computational Media",
     "$193,000. Social Sciences and Humanities Research Council.",
     "Research", "Funding (PI)"),

    ("04/01/2006", "03/30/2009",
     "Aboriginal Territories in Cyberspace",
     "$239,000. Social Sciences and Humanities Research Council.",
     "AbTeC", "Funding (PI)"),

    ("06/01/2005", "01/06/2007",
     "Software for Interactive, Variable and Performative Texts",
     "$62,000. Hexagram Institute for Research/Creation in Media Arts and Technologies.",
     "Research", "Funding (PI)"),

    ("05/01/2004", "04/30/2007",
     "The Next Text",
     "$39,000. Fonds québécois de la recherche sur la société et la culture.",
     "Research", "Funding (PI)"),

    ("06/01/2004", "01/05/2005",
     "Writing the Next Text",
     "$39,000. Hexagram Institute for Research/Creation in Media Arts and Technologies.",
     "Research", "Funding (PI)"),

    ("01/15/1995", "09/30/1995",
     "Life is Bait",
     "$11,000. Arts Council of England. Co-grant holder.",
     "Early Career", "Funding (PI)"),

    # ── FUNDING (Co-I) — EXTERNAL ──────────────────────────────────────────
    ("04/01/2022", "03/30/2029",
     "R3AI: Shifting Paradigms for a Robust, Reasoning, & Responsible AI",
     "$124,000,000. Canada First Research Excellence Fund. Core Applicant. PI: Luc Vinet.",
     "Research", "Funding (Co-I)"),

    ("04/01/2022", "03/30/2024",
     "Meeting 30×30 and the Paris Agreement: Leveraging Digital Solutions for Nature-Based Solutions",
     "$256,623. Natural Sciences and Engineering Research Council. PI: Eliane Ubalijoro.",
     "Research", "Funding (Co-I)"),

    ("03/31/2022", "03/30/2028",
     "Infrastructure Beyond Extractivism: Material Approaches to Restoring Indigenous Jurisdiction",
     "$2,296,866. Social Sciences and Humanities Research Council. PI: Dayna Scott.",
     "IIF", "Funding (Co-I)"),

    ("03/31/2021", "03/30/2023",
     "Jurisdiction Back: Infrastructure beyond Extractivism",
     "$246,725. New Frontiers in Research Fund. PI: Dayna Scott.",
     "IIF", "Funding (Co-I)"),

    ("04/01/2020", "03/31/2027",
     "Hexagram Strategic Cluster",
     "$1,827,000. Fonds de recherche du Québec Société et culture. PI: Jean Dubois.",
     "Research", "Funding (Co-I)"),

    ("04/01/2019", "03/31/2024",
     "The Land as our Teacher: Land-based Pedagogy for/by Indigenous Youth",
     "$333,000. Social Sciences and Humanities Research Council. PI: Elizabeth Fast.",
     "AbTeC", "Funding (Co-I)"),

    ("04/01/2018", "12/31/2025",
     "Inuit Futures in Arts Leadership: The Pilimmaksarniq/Pijariuqsarniq Project",
     "$2,499,774. Social Sciences and Humanities Research Council. PI: Heather Igliolorte.",
     "IIF", "Funding (Co-I)"),

    ("04/01/2017", "03/23/2024",
     "Six Seasons of the Asiniskow Ithiniwak: Reclamation, Regeneration, and Reconciliation",
     "$2,500,000. Social Sciences and Humanities Research Council. PI: Mavis Reimer.",
     "IIF", "Funding (Co-I)"),

    ("04/01/2016", "03/23/2019",
     "A First Peoples Storytelling Exchange: Intersection College and Community Circles",
     "$240,000. Social Sciences and Humanities Research Council. PI: Susan Briscoe.",
     "AbTeC", "Funding (Co-I)"),

    ("04/01/2014", "03/03/2019",
     "HexagramCIAM – Centre Interuniversitaire des Arts Médiatiques",
     "$1,048,500. Fonds québécois de la recherche sur la société et la culture. PI: Christopher Salter.",
     "Research", "Funding (Co-I)"),

    ("04/01/2013", "03/30/2014",
     "GRAND: Graphics, Animation & New Media — Collaborating Network Investigator Grant",
     "$18,000. Networks of Centres of Excellence of Canada. PI: Kellogg Booth.",
     "Research", "Funding (Co-I)"),

    ("04/01/2012", "03/30/2013",
     "GRAND: Graphics, Animation & New Media — Collaborating Network Investigator Grant",
     "$10,000. Networks of Centres of Excellence of Canada. PI: Kellogg Booth.",
     "Research", "Funding (Co-I)"),

    ("04/01/2011", "03/30/2014",
     "Hexagram CIAM",
     "$367,000. Fonds Québécois de la Recherche sur la société et la culture. PIs: Nicolas Reeves, Giséle Trudel.",
     "Research", "Funding (Co-I)"),

    ("04/01/2011", "03/30/2012",
     "GRAND: Graphics, Animation & New Media — Collaborating Network Investigator Grant",
     "$6,000. Networks of Centres of Excellence of Canada. PI: Kellogg Booth.",
     "Research", "Funding (Co-I)"),

    ("04/01/2008", "03/31/2011",
     "Migration, Memory, Media: Emergent Technologies for Interactive Narrative Storytelling",
     "$119,000. Fonds québécois de la recherche sur la société et la culture. PI: Matt Soar.",
     "Research", "Funding (Co-I)"),

    ("04/01/2006", "03/30/2007",
     "Mobile Digital Commons Network Phase II",
     "$1,152,000. Heritage Canada. PIs: Michael Longford, Sara Diamond.",
     "Research", "Funding (Co-I)"),

    ("05/01/2004", "04/30/2007",
     "Expanding the Interface",
     "$135,000. Fonds québécois de la recherche sur la société et la culture. PI: Michael Longford.",
     "Research", "Funding (Co-I)"),

    ("08/01/2004", "03/31/2005",
     "Mobile Digital Commons Network",
     "$422,000. Heritage Canada. PIs: Michael Longford, Sara Diamond.",
     "Research", "Funding (Co-I)"),

    # ── FUNDING (INTERNAL) ─────────────────────────────────────────────────
    ("06/01/2019", "05/31/2025",
     "Concordia University Research Chair (Tier 1)",
     "$275,000. Concordia University.",
     "Concordia", "Funding (Internal)"),

    ("02/13/2019", "10/02/2019",
     "Archiving Indigenous Digital Arts Conference",
     "$1,800. Centre for Interdisciplinary Studies in Culture and Society, Concordia University.",
     "Concordia", "Funding (Internal)"),

    ("10/01/2019", "10/01/2019",
     "Archiving Indigenous Digital Arts Conference",
     "$5,965. Gail and Stephen A. Jarislowsky Institute for Studies in Canadian Art.",
     "Concordia", "Funding (Internal)"),

    ("10/31/2017", "08/01/2018",
     "Future Imaginary Lecture Series",
     "$5,000. Concordia University.",
     "IIF", "Funding (Internal)"),

    ("11/01/2016", "10/31/2017",
     "Aid to Research Related Events — Future Imaginary Lecture Series",
     "$5,000. Concordia University.",
     "IIF", "Funding (Internal)"),

    ("06/01/2014", "05/31/2019",
     "Concordia University Research Chair (Tier 1)",
     "$275,000. Concordia University.",
     "Concordia", "Funding (Internal)"),

    ("10/01/2012", "09/30/2014",
     "Game Designer-in-Residency Program",
     "$100,000. Office of Research, Research Development Fund.",
     "Concordia", "Funding (Internal)"),

    ("01/10/2012", "09/30/2014",
     "Strategy to Frame and Strengthen Production Based Game Research",
     "$50,000. Concordia University.",
     "Concordia", "Funding (Internal)"),

    ("01/11/2011", "10/31/2012",
     "Vital to the General Public Welfare: An Exhibition of Research/Creation Outcomes",
     "$5,000. Concordia University.",
     "Creative", "Funding (Internal)"),

    ("10/01/2010", "09/30/2011",
     "Aboriginal Territories in Cyberspace: First Contact",
     "$5,000. Office of Research ARRE.",
     "AbTeC", "Funding (Internal)"),

    ("03/18/2010", "03/30/2010",
     "Skins Summer Institute",
     "$100,000. Office of Research, Research Development Fund. Co-investigator: Skawennati Tricia Fragnito.",
     "AbTeC", "Funding (Internal)"),

    ("01/01/2004", "12/31/2011",
     "SSHRC Travel Grants",
     "$10,000. Fine Arts Faculty. Six separate grants.",
     "Research", "Funding (Internal)"),

    ("04/01/2004", "03/30/2005",
     "Participatory Tangible Board",
     "$50,000. Fine Arts-Engineering Seed Grants.",
     "Research", "Funding (Internal)"),

    ("04/01/2004", "03/30/2005",
     "Saying Red: Integrating Video Objects and Dynamic Typography",
     "$50,000. Fine Arts-Engineering Seed Grants.",
     "Creative", "Funding (Internal)"),

    ("01/01/2004", "12/31/2008",
     "Hexagram Travel Grants",
     "$8,000. Fine Arts Faculty. Four separate grants.",
     "Research", "Funding (Internal)"),

    # ── COURSES TAUGHT ─────────────────────────────────────────────────────
    ("01/01/2024", "04/30/2024",
     "DART634 Indigenous Futurisms",
     "Graduate seminar. Concordia University, Winter 2024.",
     "Concordia", "Courses Taught"),

    ("01/01/2023", "04/30/2023",
     "DART634 Indigenous Futurisms",
     "Graduate seminar. Concordia University, Winter 2023.",
     "Concordia", "Courses Taught"),

    ("01/01/2023", "04/30/2023",
     "DART630 The Future Imaginary",
     "Graduate seminar. Concordia University, Winter 2023.",
     "Concordia", "Courses Taught"),

    ("01/01/2022", "04/30/2022",
     "DART630 The Future Imaginary",
     "Graduate seminar. Concordia University, Winter 2022.",
     "Concordia", "Courses Taught"),

    ("01/01/2021", "04/30/2021",
     "DART630 The Future Imaginary",
     "Graduate seminar. Concordia University, Winter 2021.",
     "Concordia", "Courses Taught"),

    ("01/01/2019", "04/30/2019",
     "DART630 The Future Imaginary",
     "Graduate seminar. Concordia University, Winter 2019.",
     "Concordia", "Courses Taught"),

    ("09/01/2018", "12/31/2018",
     "CART 345 Computational Texts and Typography I",
     "Undergraduate course. Concordia University, Fall 2018.",
     "Concordia", "Courses Taught"),

    ("01/01/2018", "04/30/2018",
     "DART630 The Future Imaginary",
     "Graduate seminar. Concordia University, Winter 2018.",
     "Concordia", "Courses Taught"),

    ("09/01/2017", "12/31/2017",
     "CART 345 Computational Texts and Typography I",
     "Undergraduate course. Concordia University, Fall 2017.",
     "Concordia", "Courses Taught"),

    ("09/01/2016", "12/31/2016",
     "CART 253a/b Creative Computation I",
     "Undergraduate course, two sections. Concordia University, Fall 2016.",
     "Concordia", "Courses Taught"),

    ("09/01/2015", "12/31/2015",
     "CART 253a/b Creative Computation I",
     "Undergraduate course, two sections. Concordia University, Fall 2015.",
     "Concordia", "Courses Taught"),

    ("09/01/2014", "12/31/2014",
     "CART 253a/b Creative Computation I",
     "Undergraduate course, two sections. Concordia University, Fall 2014.",
     "Concordia", "Courses Taught"),

    ("01/01/2013", "04/30/2013",
     "CART 345 Computational Texts & Typography I / CART 444 Portfolio Studio",
     "Undergraduate courses. Concordia University, Winter 2013.",
     "Concordia", "Courses Taught"),

    ("09/01/2012", "12/31/2012",
     "CART 253a/b Creative Computation I",
     "Undergraduate course, two sections. Concordia University, Fall 2012.",
     "Concordia", "Courses Taught"),

    ("01/01/2012", "04/30/2012",
     "CART 345 Computational Texts & Typography I / CART 444 Portfolio Studio",
     "Undergraduate courses. Concordia University, Winter 2012.",
     "Concordia", "Courses Taught"),

    ("09/01/2011", "12/31/2011",
     "CART 253aa/a Creative Computation I/II",
     "Undergraduate course, two sections. Concordia University, Fall 2011.",
     "Concordia", "Courses Taught"),

    ("01/01/2011", "04/30/2011",
     "CART 253aa/a Creative Computation I/II",
     "Undergraduate course, two sections. Concordia University, Winter 2011.",
     "Concordia", "Courses Taught"),

    ("09/01/2010", "12/31/2010",
     "CART 345 Computational Texts & Typography I",
     "Undergraduate course. Concordia University, Fall 2010.",
     "Concordia", "Courses Taught"),

    ("01/01/2008", "04/30/2008",
     "CART 253aa/a Creative Computation I/II",
     "Undergraduate course, two sections. Concordia University, Winter 2008.",
     "Concordia", "Courses Taught"),

    ("09/01/2007", "12/31/2007",
     "DART 503 Theories of Interactivity / CART 355c Topics in Kinetic Imagery (The Next Text)",
     "Graduate and undergraduate courses. Concordia University, Fall 2007.",
     "Concordia", "Courses Taught"),

    ("01/01/2007", "04/30/2007",
     "CART 253a/b Languages of Programming",
     "Undergraduate course, two sections. Concordia University, Winter 2007.",
     "Concordia", "Courses Taught"),

    ("09/01/2006", "12/31/2006",
     "DART 503 Theories of Interactivity / CART 355c Topics in Kinetic Imagery (The Next Text)",
     "Graduate and undergraduate courses. Concordia University, Fall 2006.",
     "Concordia", "Courses Taught"),

    ("01/01/2006", "04/30/2006",
     "CART 253a/aa The Languages of Programming",
     "Undergraduate course, two sections. Concordia University, Winter 2006.",
     "Concordia", "Courses Taught"),

    ("09/01/2005", "12/31/2005",
     "CART 355b Topics in Kinetic Imagery (The Next Text) / DART 503 Theories of Interactivity",
     "Undergraduate and graduate courses. Concordia University, Fall 2005.",
     "Concordia", "Courses Taught"),

    ("01/01/2005", "04/30/2005",
     "DFAR 253a/b The Languages of Programming",
     "Undergraduate course, two sections. Concordia University, Winter 2005.",
     "Concordia", "Courses Taught"),

    ("01/01/2004", "04/30/2004",
     "DFAR 452 TriMedia Productions / DFAR 353a The Languages of Programming",
     "Undergraduate courses. Concordia University, Winter 2004.",
     "Concordia", "Courses Taught"),

    ("09/01/2003", "12/31/2003",
     "DFAR 451 Interactive Media / DFAR 498 Bending Bits",
     "Undergraduate courses. Concordia University, Fall 2003.",
     "Concordia", "Courses Taught"),

    ("01/01/2003", "04/30/2003",
     "DFAR 353a/aa The Languages of Programming",
     "Undergraduate course, two sections. Concordia University, Winter 2003.",
     "Concordia", "Courses Taught"),

    ("09/01/2002", "12/31/2002",
     "DFAR 451a/b Interactive Media",
     "Undergraduate course, two sections. Concordia University, Fall 2002.",
     "Concordia", "Courses Taught"),

    # ── SUPERVISION ────────────────────────────────────────────────────────
    # Undergraduate (SYNTHETIC — replace with real data)
    ("01/01/2024", "12/31/2024",
     "Undergraduate [Student A] (Honours)",
     "SYNTHETIC. Honours thesis in computation arts and Indigenous futures. Concordia University.",
     "Concordia", "Undergraduate"),

    ("01/01/2022", "12/31/2023",
     "Undergraduate [Student B] (Honours)",
     "SYNTHETIC. Independent study in interactive media and land-based knowledge. Concordia University.",
     "Concordia", "Undergraduate"),

    ("01/01/2019", "12/31/2020",
     "Undergraduate [Student C] (Independent Study)",
     "SYNTHETIC. Creative coding and Indigenous language revitalization. Concordia University.",
     "AbTeC", "Undergraduate"),

    # Grad Certificate (SYNTHETIC — replace with real data)
    ("01/01/2023", "12/31/2024",
     "Grad Certificate [Student D]",
     "SYNTHETIC. Graduate certificate in computation arts. Concordia University.",
     "Concordia", "Grad Certificate"),

    ("01/01/2021", "12/31/2022",
     "Grad Certificate [Student E]",
     "SYNTHETIC. Graduate certificate in digital fabrication and Indigenous design. Concordia University.",
     "Concordia", "Grad Certificate"),

    # Postdoctoral Fellows
    ("01/01/2025", PRESENT,
     "Postdoc Melemaikalani Moniz",
     "Postdoctoral Fellow in Abundant Soils. Concordia University.",
     "AI", "Postdoc"),

    ("01/01/2024", "12/31/2026",
     "Postdoc Ceyda Yolgörmez",
     "Horizon Postdoctoral Fellow in Abundant Intelligences. Concordia University.",
     "AI", "Postdoc"),

    ("01/01/2019", "12/31/2021",
     "Postdoc Leuli Eschraghi",
     "Horizon Postdoctoral Fellow in Indigenous Futures. Concordia University.",
     "IIF", "Postdoc"),

    # Doctoral Advisees
    ("01/01/2023", PRESENT,
     "PhD Juliet Mackie",
     "Reconstituting Indigenous Identities through Portraiture and Storytelling. Concordia University.",
     "Concordia", "PhD"),

    ("01/01/2021", "12/31/2024",
     "PhD Mel Lefebvre",
     "Healing Through Ancestral Skin Marking: Traditional Tattooing as Healing and (Re)connection for Indigenous People. Concordia University.",
     "Concordia", "PhD"),

    ("01/01/2019", "12/31/2023",
     "PhD Jessica Barudin (Co-supervisor)",
     "Re-connecting Through Women's Teachings, Language and Movement. Concordia University.",
     "Concordia", "PhD"),

    ("01/01/2017", "12/31/2023",
     "PhD Suzanne Kite",
     "Lakota Epistemology, Performance Practice, and Digital Technology. Concordia University.",
     "AI", "PhD"),

    ("01/01/2017", PRESENT,
     "PhD Nafisa Sarwath (Secondary)",
     "Indigenous knowledge, resilience and adaptive capacity. Concordia University.",
     "Concordia", "PhD"),

    ("01/01/2016", "12/31/2021",
     "PhD Michelle Brown (Secondary)",
     "(Re)Coding Resurgence: Indigenous Digital Media Kinnections. University of Hawaii Mānoa.",
     "AbTeC", "PhD"),

    ("01/01/2007", "12/31/2014",
     "PhD Elizabeth LaPensée (Co-supervisor)",
     "Experiencing Stories: Narrative and Experience in Interactive Media. Simon Fraser University.",
     "AbTeC", "PhD"),

    ("01/01/2008", "12/31/2012",
     "PhD Miao Song (Secondary)",
     "Experiencing Stories: Narrative and Experience in Interactive Media. Concordia University.",
     "Concordia", "PhD"),

    ("01/01/2008", "12/31/2011",
     "PhD David Johnston (Secondary)",
     "Aesthetic Animism: Digital Poetry as Ontological Probe. Concordia University.",
     "Research", "PhD"),

    ("01/01/2005", "12/31/2008",
     "PhD Rozita Naghshin (Committee)",
     "Software Design as an Aesthetic Design Practice. Concordia University.",
     "Concordia", "PhD"),

    # Masters Thesis Advisees
    ("01/01/2022", PRESENT,
     "Masters Vanessa Racine",
     "Anishinaabe Love: Epistemologies & Videogames. Concordia University.",
     "AbTeC", "Masters"),

    ("01/01/2022", "12/31/2025",
     "Masters Tarcisio Cataldi Tegani (Committee)",
     "Speculative Vexillology: Exploring National Identity and Imagining Afro-Brazilian Futures through Flags. Concordia University.",
     "Concordia", "Masters"),

    ("01/01/2021", "12/31/2024",
     "Masters Caeleigh Lightning Long",
     "Wawêsiwîn: The Act of Dressing Up — A Research Cree-ation Project. Concordia University.",
     "AbTeC", "Masters"),

    ("01/01/2018", "12/31/2023",
     "Masters Sébastien Aubin",
     "Designing Culturally Grounded Cree Syllabaries. Concordia University.",
     "AbTeC", "Masters"),

    ("01/01/2018", "12/31/2021",
     "Masters Waylon Wilson",
     "Tuscarora Virtual Realities. Concordia University.",
     "AbTeC", "Masters"),

    ("01/01/2017", "12/31/2019",
     "Masters Maize Longboat",
     "Haudenosaunee Storytelling via Video Games. Concordia University.",
     "AbTeC", "Masters"),

    ("01/01/2016", "12/31/2020",
     "Masters Nicholas Gwyn Shulman (Co-supervisor)",
     "Network Arts: Seeing and Making Network Organisms. Concordia University.",
     "Research", "Masters"),

    ("01/01/2014", "12/31/2024",
     "Masters Morgan Kennedy",
     "Storied Indigeneity in Videogames: Post-Indian Warriors and Indie Japan. Concordia University.",
     "AbTeC", "Masters"),

    ("01/01/2012", "12/31/2015",
     "Masters Nikolaos Chandolias (Co-supervisor)",
     "KinectEcho: Gesture and Vocal Recognition in New Media, Interactive Art and Live Events. Concordia University.",
     "Research", "Masters"),

    ("01/01/2006", "12/31/2007",
     "Masters Leslie Plumb",
     "Transversal Entanglements: Research-Creation and the Design Process for Inflexions. Concordia University.",
     "Research", "Masters"),

    ("01/01/2004", "12/31/2008",
     "Masters Mia Song (Co-supervisor)",
     "Computer-Assisted Interactive Documentary and Performance Arts in Illimitable Space. Concordia University.",
     "Research", "Masters"),

    ("01/01/2003", "12/31/2005",
     "Masters Rozita Naghshin (Committee)",
     "CASE Tool Simplification Via Task-Sensitive Metaphor. Concordia University.",
     "Concordia", "Masters"),

    # ── SERVICE ────────────────────────────────────────────────────────────
    # Administrative roles
    ("01/01/2010", "12/31/2018",
     "Acting Chair",
     "Department of Design and Computation Arts, Concordia University. Various 1-to-2-week terms.",
     "Concordia", "Service"),

    ("09/01/2003", "08/31/2013",
     "Computation Arts Undergraduate Program Director / Co-director",
     "Department of Design and Computation Arts, Concordia University.",
     "Concordia", "Service"),

    ("09/01/2005", "08/31/2008",
     "Graduate Program Director",
     "Department of Design and Computation Arts, Concordia University.",
     "Concordia", "Service"),

    ("09/01/2003", "08/31/2014",
     "Computation Lab Director",
     "Department of Design and Computation Arts, Concordia University.",
     "Concordia", "Service"),

    # Departmental committees
    ("01/01/2008", "12/31/2020",
     "Personnel Committee",
     "Department of Design and Computation Arts, Concordia University.",
     "Concordia", "Service"),

    ("01/01/2002", "12/31/2014",
     "CART Curriculum Committee, Chair",
     "Department of Design and Computation Arts, Concordia University.",
     "Concordia", "Service"),

    ("01/01/2002", PRESENT,
     "Undergraduate and Graduate Admissions Committees",
     "Department of Design and Computation Arts, Concordia University.",
     "Concordia", "Service"),

    # Faculty committees
    ("01/01/2005", "12/31/2008",
     "Faculty Research Advisory Committee",
     "Faculty of Fine Arts, Concordia University.",
     "Concordia", "Service"),

    ("01/01/2005", "12/31/2008",
     "Hexagram-Concordia Steering Committee",
     "Concordia University.",
     "Concordia", "Service"),

    # University roles
    ("01/01/2020", PRESENT,
     "Co-director, Indigenous Futures Research Center",
     "Concordia University.",
     "IIF", "Service"),

    ("01/01/2020", PRESENT,
     "Indigenous Directions Leadership Council",
     "Concordia University.",
     "IIF", "Service"),

    ("01/01/2015", PRESENT,
     "Milieux Research Institute Advisory Board",
     "Concordia University.",
     "Concordia", "Service"),

    ("01/01/2015", "12/31/2018",
     "Senate Research Committee",
     "Concordia University.",
     "Concordia", "Service"),

    ("01/01/2009", "12/31/2018",
     "Board Member (Founding), Research Centre on Technoculture, Art and Gaming (TAG)",
     "Concordia University.",
     "Concordia", "Service"),

    ("01/01/2011", "12/31/2014",
     "Faculty Senate",
     "Concordia University.",
     "Concordia", "Service"),

    # External committees
    ("01/01/2025", "12/31/2028",
     "Advisory Board, Digital Technologies Research Centre",
     "National Research Council of Canada.",
     "Research", "Service"),

    ("01/01/2021", "12/31/2023",
     "Advisory Council on Artificial Intelligence",
     "Government of Canada.",
     "AI", "Service"),

    ("01/01/2020", "12/31/2022",
     "Canadian Commission for UNESCO Working Groups on AI Ethics & the Sustainable Development Goals",
     "",
     "AI", "Service"),

    ("01/01/2016", "12/31/2022",
     "Board Member, imagineNATIVE Film + Media Arts Festival",
     "",
     "AbTeC", "Service"),

    ("01/01/2010", "12/31/2016",
     "Founding Member, New Media Advisory Board, imagineNATIVE Film + Media Arts Festival",
     "",
     "AbTeC", "Service"),

    ("01/01/2006", PRESENT,
     "Co-Director, Aboriginal Territories in Cyberspace Research Network",
     "",
     "AbTeC", "Service"),

    ("01/01/2013", "12/31/2016",
     "First Peoples Literary Prize Incubating Committee & Founding Advisory Board",
     "Blue Metropolis International Literary Festival, Montreal, QC.",
     "AbTeC", "Service"),

]


# ─────────────────────────────────────────────────────────────────────────────
# derive_cv_dimensions — unchanged
# ─────────────────────────────────────────────────────────────────────────────

def derive_cv_dimensions(rows_in):
    """Add org (institution) and program (funding agency) columns.
    - org is set only for Employment and Education rows.
    - program (agency) and project (role) are set only for Funding rows.
    - All other rows get empty strings so they appear as untagged in the filter.
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
    # Ordered by specificity (longer/more specific first)
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
    # Maps agency name → subsection label for the filter panel
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
        'Undergraduate':          'Supervision',
        'Grad Certificate':       'Supervision',
        'Masters':                'Supervision',
        'PhD':                    'Supervision',
        'Postdoc':                'Supervision',
        'Creative Works':         'Art',
        'Solo Exhibitions':       'Art',
        'Group Exhibitions':      'Art',
        'Productions':            'Art',
        "Artist's Books":         'Art',
        'Books/Chapters':         'Dissemination',
        'Journal Articles':       'Dissemination',
        'Keynotes':               'Dissemination',
        'Conference Presentations':'Dissemination',
        'Invited Publications':   'Dissemination',
        'Invited Lectures':       'Dissemination',
        'Policy Papers':          'Dissemination',
        'Funding (PI)':           'Funding',
        'Funding (Co-I)':         'Funding',
        'Funding (Internal)':     'Funding',
    }

    result = []
    for row in rows_in:
        start, end, headline, desc, _project, group = row[:6]
        org = ''
        program = ''
        role = ''
        funding_group = ''
        category_group = category_group_map.get(group, '')

        if group == 'Education':
            for keyword, institution in edu_orgs:
                if keyword in headline:
                    org = institution
                    break

        elif group == 'Employment':
            org = 'Concordia University'  # default; overridden for pre-Concordia
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
            else:  # Funding (Internal)
                role = 'Internal'

        result.append((start, end, headline, desc, role, group, org, program, funding_group, category_group))
    return result


# ─────────────────────────────────────────────────────────────────────────────
# MAIN EXECUTION
# ─────────────────────────────────────────────────────────────────────────────

parsed_rows = parse_cv_txt()
all_rows = derive_cv_dimensions(rows + parsed_rows)
all_rows.sort(key=lambda r: GRP_ORDER.index(r[5]) if r[5] in GRP_ORDER else 99)

for row in all_rows:
    ws.append(list(row))

# Auto-width columns
for col in ws.columns:
    max_len = max(len(str(cell.value or "")) for cell in col)
    ws.column_dimensions[col[0].column_letter].width = min(max_len + 2, 60)

path = Path(__file__).parent / "cv.xlsx"
wb.save(path)
print(f"Saved {len(all_rows)} rows to {path}")
print(f"  Hardcoded rows : {len(rows)}")
print(f"  Parsed from cv.txt: {len(parsed_rows)}")
