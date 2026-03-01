# AbTeC Timeline

Developer: Jason Edward Lewis with heavy lifting from Claude Code.

Developed to capture the research work of [Aboriginal Territories in Cyberspace](https://abtec.org), [Obx Labs](https://www.obxlabs.net), and [other work](https://jasonlewis.org) I've done.

---

## Data Source

It loads by default the data from a local file. You can drag your own file into the file drop box, or give it a Google Sheet URL. The Google Sheet must be Published. Terrible things will happen if your file is not formatted properlly. See Data Format section below.

## Getting Started

### Recommended: Chrome or Brave

Double-click `index.html` to open. The timeline data loads automatically.

If the data does not appear, the pre-generated data file may be out of date — see [Keeping local data current](#keeping-local-data-current).

### All other browsers (Firefox, Safari, etc.)

Browsers other than Chrome/Brave block local file access, so the data cannot load via double-click. Instead:

1. Open a terminal and navigate to this folder:
   ```
   cd /path/to/Timeline-JEL
   ```
2. Start a local server:
   ```
   python3 -m http.server 8000
   ```
3. Open in your browser:
   ```
   http://localhost:8000/index.html
   ```

---

## Navigation

| Action | How |
|--------|-----|
| Zoom in/out | Spacebar + mousewheel |
| Pan left/right | Click and drag on the timeline |
| Fit all events | Click **Fit** in the sidebar |
| Jump to today | Click **Today** in the sidebar |
| Search | Type in the search box and press Enter; use ◀ ▶ to cycle through matches |
| Search mode | **Abs** starts from the earliest match; **Rel** starts from the current view position |

---

## Loading Data

Three ways to load data:

**1. Pre-generated local file (default, fastest)**
The timeline loads `AbTeC-Timeline-Data.xlsx` automatically on startup via the pre-built `data/timeline-data/timeline-data.js` file.

**2. Drag and drop**
Drag any `.xlsx` file onto the drop zone in the sidebar.

**3. Google Sheets**
Paste a published Google Sheets URL into the URL field in the sidebar and click **Load** (or press Enter). The sheet must be published to the web (**File → Share → Publish to web**). The URL is remembered between sessions but is never fetched automatically — click Load each time you want to refresh.

---

## Keeping Local Data Current

When `AbTeC-Timeline-Data.xlsx` is updated, regenerate the pre-built data file:

```
python3 data/timeline-data/make_data_js.py
```

Requires Python 3 and the openpyxl library:
```
pip3 install openpyxl
```

---

## Data Format

The source file is an Excel workbook (`.xlsx`). The first row must be a header row. The following columns are recognised:

### Dates (required)

| Column | Notes |
|--------|-------|
| Year | Start year (4-digit) |
| Month | Start month (1–12; optional) |
| Day | Start day (optional) |
| End Year | End year — omit for point events |
| End Month | End month (optional) |
| End Day | End day (optional) |

### Event Content

| Column | Notes |
|--------|-------|
| Title | Plain-text event title (preferred for display) |
| Headline | May contain an `<a href="…">` link — the URL becomes the **More Info** link in the Storybox |
| Text | Body text shown in the Storybox (HTML allowed) |

### Categorisation

| Column | Notes |
|--------|-------|
| Category | Primary grouping — drives the row, row colour, and Categories filter (required) |
| Group | Organisational dimension (e.g. AbTeC, IIF) |
| Program | Program dimension (e.g. IIF) |
| Project | Project dimension (e.g. Skins, Isuma) |

### Media (all optional)

| Column | Notes |
|--------|-------|
| Media | YouTube URL, Vimeo URL, or direct image URL — rendered as embedded video or image |
| Media Thumbnail | Direct image URL or Flickr page URL — fallback thumbnail when no video present |
| Media Caption | Caption shown below the media |
| Media Credit | Credit line shown below the media |

### Team & Funders (optional)

| Column | Format |
|--------|--------|
| Team Members | Semicolon-separated `Role: Name(s)` pairs, e.g. `RA-Undergraduate: Alice, Bob; Staff: Dave; Co-investigators: Eve; Primary Investigator: Frank` |
| Funders | Semicolon-separated list of funder names |

Recognised team roles (in display order): `RA-Undergraduate`, `RA-Masters`, `RA-PhD`, `Staff`, `Co-investigator(s)`, `Primary Investigator`

---

## PDF Export

Click the **PDF** button in the sidebar. Enter a year range when prompted. A print-ready SVG opens in a new tab — click **Print / Save as PDF**.

> **Note:** PDF export requires Chrome or Brave. Firefox and Safari are not currently supported due to browser differences in print and SVG handling.
