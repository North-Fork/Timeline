# AbTeC Timeline

Developer: Jason Edward Lewis with heavy lifting from Claude Code.

Developed to capture the research work of [Aboriginal Territories in Cyberspace](https://abtec.org), [Obx Labs](https://www.obxlabs.net), and [other work](https://jasonlewis.org) I've done.

Also works for CVs. See Data Formats below.

---

## Data Source

It loads by default the data from a local file. You can drag your own file into the file drop box, or give it a Google Sheet URL. The Google Sheet must be Published. Terrible things will happen if your file is not formatted properlly. See Data Format section below.

## Tested Platforms

This app has been tested on the following platforms only. Contributors should note any regressions on these targets and test on them before submitting changes.

| Platform | Browser | Notes |
|----------|---------|-------|
| macOS | Brave | Primary development browser |
| iPhone 14, iOS 26.2 | Safari | |
| iPad Pro 11" 4th gen, iOS 26.2 | Safari | |

---

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

| Action | Desktop | Mobile |
|--------|---------|--------|
| Zoom in/out | Spacebar + mousewheel or trackpad | Pinch gesture |
| Zoom buttons | ＋ / － in sidebar | ＋ / － in toolbar |
| Pan left/right | Click and drag on the timeline | Single-finger swipe horizontally |
| Scroll up/down | Mousewheel / trackpad | Single-finger swipe vertically |
| Open event detail | Click event (tooltip previews on hover) | Tap event — opens Storybox directly |
| Fit all events | Click **Fit** in the sidebar | Tap **Fit** in toolbar |
| Jump to today | Click **Today** in the sidebar | Tap **Today** in toolbar |
| Search | Type in the search box and press Enter; use ◀ ▶ to cycle through matches. Non-matching events dim to 15% opacity so matches stand out; clearing the search restores all events to normal opacity. | Same |
| Search mode | **Abs** starts from the earliest match; **Rel** starts from the current view position | Same |

---

## Loading Data

**1. Pre-generated local file (default, fastest)**
The timeline loads `timeline-data.xlsx` automatically on startup via the pre-built `data/timeline-data/timeline-data.js` file.

**2. Drag and drop**
Drag a file onto the drop zone in the sidebar, or click **Browse for file**. Supported formats:

| File type | Use for |
|-----------|---------|
| `.xlsx` / `.csv` | Events (research/project data) or CV |
| `.txt` | CV plain text |
| `.json` | ORCID record export |

**3. URL / ID field**
Paste a URL or ID into the field below the drop zone and click **Load** (or press Enter). The value is remembered between sessions but never fetched automatically. Supported inputs:

| Input | What it loads |
|-------|--------------|
| Google Sheets URL | Published spreadsheet (must be published to web via **File → Share → Publish to web**) |
| Google Doc URL | Published CV Google Doc |
| ORCID iD | Bare iD (`0000-0001-5000-0007`) or full URL (`https://orcid.org/…`) — fetched live from the ORCID public API |

---

## Using Your Own Data

### Research / Project data

Replace `data/timeline-data/timeline-data.xlsx` with your own `.xlsx` file of the same name, then regenerate the pre-built data file:

```
python3 data/timeline-data/make_data_js.py
```

### CV data

Paste the URL of your published Google Doc CV into the URL field and click **Load** — no local files needed.

#### Public and private CV data (collaborator note)

The CV timeline has two builds:

| Build | Data | How to access |
|-------|------|---------------|
| **Public** | Research-Creation only | Add `?public` to the URL — e.g. `index.html?public` |
| **Private** | All CV sections | Local only — not in this repo |

`cv-data-public.js` (Research-Creation) is auto-generated weekly by GitHub Actions and committed to this repo. It is the only CV data file collaborators need to work with.

The full private CV (`cv-data.js`, containing Funding and Teaching & Service sections) is gitignored and never pushed. It is generated locally by the repo owner only and is not available to collaborators.

---

## Filters

The **Filters** section in the sidebar controls which events are visible on the timeline.

### Category reorder

The Category section shows a ⠿ drag handle to the left of each row. Drag rows up or down to reorder the timeline lanes — the order updates live as you drag. Your custom order persists across page refreshes and is saved and restored with View files.

---

## View

The **View** section in the sidebar lets you save and restore a named snapshot of the current pan/zoom position and all active filter settings (Category, Group, Program, Project).

### Save

Type a name in the input field and click **Save…** (or press Enter). The browser downloads a file named `<name>.view.json` to your downloads folder. Move it to a `/views` folder alongside your data files to keep things organised.

### Load

Click **Load…** to open a file picker (filtered to `.view.json` files). Select a previously saved view file — the timeline immediately restores the zoom level, scroll position, and filter state captured at save time.

Filter values that no longer exist in the current dataset are silently ignored; everything else is restored exactly.

---

## Export

The **Export** section is pinned at the bottom of the sidebar.

### List

Click **List** to download a Markdown (`.md`) file of all currently visible events. The file is grouped by category in display order and includes a header with the title, date range, event count, and export date. Active filters are respected — only events visible on the canvas are exported. Default filename: `AbTeC-Timeline-List-{startYear}-{endYear}.md`.

### Timeline

Click **Timeline** to export the current view as a PDF. Enter the year range when prompted. A print-ready SVG opens in a new tab; the print dialogue appears automatically — choose **Save as PDF** in your browser's print panel. Default filename: `AbTeC-Timeline-Visual-{startYear}-{endYear}`.

> **Note:** PDF export requires Chrome or Brave. Firefox and Safari are not currently supported due to browser differences in print and SVG handling.

---

## Data Format

> **NOTE for Nancy/AbTeC Team** — we need to validate the Group:Program:Project taxonomy, and update the IIF data to reflect properly.

The timeline auto-detects whether a file contains research/project data or CV data based on its column headers.

### Research Data

The source file is an Excel workbook (`.xlsx`) or a comma-separated values file (`.csv`). The first row must be a header row. The following columns are recognised:

#### Dates (required)

| Column | Notes |
|--------|-------|
| Year | Start year (4-digit) |
| Month | Start month (1–12; optional) |
| Day | Start day (optional) |
| End Year | End year — omit for point events |
| End Month | End month (optional) |
| End Day | End day (optional) |

#### Event Content

| Column | Notes |
|--------|-------|
| Title | Plain-text event title (preferred for display) |
| Headline | May contain an `<a href="…">` link — the URL becomes the **More Info** link in the Storybox |
| Text | Body text shown in the Storybox (HTML allowed) |

#### Categorisation

The filter panel builds its options dynamically from whatever unique values appear in these columns — there is no fixed list. Add a new value to the data and it will appear in the filters automatically.

| Column | Notes |
|--------|-------|
| Group | Organisational dimension (e.g. AbTeC, IIF) |
| Program | Program dimension (e.g. IIF) |
| Project | Project dimension (e.g. Skins, Isuma) |
| Category | Primary grouping — drives the row, row colour, and Category filter (required) |

#### Media (all optional)

| Column | Notes |
|--------|-------|
| Media | YouTube URL, Vimeo URL, or direct image URL — rendered as embedded video or image |
| Media Thumbnail | Direct image URL or Flickr page URL — fallback thumbnail when no video present |
| Media Caption | Caption shown below the media |
| Media Credit | Credit line shown below the media |

#### Team & Funders (optional)

| Column | Format |
|--------|--------|
| Team Members | Semicolon-separated `Role: Name(s)` pairs, e.g. `RA-Undergraduate: Alice, Bob; Staff: Dave; Co-investigators: Eve; Primary Investigator: Frank` |
| Funders | Semicolon-separated list of funder names |

Recognised team roles (in display order): `RA-Undergraduate`, `RA-Masters`, `RA-PhD`, `Staff`, `Co-investigator(s)`, `Primary Investigator`

### CV Data

The CV Data handling is currently optimized to read Jason Lewis' CV format. It is not a general purpose CV parser yet, though if you format your CV in a similar way, it should work.

There is no auto-loaded CV file — you must load CV data manually each session using one of the four methods below.

**Method 1 — Drag and drop (or Browse) a `.txt` file**

Export or copy your CV as a plain text (`.txt`) file, then drag it onto the drop zone or use **Browse file**. The file is not stored; you need to re-load it each session. The parser looks for section headings and date-prefixed entries in the same format described under *Entry format* below.

> Note: `data/cv-data/cv.txt` is included in the repo as an example but is not loaded automatically — drag it in to use it.

**Method 2 — Load from a published Google Doc URL**

Paste the published URL of a Google Doc CV into the URL field and click **Load**. The doc must be published to the web (**File → Share → Publish to web**). The timeline parses the document's section headings and date-prefixed entries automatically and sets the title to *CV Timeline*. The URL is remembered between sessions but is never fetched automatically — click Load each time you want to refresh.

**Method 3 — From an Excel or CSV file (`.xlsx` / `.csv`)**

The file should have a `Group` column (the CV section name, e.g. *Employment*, *Books*, *Solo Exhibitions*) plus `start date`, `end date`, `headline`, and `description` columns. Drag the file onto the drop zone or use **Browse file**. Run `data/cv-data/make_cv_data_js.py` to pre-generate a local data file that loads automatically on startup (advanced use).

**Method 4 — Load from ORCID**

Paste your ORCID iD (e.g. `0000-0001-5000-0007`) or full ORCID URL into the URL field and click **Load**. The timeline fetches your public record live from the ORCID API and displays all sections — Works, Employment, Education, Funding, Distinctions, Service, Memberships, and Invited Positions. Alternatively, export your ORCID record as a `.json` file from orcid.org and drag it onto the drop zone.

**Converting your CV to the right format**

The simplest path is to keep your CV in Google Docs and publish it to the web — no conversion needed. If you want to use a `.txt` file instead, structure it as plain text with section headings on their own lines and one entry per line, with the date at the start separated from the text by a tab or two or more spaces (see *Entry format* below).

Recognised section headings include: Employment History, Education, Honors and Awards, Books, Book Chapters, Journal Articles & Conference Proceedings, Conference / Symposia Presentations, Keynote / Plenary / Special Guest Speaker, Invited Publications, Invited Lectures / Artist Talks / Panels, Artist's Books and Exhibition Publications, Symposium / Workshop / Lecture Series Organizer or Lead, Documentaries, Websites, Residencies, Residency Organizer, Academic Review & Textbook Inclusion, Op-Ed, Press Coverage / Interviews / Documentaries, Policy Papers / Governmental Presentations / Reviews & Consultations, Exhibitions - Solo, Exhibitions - Group, Film Screenings, Commissions, Poetry Publication & Performances, Curatorial, Visiting Artist & Master Classes, Producer / Executive Producer, Major Works.

**Entry format (Google Doc and `.txt`)**

Each entry should begin with a date, followed by the entry text. In a Google Doc the separator is two or more non-breaking spaces; in a `.txt` file it is a tab or two or more regular spaces. The parser recognises a range of date formats:

| Format | Example |
|--------|---------|
| `M.YY` | `9.19` |
| `M.YYYY` | `9.2019` |
| `M.YY-present` | `6.14-present` |
| `M.YY-M.YY` | `6.08-5.14` |
| `YYYY` | `2019` |
| `YYYY-YY` | `2014-18` |
| `YYYY-YYYY` | `2014-2018` |
| `Month YYYY` | `Sept 2019` |
| `D Month, YYYY` | `2 March, 2023` |
| `Month. D, YYYY` | `Oct. 22, 2021` |

Bibliography-style entries with no date prefix are also supported — the parser extracts the most recent four-digit year from the citation text.

**Links in entries**

Any hyperlink found in an entry is surfaced as a **More Info ↗** link in the Storybox. To mark a link as the full text of a publication, annotate the entry with `{`*`text`*`}` where the word *text* is hyperlinked to the document URL — the parser detects this convention and labels the link **Text ↗** in the Storybox instead.

**Publication cover images (Dissemination events)**

For events in the Dissemination category groups — Books/Chapters, Journal Articles, Invited Publications, Op-Ed — the Storybox will automatically display a cover image if one is available. Images are sourced from the [jasonlewis.org media library](https://jasonlewis.org/category/publication/) and stored in a pre-built lookup table at `data/cv-data/pub-images.js`.

To refresh the lookup after new publications are added to jasonlewis.org:

```
cd data/cv-data
python3 fetch_pub_images.py
```

The script fetches the WP media library via the WordPress REST API, matches publication titles to cv.xlsx headlines by keyword overlap, and rewrites `pub-images.js`. Requires Python 3 and openpyxl.

> **Note on new publication titles:** jasonlewis.org/category/publication/ is JavaScript-rendered and cannot be scraped statically. When a new publication appears on the site, add its title to the `WEBSITE_TITLES` list in `fetch_pub_images.py`. New cover images uploaded to jasonlewis.org are discovered automatically via the WP media API without any manual changes.

**Automated weekly updates (GitHub Actions)**

The repo includes a GitHub Actions workflow (`.github/workflows/update-cv.yml`) that runs every Monday at 06:00 UTC on the `Timeline-AbTeC-Media` branch. It:

1. Fetches the three published Google Doc CV sections and rebuilds `cv-data.js`
2. Fetches the jasonlewis.org media library and rebuilds `pub-images.js`
3. Commits and pushes both files if anything changed

To trigger a manual run: go to **Actions → Weekly CV update → Run workflow** in the GitHub repository UI.

No secrets beyond the default `GITHUB_TOKEN` are required — the CV Google Docs and the WP media API are both publicly accessible.
