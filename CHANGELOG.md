# Changelog

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
