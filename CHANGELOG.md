# Changelog

## Session 9 — 2026-02-28

### Filters — two-way category/dimension sync
- **Uncheck Group/Program/Project** → auto-unchecks any Category that has no events in the remaining visible dimensions (`syncCategoryVis`)
- **Check a Category** → auto-checks any Group/Program/Project that has events in that category (`syncDimVis`)
- Unchecking a Category has no cascade effect (explicit hide)

---

## Session 8 — 2026-02-28

### UI
- Group labels in timeline left column now word-wrap intelligently up to 3 lines (centred vertically) instead of truncating; applied to both main SVG and PDF export
- `wrapLabel()` and `svgWrappedLabel()` helpers added
- Filter panel reorganised: sections now ordered Group → Program → Project → Categories; top of panel labelled **Filters** (`.filter-panel-title` class); individual category sections retain their own names

### Data
- Added Abundant Intelligences group to AbTeC-Timeline-Data.xlsx (1203 rows)
- README.txt replaced by README.md with full markdown formatting

---

## Session 7 — 2026-02-28

### Google Sheets loader
- URL input + Load button added to file section in sidebar
- Accepts published Google Sheets URLs (pubhtml, pub, standard /d/{key}/, with optional ?gid=)
- Tries direct fetch first; falls back to corsproxy.io if CORS blocks
- Cache-busting timestamp + `cache: 'no-store'` on every fetch to avoid stale data
- Last-used URL saved to localStorage (pre-filled on next open, not auto-fetched)
- Status feedback: Loading… / ✓ Loaded / Failed / Invalid URL

### Data source rename
- Source file renamed from `IIF-Timeline-Data-Multi-Project.xlsx` → `AbTeC-Timeline-Data.xlsx`
- `make_data_js.py` and `CLAUDE.md` updated accordingly

### Backlog
- `Timeline-m48`: Auto-sync Google Sheets via GitHub Actions (P3, not yet started)

---

## Session 6 — 2026-02-28

### Research Team (Storybox)
- **Grouped RA levels**: RA-Undergraduate, RA-Masters, RA-PhD now appear under a single "Research Assistant/s" heading (plural if >1 name total); sub-headings "Undergraduate", "Masters", "PhD" in italic grey
- **"and" rule**: any team category with exactly two names joins them with "and" instead of a comma
- **Co-investigator/s** and **Primary Investigator/s** labels now singular or plural based on name count
- **Role labels**: changed from `<u>` underline to white text (`d-team-role` class)
- **Spacing**: 5px between RA sub-sections; 2px between names reduced to 0px sublabel gap

### Funders section (Storybox)
- New **Funders** column (col W) in xlsx wired through normalizer → event objects → Storybox
- Funders section rendered below Research Team; hidden when empty; semicolon-separated, one entry per line
- Storybox body already `overflow-y: auto` so long lists scroll correctly

### Search
- **Search box** added to sidebar: text input, ◀ ▶ nav buttons, Abs/Rel toggle, result counter
- **Abs mode**: results sorted chronologically, starts at earliest match
- **Rel mode**: starts at first match at or after current viewport centre, wraps if all in past
- Counter shows `N / total`; arrows disabled until results exist; clearing input resets state
- Searches: headline, description, group, org, program, project, teamMembers, funders

### Crosshair date line
- Added to FEATURES-WISH-LIST.txt: z-ordering issue (appears above events instead of below); needs fresh investigation

### Sidebar layout
- **Three named sections** with divider lines: Title / View Controls / Search / File+PDF (scrolls with filters)
- Zoom (＋ －), Fit, and Today buttons grouped together in **View Controls** section
- Search box moved to its own section directly below View Controls
- File drop zone + PDF button moved to bottom of scrollable filters area, re-appended after last Project item on each `buildFilters()` call
- `groupY` promoted to module-level so `jumpToEvent()` can scroll vertically to matched event's row

### Data
- Reparsed `IIF-Timeline-Data-Multi-Project.xlsx` (1202 rows); Funders column added

---

## Session 5 — 2026-02-27

### Storybox (event detail drawer) — Timeline-AbTeC-Media branch

- **Renamed**: the slide-in event detail panel is now called the **Storybox**
- **Media embedding**: clicking an event opens the Storybox with embedded media
  - YouTube and Vimeo URLs in the `Media` column render as iframes (video takes priority; thumbnail ignored when video is present)
  - Flickr URLs resolved to direct image via noembed.com (CORS-friendly); checked in both `Media` and `Media Thumbnail` columns
  - Direct image URLs (.jpg / .png etc.) rendered as `<img>`
  - `noembedCache` + `preloadAdjacent()` for Flickr performance
- **Toggle close**: clicking the same event again closes the Storybox
- **Prev/next navigation**: ◀ ▶ arrows in Storybox header step through visible events chronologically
- **Navigation scope toggle**: "All | Category" toggle next to arrows — "All" walks all visible events; "Category" walks only events in the same category as the current event
- **More Info link**: if the `Headline` column contains an `<a href>`, a "More Info ↗" link appears after the description, opening in a new tab
- **Research Team section**: `Team Members` column (format: `Role: Name(s); Role: Name(s)`) rendered with underlined roles, names on next line, spacing between groups
- **Meta layout**: date (white) shown above category, no labels
- **Description**: line-height tightened from 1.7 → 1.53

### Parser updates
- Added `Team Members` column to `normalizeRow` and parsed event objects
- Added `headlineUrl` extraction from `Headline` HTML (`<a href>`) — uses `Headline` column directly (not `Title`) to preserve the link
- Added `Media Thumbnail` column support; Flickr page URLs in thumbnail fall through to noembed

### Data
- `Media Thumbnail` column added to `IIF-Timeline-Data-Multi-Project.xlsx`
- Flickr URLs copied from `Media` column into `Media Thumbnail` for ~516 rows
- Skins 4.0 (row 526): Vimeo link added to `Media` column; direct thumbnail `.jpg` in `Media Thumbnail`
- `Team Members` column (col V) added with role-structured data

### Colour palette
- Swapped colours for Residencies/Exhibitions (now purple `#8b5cf6`) and Dissemination (now amber `#f59e0b`)

---

## Session 4 — 2026-02-26

### PDF Export (Timeline-AbTeC)
- **PDF button** added to toolbar (after Today button)
- **Year-range modal** prompts for Start Year / End Year with defaults from data range
- **`buildExportSVG(y1, y2)`** generates a standalone 1100px SVG respecting all active filters: title bar (orange), top axis, row backgrounds, year grid lines, event bars with labels, today marker, label column, bottom axis
- **Print window**: SVG opened via blob URL in a new tab; "Print / Save as PDF" button triggers `window.print()` then auto-closes the tab; page size `11in × 8.5in` (US letter landscape) with 0.75in margins; `viewBox` + `width:100%` fills the full printable area
- **Focus redraw**: `window.addEventListener('focus', redraw)` recovers the original window's UI after the print dialog unblocks the browser

### Offline data loading (Timeline-AbTeC)
- **`data/timeline-data/make_data_js.py`**: converts xlsx to `timeline-data.js` (`window.__TIMELINE_DATA__ = [...]`) for use without a local server
- **Auto-load priority**: pre-generated JS (works with `file://` double-click in Chrome/Brave) → fetch xlsx (http/https) → synthetic fallback
- **`README.txt`**: browser notes (Chrome/Brave for double-click; server URL for others), data update instructions

---

## Session 3 — 2026-02-26

### File Organisation (all branches)
- Renamed `data/cv/` → `data/cv-data/` on `main`, `Timeline-CV`, `Timeline-AbTeC`
- Moved all timeline-named files from `data/` root into new `data/timeline-data/` subfolder on all three branches
- Updated auto-load fetch paths to match new locations (`data/cv-data/cv.xlsx`, `data/timeline-data/IIF-Timeline-Data-Multi-Project.xlsx`)
- Deleted untracked `reference/` folder (unused)

### Branch Titles
- Set per-branch `<title>` and `#sidebar-title`:  `main` → "Timeline", `Timeline-CV` → "CV Timeline", `Timeline-AbTeC` → "AbTeC Timeline"

---

## Session 2 — 2026-02-25

### New Branches
- **Timeline-CV** — branched from `main`; loads Jason Lewis academic CV data
- **Timeline-AbTeC** — branched from `Timeline-CV`; loads IIF/AbTeC project data with multi-project filtering
- **Timeline-JEL-AbTeC** — experimental branch (superseded by Timeline-AbTeC)

### File Organisation
- Moved all `.xlsx` data files from repo root into `data/`
- Moved `cv.txt`, `cv.xlsx`, `generate_cv_xlsx.py` into `data/cv/`
- Moved `timeline-reference.xlsx` duplicate from root (canonical copy remains in `reference/`)

### Timeline-CV improvements
- **Vertical scrolling**: extracted time axis into sticky `#tl-header` div; `#tl-wrap` changed to `overflow-y: auto`; bottom axis changed to `position: sticky; bottom: 0`; drag handler extended to also scroll vertically
- **Today button**: added to toolbar; pans timeline so today's date sits at the right edge of the canvas
- **Spacebar zoom fix**: `e.preventDefault()` on spacebar keydown prevents browser from scrolling the page when activating wheel zoom
- **CV data**: `data/cv/generate_cv_xlsx.py` generates 139-row `cv.xlsx` from `data/cv/cv.txt` across 10 categories (Employment, Honors, Education, Creative Works, Books/Chapters, Journal Articles, Keynotes, Solo Exhibitions, Group Exhibitions, Productions)
- **Color by category**: events coloured by group/category rather than project; `groupColor` replaces `projColor`
- **Categories filter**: sidebar shows Categories filter only (Projects filter suppressed)
- **Lane stacking**: same-date point events assigned to separate vertical lanes; minimum effective width derived from fit-all scale so closely-spaced events don't visually overlap
- **Label truncation**: point event labels bounded by the start of the next event in the same lane to prevent horizontal overflow
- **HTML stripping**: `stripHtml()` applied to headline; `Title` column preferred over `Headline` (which may contain raw HTML links)

### Timeline-AbTeC improvements
- **IIF data**: loads `data/IIF-Timeline-Data-Multi-Project.xlsx` (552 events, 2013–2021)
- **TimelineJS format support**: parses `Year`/`Month`/`Day` split-date columns; `sheetToRows()` helper deduplicates repeated column headers
- **Multi-dimension filtering**: sidebar shows Group, Program, and Project filter sections in addition to Categories when the data contains those columns
- **OR filter logic**: Group/Program/Project use OR logic — an event is visible if any one of its tags is checked; events with no tags always show through; Categories remain a strict AND filter driving row visibility
- **Group ordering**: custom `GROUP_ORDER` for IIF categories (Workshops → Symposia → Residencies → Guest Lectures → Illustrating the Future Imaginary → Archive → Dissemination → Press/Reviews)
- **Parser fix**: `normalizeRow` prefers `Category` column over `Group` for row grouping; `Group` column correctly read as organisational dimension; `hasOrgDim` check suppresses redundant Group filter for old-format files

---

## Session 1 — (prior session)

### Initial features (from commit history)
- Browser-based SVG timeline tool (single `timeline.html` file)
- SheetJS drag-and-drop Excel file loading
- Horizontal pan (click+drag) and zoom (toolbar buttons)
- Fit and FitAll view controls
- Event bars with lane stacking for overlapping durational events
- Sidebar category/project filters with colour-coded checkboxes
- Click-to-open event detail modal
- Hover tooltips
- Top and bottom month/year axes
- AbTeC sample data support
