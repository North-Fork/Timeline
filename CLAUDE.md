# CLAUDE.md

## Project Description

Vibe-coding a timeline to track all of the research activity of Jason Lewis (https://www.jasonlewis.org) and his research studio-lab at Concordia University, Montreal, called Aboriginal Territories in Cyberspace (https://www.abtec.org).

## Issue Tracking: Use Beads

This project uses **beads** (`bd`) for all issue tracking.

### Required Workflow

Before starting any work:

1. Check for ready work:
   bd ready

2. Pick a task and claim it:
   bd update <issue-id> --status=in_progress

3. Work on the task (code, tests, docs)

4. When done, close it:
   bd close <issue-id>

### Creating New Issues

If you discover new work while implementing:

bd create --title="Issue title" --type=task|bug|feature --priority=2

### Rules

- ALWAYS check `bd ready` before asking "what should I work on?"
- ALWAYS update issue status to `in_progress` when you start working
- ALWAYS close issues when you complete them
- NEVER use markdown TODO lists for tracking work

---

## Project Map

### Overview

Single-file browser app. All application code (HTML, CSS, JavaScript) lives in one file.
No build step, no framework, no bundler.

### Root Files

| File | Purpose |
|---|---|
| `timeline.html` | The entire app — HTML structure, inline CSS, inline JS |
| `serve.sh` | Starts `python3 -m http.server 8000` (required for auto-load fetch) |
| `README.txt` | End-user usage instructions |
| `CHANGELOG.md` | Session-by-session change log (update at end of every session) |
| `FEATURES-WISH-LIST.txt` | Planned features and known limitations |
| `.gitattributes` | Configures `bd merge` driver for `.beads/issues.jsonl` |
| `AGENTS.md` | Beads agent landing-the-plane instructions |

### data/ Directory

```
data/
├── cv-data/
│   ├── cv.txt                              raw CV source text
│   ├── cv.xlsx                             generated timeline data (Timeline-CV branch)
│   └── generate_cv_xlsx.py                 converts cv.txt → cv.xlsx
└── timeline-data/
    ├── timeline-data.xlsx  active AbTeC data (Timeline-AbTeC* branches)
    ├── make_data_js.py                       converts xlsx → timeline-data.js
    ├── timeline-data.js                      generated JS with embedded data (auto-load)
    ├── timeline-test-data-synthetic.xlsx     synthetic test data (main branch)
    ├── timeline-test-data-handcrafted.xlsx   handcrafted test data
    └── *.xlsx                                older/reference versions
```

**Whenever the xlsx changes:** run `python3 data/timeline-data/make_data_js.py` to regenerate
`timeline-data.js` from the xlsx. This must be done before committing or testing.

**No server needed:** `timeline-data.js` is loaded via `<script src>` which works with
`file://`. `serve.sh` / http server only needed for xlsx drag-and-drop fallback path.

### xlsx Columns (timeline-data.xlsx)

Key columns used by the parser (`normalizeRow`):

| Column | Field | Notes |
|---|---|---|
| Year/Month/Day, End Year/Month/Day | start, end | TimelineJS split-date format |
| Headline | headline, headlineUrl | May contain `<a href>` — URL extracted separately |
| Title | headline (fallback) | Plain text; preferred over Headline for display |
| Text | description | Event body text |
| Category | group | Primary grouping (drives row colour + filter) |
| Group | org | Organisational dimension |
| Program | program | Program dimension |
| Project | project | Project dimension |
| Media | media | YouTube/Vimeo URL or direct image URL |
| Media Thumbnail | mediaThumbnail | Direct image URL or Flickr page URL |
| Media Caption | mediaCaption | Caption shown below media |
| Media Credit | mediaCredit | Credit shown below media |
| Team Members | teamMembers | Format: `Role: Name(s); Role: Name(s)` |

### How Components Interact

```
timeline.html (browser)
  ├─ on load: <script src="data/timeline-data/timeline-data.js">  ← works with file://
  │    └─ OR: user drag-and-drops an .xlsx onto the page
  ├─ detectFormat(rows) → 'abtec' (has Category col) or 'cv'
  ├─ normalizeRow() maps raw columns → internal event objects
  ├─ redraw() renders everything to SVG
  │    ├─ #tl-header  (sticky top)    ← time axis
  │    ├─ #tl-svg     (scrollable)    ← events + group labels
  │    └─ #tl-bottom  (sticky bottom) ← bottom axis
  ├─ Storybox (#drawer): slide-in panel showing event detail + media
  │    ├─ renderMedia() → YouTube/Vimeo iframe, direct img, or Flickr via noembed.com
  │    ├─ Prev/Next arrows with All/Category scope toggle
  │    ├─ More Info ↗ link (from Headline href)
  │    └─ Research Team section (from Team Members column)
  └─ PDF export: buildExportSVG() → blob URL → new tab → window.print()
```

### Branches and Their Data

| Branch | Auto-loads | Title |
|---|---|---|
| `main` | synthetic test data | Timeline |
| `Timeline-AbTeC` | `data/timeline-data/timeline-data.xlsx` | AbTeC Timeline |
| `Timeline-AbTeC-Media` | `data/timeline-data/timeline-data.xlsx` | AbTeC Timeline (active dev branch) |
| `Timeline-AbTeC-Prototype` | (archived) | superseded by Timeline-AbTeC |
| `Timeline-CV` | (archived) | CV support folded into Timeline-AbTeC-Media |

**CV data:** All CV support (`detectFormat()`, `normalizeRow()`, `parseCVText()`, Google
Doc parser) lives in `Timeline-AbTeC-Media/index.html`. No branch switch needed.
To view CV data: drag `data/cv-data/cv.xlsx` onto the timeline, or swap the `<script src>`
on line 9 to `data/cv-data/cv-data.js`. Format is auto-detected; sidebar title updates.

**CV data files:**
- `data/cv-data/cv.xlsx` — source (generated by `generate_cv_xlsx.py`)
- `data/cv-data/cv-data.js` — auto-load version (generated by `make_cv_data_js.py`)
- Run both scripts in sequence whenever CV data changes.

### Source URLs for CV Testing

Jason's CV is split across three published Google Docs:

| Document | URL |
|---|---|
| Research-Creation | https://docs.google.com/document/d/e/2PACX-1vRIeY4A3fbqJj29GP2yT0FpJkoPOLiLVqaOqPuIUDuJOjXLGwM0jEuS2WGb_daBLY8dCEuooURhz-5D/pub |
| Funding | https://docs.google.com/document/d/e/2PACX-1vTitfLMisxZ3NcqdLOIsf4Bsj_qSuMfuj6vh2N3d86ZjHyy4FlXx0cRIgGWdEhoerPLjs7rgVn75XNL/pub |
| Teaching & Service | https://docs.google.com/document/d/e/2PACX-1vQXdHyfjF3YivP2hM8Tf81qiasZymZKN4edMZFK3Rp7cq1O__opAvx0iFqdvK-xFzH5duKBb4Eo3Xt6/pub |

Use these URLs to test `fetch_cv_from_gdoc.py`, `loadFromGDoc()` (browser), and any
future multi-document CV pipeline.
