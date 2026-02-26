# Changelog

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
