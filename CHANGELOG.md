# Changelog

## Session 13 — 2026-03-01

### Themes view
- New **Themes** view mode: timeline rows keyed by research theme instead of CV section
- `VIEW_MODE` state (`'sections'` | `'themes'`); reset to `'sections'` on each `parse()` call
- `parse()` reads `themes`, `concepts`, `collaborators` arrays from enriched CV rows (Array.isArray guard handles non-enriched data)
- Theme frequency map → `themeRows` (sorted desc), `themeColor`, `themeVis`
- `computeThemeLanes()`: parallel to `computeLanes()`, builds `themeLanes[theme][evId]`, `themeLaneCounts`, `themeRowH`
- `redraw()`: `isThemes` flag drives row source, cumulative-Y, header label (`CATEGORY` → `THEME`), row backgrounds, event bars, label column, event count
- `drawEventBar()` helper extracted from inline loop; used by both sections and themes modes
- Sections / Themes toggle appears in sidebar only when enriched data is loaded
- `buildFiltersThemes()`: theme checkbox list with All / None, reuses `makeFilterItems` / `makeAllNoneButtons`
- Drawer: `#d-themes`, `#d-concepts`, `#d-collaborators` divs render enrichment tag pills when populated
- CSS: `.view-mode-toggle`, `.view-mode-btn`, `.d-tags`, `.d-tag` (+ `.theme`, `.concept`, `.collaborator` variants)

### Canvas watermarks
- **Past** (left of timeline start): *i ka wā ma mua / ka wā ma hope* — Nunito 700, 100px, amber, 25% opacity; right-justified flush to `AXIS_START`
- **Future** (right of timeline end): *the future is / Indigenous* — same style, left-justified
- AbTeC logo (`image/AbTeCLogo-Horizontal-Primary.png`) below past phrase, 15% opacity
- All three watermark groups re-centre vertically on scroll and redraw without full SVG rebuild
- Left group (phrase + logo) centred as a unit using measured logo height; right phrase centred independently
- Nunito loaded via Google Fonts (`wght@300;400;600;700`)

### Data
- `data/themes-data/jason-themes.md`: research themes profile extracted from `cv-data-enriched.js` (949 entries, 112 themes, 349 collaborators)

---

## Session 12 — 2026-02-28

### GDoc CV parser — link extraction
- `gdocExtractLink(tag)` extracts the first hyperlink from each entry and unwraps Google's redirect wrapper
- `{text}` convention: if an entry contains `{`*text*`}` where the word *text* is hyperlinked, that URL is used preferentially and the Storybox shows **Text ↗** instead of **More Info ↗**
- Detection matches on link text being exactly `"text"` (or `"{text}"`) — robust to Google Docs inserting empty spans around the braces
- `headlineLinkLabel` field threads through `normalizeRow` → `parse()` → event object → Storybox renderer

### Drop zone — plain-text CV support
- Drop zone now accepts `.txt` files in addition to `.xlsx`
- `parseCVText(text)` mirrors `parseGDoc()` logic: section heading detection, date-prefix + tab/2+ spaces split, continuation lines, bibliography year extraction
- `load()` branches on `.txt` extension and reads as UTF-8 text
- Drop zone label updated to "Drop Excel or text file here or Browse file" (single line, inline link style)
- File input `accept` attribute updated to include `.txt`

### Data / file organisation
- `AbTeC-Timeline-Data.xlsx` renamed to `timeline-data.xlsx`; `make_data_js.py` updated
- Old reference xlsx files moved to `ARCHIVE/`
- `data/cv-data/cv.txt` is an example file only — not auto-loaded; must be dragged in or browsed

### README
- New **Export** section (above Data Format) documents List and Timeline buttons
- **Data Format** split into Research Data and CV Data subsections
- CV Data subsection expanded: three loading methods, entry format table, `{text}` link convention, clarification that no CV file auto-loads
- **Using Your Own Data** section explains how to replace `timeline-data.xlsx` or `cv.txt`

### Backlog
- `Timeline-lkr`: CV Insights — visualize career evolution using Claude API (P3, new branch `Timeline-CV-Insights`)

---

## Session 11 — 2026-02-28

### Google Doc CV loader (in-browser)
- Paste any published Google Doc URL into the URL field → Load button auto-detects `/document/d/` and calls `loadFromGDoc()` instead of `loadFromGSheet()`
- `isGDocUrl(url)`: simple detection predicate
- `parseGDoc(html)`: JS port of `fetch_cv_from_gdoc.py` using `DOMParser`; same 3-strategy parser (date-prefix + `\xa0\xa0+` split, continuation line, bibliography year extraction)
- `gdocParseDateRange(s)`: full JS port of Python date parser; handles `M.YY`, `M.YY-present`, `M.YY-M.YY`, `M.YYYY`, `YYYY`, `YYYY-YY`, `YYYY-YYYY`, full month-name forms
- `loadFromGDoc(url)`: fetches published HTML (with `corsproxy.io` fallback for CORS), calls `parseGDoc`, then `parse(rows)` directly; status shows entry count on success
- 27-section `GDOC_SECTION_MAP` + `GDOC_PROJECT_MAP` match Python equivalents exactly
- Outputs rows with `'start date'`/`'end date'`/`'group'`/`'project'` keys → detected as `cv` format by `detectFormat()`; timeline title auto-updates to "CV Timeline"

---

## Session 10 — 2026-02-28

### Print section
- New **Print** section pinned to the bottom of the sidebar (outside the scrollable filter area)
- Contains two buttons: **List** (Markdown export) and **Timeline** (PDF export)
- Replaces the old `#sidebar-actions` row that was buried inside the file loader

### List (Markdown) export
- Exports all currently visible events (respects active filters) as a `.md` file
- Grouped by category in display order; each entry: `**date** — headline`
- File header includes title, date range, event count, and export date
- Default filename: `AbTeC-Timeline-List-{startYear}-{endYear}.md`

### Timeline (PDF) export
- Print dialogue now opens automatically when the export tab loads (`window.onload`)
- Export tab closes automatically after the dialogue is dismissed (`window.onafterprint`)
- `<title>` tag in the blob page sets the browser's default save-as filename to `AbTeC-Timeline-Visual-{y1}-{y2}`

---

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
