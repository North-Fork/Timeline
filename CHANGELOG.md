# Changelog

## Session 21 — 2026-03-15  ·  tag: V.03.06-Timeline-Vignettes

### Portrait vignettes on timeline and hover
- **Timeline bars** — `people` format events show a 25×25 circular portrait at the left edge of each bar; text label shifts right to avoid overlap; events without a matched photo render as normal bars
- **Hover tooltip** — portrait shown as a 75×74px rectangle below the category/date fields; hidden for events without a photo
- `currentFormat` module-level state variable added so `drawEventBar()` can check the active format without threading it through call arguments

## Session 20 — 2026-03-15  ·  tag: V.03.05-Team

### People / Team timeline format
- New `people` format: add a `format` column with value `people` to any xlsx; `detectFormat()` reads it and sets the sidebar title to **AbTeC People**
- `FORMAT_TITLES` extended: `{ abtec, cv, people }`; falls through to `cv` normalizeRow branch (group/org/etc. map correctly)
- `data/fetch_people_images.py` — scrapes `https://www.obxlabs.net/people`; fuzzy-matches names from team xlsx; writes `data/people-images.js` (`window.__PEOPLE_IMAGES__`)
- `image/abtec-team/` — 76 team portraits downloaded as `FirstName-LastName.ext`; Jason Lewis added manually (his name div is hidden on the people page)
- `data/people-images.js` — keys are xlsx headline values; values are local `image/abtec-team/` paths
- `openDrawer()` shows portrait when `ev.headline` matches a `__PEOPLE_IMAGES__` key and no other media is set
- Bios scraped from `div.msg_body` on obxlabs.net/people; personal URLs picked preferring h5 URL-text links, skipping institutional domains; written to xlsx `description` + `headline_url` columns
- `data/timeline-data/ra-team-data.js` — Python-generated JS from RA team xlsx (bypasses SheetJS for testing)

### Bug fixes
- **xlsx drag-and-drop lost long cell values** — `readAsBinaryString` + `type:'binary'` mishandles large UTF-8 shared string tables; switched to `readAsArrayBuffer` + `type:'array'` (current SheetJS best practice)
- **Tooltip showed full bio on hover** — now shows name, category, and dates only; full bio reserved for Storybox
- **`"present"` in end date** — parsed as today's date at load time; displayed literally as "present" in both hover tooltip and Storybox date range

## Session 19 — 2026-03-15

### ORCID support
- New `utilities/orcid-utilities.js` — exports `window.ORCIDFormat` with `detect()`, `parse()`, `fetchByID()`
- Parses all ORCID sections: Works, Employment, Education, Funding, Distinctions, Service, Memberships, Invited Positions
- Fetches live from the ORCID public API (no auth required); also accepts dropped `.json` export files
- Tested against ORCID iD `0000-0003-0130-8544` — 87 events parsed across 10 groups

### Unified URL load field
- Collapsed Google Sheets, Google Doc, and ORCID inputs into a single field (`#url-box`) with auto-detection
- Detection order: ORCID iD / URL → Google Doc URL → Google Sheets URL
- Old `GSHEET_LS_KEY` → `URL_LS_KEY`; localStorage remembers last input across all types

### File drop updates
- Added `.json` handler in `load()` for ORCID export files
- Drop-zone hint text updated: "Drop Events (.xlsx, .csv) or CV (.xlsx, .txt, .json)"
- File input `accept` updated to include `.json`

### Restructured utilities
- `cv.js` → `utilities/cv-utilities.js`
- `utilities/orcid-utilities.js` added alongside it
- All path references updated in `index.html`, `test.html`, `CLAUDE.md`, `HANDOFF.md`

### Externalized logo and taglines
- Logo renamed: `image/AbTeCLogo-Horizontal-Primary.png` → `image/logo.png`
- Pre-history / post-history watermark text externalized to `data/taglines.js` (loaded via `<script src>`, works with `file://`)
- Watermark variable names updated: `pastWatermarkG` → `preHistoryWatermarkG`, `futureWatermarkG` → `postHistoryWatermarkG`
- Watermark rendering now dynamic — supports any number of lines at 110px spacing

### Handoff packaging
- `Handoff-File-Drop/` — self-contained handoff folder with File section visible; auto-loads `cv-data-public.js`
- `Handoff-No-File-Drop/` — handoff folder with File section hidden
- `package-handoff.sh` — syncs all current source files into `Handoff-File-Drop/`, applies handoff-specific patches, and zips; always use this instead of zipping manually
- `image/` directory and `data/taglines.js` now included in all handoff folders

### Planning and docs
- `PLANNING.md` — full design spec for Smart Mapper (heuristic-first, Claude API fallback)
- `FEATURES-WISH-LIST.md` — Smart Mapper entry added with pointer to `PLANNING.md`
- `README.md` — Loading Data section rewritten; CV methods expanded to four (added ORCID)
- `CLAUDE.md` — updated for all structural changes; `image/` directory section added
- `HANDOFF.md` — packaging instructions added; `package-handoff.sh` documented

---

## Session 18 — 2026-03-12

### CV Storybox — description fidelity improvements

- **Italic title detection for CSS-class-based italic**: GDocs published HTML often uses CSS classes (e.g. `class="c14"`) rather than inline `font-style:italic` or `<em>` tags for italic text. `extract_italic_title()` now parses the document `<style>` block at the start of `parse_doc()` to collect italic class names, then checks span classes against that set. Fixes book titles like "Against Reduction" and "Educational, Psychological..." that were showing author lists instead.

- **Book chapters: chapter title as headline**: For book chapter entries, the chapter title is in quotes and the volume title is in italics. `_strategy3_headline()` now prefers quoted text (chapter title) over italic text (volume title). Fixes image lookup for ~15 chapters whose titles match keys in `pub-images.js`. Also adds single-quote (`\x27`) support so entries like `'Reworlding AI Through Future Imaginaries'` are detected.

- **Italic markup preserved in Storybox description**: New `tag_to_desc_html()` converts GDoc HTML tags to an HTML string, wrapping italic spans in `<em>` while HTML-escaping all text content. Bibliography entries (Strategy 3 path) now store HTML descriptions, so book titles, journal names, and conference names render in italic in the Storybox. Non-bibliography entries (employment, keynotes, etc.) use the plain-text path unchanged.

- **More Info links from `{text}` / `{link}` annotations**: GDoc annotation syntax encodes a URL as `{` + `<a href="google.com/url?q=ACTUAL_URL">text</a>` + `}`. New `extract_annotation_url()` decodes the Google redirect wrapper and returns the target URL. Stored as `headline_url` on each row; `normalizeRow()` reads it as `headlineUrl` so the Storybox shows a More Info link. `tag_to_desc_html()` strips the `{text}` / `{link}` markers from the rendered description.

- **`generate_cv_xlsx.py` updated**: Added `headline_url` column to xlsx output; HTML stripped from descriptions before writing (xlsx is plain text). `normalizeRow()` updated to read `headlineurl` first, then fall back to extracting a URL from the headline field.

### Code quality

- Collaborator-facing comments added to `index.html`: block comment at `detectFormat()` explains the dual-format (AbTeC / CV) architecture; `// CV only` markers on all `CVFormat.*` call sites in `parse()`, `buildFilters()`, and `openDrawer()`; head comment explains `cv.js` and `pub-images.js`.
- `HANDOFF.md` created: lists the four files to FTP-upload for a CV build handoff, test URL, and summary of what's new.

---

## Session 17 — 2026-03-12

### Code refactoring — Extract CV code to `cv.js`
- Created `cv.js`: an IIFE (~537 lines) that exports `window.CVFormat` with all CV-specific logic
- Moved from `index.html` to `cv.js`: `GDOC_SECTION_MAP/PROJECT_MAP/MONTHS`, gdoc helpers, `parseCVText`, `parseGDoc`, `loadFromGDoc`, `GROUP_ORDER`, `DIM_LABELS`, `DISSEMINATION_GROUPS`, `catSubGroupsFor`, `programGroupsFor`, `computeThemeLanes`, `buildFiltersThemes`, `appendViewModeToggle`, `renderTags`, `lookupPubImage`
- `index.html` reduced by ~437 lines; 17 `CVFormat.*` call sites replace inline CV blocks
- `DISSEMINATION_GROUPS` aliased at module level in `index.html` so existing call sites are unchanged
- Bug fix: added `handle.setPointerCapture(e.pointerId)` to the category drag handler (correct pointer capture for drag; previously relied solely on document-level listeners)
- `test.html` updated: `fw.gdocParseDateRange(...)` → `fw.CVFormat._gdocParseDateRange(...)`; ~25 new assertions covering `CVFormat` module, `parseCVText`, `lookupPubImage`, `DISSEMINATION_GROUPS`, and AbTeC regression

---

## Session 16 — 2026-03-10

### Category drag reorder
- Each row in the Category filter section now has a ⠿ drag handle on the left
- Drag any category up or down to reorder the timeline rows; order updates live during drag
- A floating ghost clone follows the cursor while dragging; the original row stays dimmed in-place as a drop indicator
- Order persists across page refresh (saved to `localStorage`) and is included in saved View files (captured in `captureView()`, restored in `applyView()`)
- `groupOrder` module-level array drives row order in both `redraw()` and `buildExportSVG()`; initialized from localStorage on each `parse()` with new groups appended at the end

### UI — View and File sections
- Both the **View** and **File** sidebar sections now start **collapsed by default** on all platforms (previously only collapsed on touch devices)

### Code refactoring — Readability / Maintainability / Efficiency (Stages 1–3)
- **Stage 2 (trivial fixes):** stale HTTP fallback URL, export title element fix, dead `renderMedia` Case 5 removed, stale `timeline.html` deleted, debug `loadTestData()` call removed, `generateTicks()` safety guard warning, export heuristic comment, `innerHTML` trust comments, CORS proxy trust note
- **Stage 3 (small-effort fixes):** `fh.getParent()` non-standard API removed, `isEventVisible()` extracted (deduplicating 3-way copy-paste), `accordionState.clear()` on reload, `FILTER_LAYOUT` stubs removed, named toolbar action functions (`doZoomIn`, `doZoomOut`, `doToday`), SheetJS pinned to 0.20.3 with SRI hash

### Code refactoring — Optimization (Opt-Stages 1–2)
- **O1** RAF-throttle mousemove: at most one `redraw()` per animation frame during pan
- **O2** Cache `visEvs`: `_visEvsDirty` flag; O(n) filter skipped on pure pan/zoom frames
- **O3** Cache tick arrays by scale level: `generateTicks()` only runs when zoom crosses a threshold
- **O6** Event delegation for event bars: removed ~3 per-element listeners per bar; CSS hover handles opacity; three delegated listeners on `evG` handle tooltip and click
- **O7** Eliminate `getComputedTextLength()` layout flush: replaced with `label.length * 7` heuristic
- **O9** `eventsByGroup` index (`Map<group, Event[]>`) built once in `parse()`; used in `syncCategoryVis()` and `syncDimVis()` — O(g×n) → O(total events)

### Unit tests
- `test.html` expanded to cover all refactor stages and category reorder feature

---

## Session 15 — 2026-03-09

### Search dimming
- Non-matching events dim to 15% opacity when a search query is active, so matching events stand out clearly
- `searchMatchSet` (a `Set` of matching event IDs) maintained alongside `searchResults`; populated in `runSearch()`, cleared in the `input` event handler
- `drawEventBar()` sets `opacity="0.15"` on the event `<g>` when `searchQuery` is set and the event is not in `searchMatchSet`
- Dimming is visual-only — clicking a dimmed event still opens the Storybox; hover still works on matching events

### View save / load
- New **View** section in the sidebar (above the File section) for saving and restoring named snapshots of pan/zoom position + all filter state (Category, Group, Program, Project)
- `captureView(name)` serialises: `scale`, `centreTs` (viewport-centre timestamp — viewport-width-independent), `scrollTop`, and the four filter Sets
- `applyView(v)` restores state: assigns `scale` + recomputes `panX` from `centreTs`, replaces filter Sets (silently discarding values no longer in the dataset), calls `buildFilters()` + `redraw()`
- File format: `<name>.view.json` (`.view` before `.json` per naming convention)
- **File System Access API** (`showSaveFilePicker` / `showOpenFilePicker`) used when available (Chrome/Edge/Brave): real OS save/open dialog; previously-used directory remembered in IndexedDB so the dialog re-opens in the same folder
- Falls back to `<a download>` / `<input type="file">` on Firefox/Safari
- Accordion toggle collapses by default on touch devices; expanded on desktop
- README updated with Search and View sections

---

## Session 14 — 2026-03-09

### Mobile / tablet layout

#### File section redesign
- Replaced separate `#sidebar-files` (inside `#filters`) and `#sidebar-print` with a unified `#sidebar-file-section` containing two named subsections: **Import** and **Export**
- Section header styled to match the **Filters** header (same `color: #9ca3af`, `font-size: 12px`, `font-weight: 700`, `border-bottom`)
- Partial-width divider (`border-top: 1px solid #374151; margin: 0 8px`) separates Import from Export
- Section labelled **File** (singular); collapses/expands via click on header with ▶ arrow indicator
- Loads **collapsed by default** on touch devices; expanded on desktop
- `buildFilters()` no longer saves/restores `#sidebar-files` — it now lives outside `#filters`

#### Touch layout breakpoint — switched from width to capability
- All touch-layout CSS was `@media (max-width: 767px)` — missed iPad entirely
- Width-based attempts (`max-width: 1023px`, `max-width: 1024px`) still failed because iPads in landscape and iPad Pro 12.9" in portrait are ≥1024px wide
- **Final fix**: `@media (hover: none), (max-width: 1024px)` — `hover: none` reliably identifies touch-first devices (iPhone, iPad) in any orientation, without matching laptops

#### Desktop vs iPhone vs iPad differences

| Feature | Desktop | iPhone | iPad |
|---|---|---|---|
| Sidebar | Always visible, resizable | Hidden; slides in via ☰ overlay | Hidden; slides in via ☰ overlay |
| Sidebar width | 220px (resizable) | 280px fixed | 300px fixed |
| Mobile toolbar | Hidden | Fixed top bar: ☰ + title + zoom buttons | Fixed top bar: ☰ + title + zoom buttons |
| App title | In sidebar header | In mobile toolbar (amber) | In mobile toolbar (amber) |
| Zoom controls | In sidebar (`#sidebar-controls`) | In mobile toolbar | In mobile toolbar |
| Storybox (drawer) | 400px side panel | Full width | 480px side panel |
| File drop zone | Visible | Hidden (`#drop-zone { display: none }`) | Hidden |
| File section | Expanded | Collapsed by default | Collapsed by default |
| Zoom hint text | "spacebar + mousewheel / trackpad" | "horizontal pinch" | "horizontal pinch" |
| Touch pan/pinch | Mouse drag + scroll wheel | Custom touch handlers | Custom touch handlers |

#### Other touch fixes (this session)
- File drop zone hidden on touch devices (drag-and-drop not usable on iOS)
- `#mobile-title` span added to `#mobile-toolbar`; `parse()` mirrors title updates to it
- Phone-only overrides (`@media (max-width: 767px)`): sidebar 280px, drawer 100% width
- Tablet overrides: sidebar 300px, drawer 480px

---

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
