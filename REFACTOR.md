# REFACTOR.md — Timeline-JEL Code Review

Each stage represents one refactoring cycle: an audit pass followed by a fix pass.
Latest stage is at the top; earliest stage is at the bottom.

---

## Stage 3 — Small-Effort Fix Pass

**Date:** 2026-03-10
**Branch:** `Timeline-AbTeC-Media` @ (pending commit)
**Status:** Complete.

Applied all 6 remaining "small effort" items from Stage 1:

| # | Issue | Resolution |
|---|-------|------------|
| 4 | `fh.getParent()` non-standard API | Removed both calls; added explanatory comments |
| 7 | Event visibility logic duplicated 3× | Extracted `isEventVisible(e)`; all 3 sites replaced |
| 8 | `accordionState` never cleared on reload | Added `accordionState.clear()` at start of `parse()` |
| 9 | `FILTER_LAYOUT` stubs — dead code | Removed variable + 3 stub functions; added PLANNED comment; simplified dispatch |
| 10 | Mobile toolbar delegates via `.click()` | Extracted `doZoomIn`, `doZoomOut`, `doToday`; both toolbars call directly |
| 14 | CDN dependencies without SRI hashes | Pinned SheetJS to `0.20.3`; added `integrity` + `crossorigin` attributes |

**Unit tests:** `test.html` — Stage 3 tests added. Run via `serve.sh`, open `http://localhost:8000/test.html`.

---

## Stage 2 — Trivial Fix Pass

**Date:** 2026-03-10
**Branch:** `Timeline-AbTeC-Media` @ `1f0e66d`
**Commit:** `Apply trivial refactor fixes from REFACTOR.md`
**Status:** Complete.

Applied all 9 trivial items from Stage 1:

| # | Issue | Resolution |
|---|-------|------------|
| 1 | Stale HTTP fallback URL | Changed to `timeline-data.xlsx` |
| 2 | Export title reads wrong element | Changed to `#sidebar-title-text` (both call sites) |
| 3 | Unreachable `renderMedia` Case 5 | Deleted dead block |
| 5 | `timeline.html` stale file | Deleted from repo (`git rm`) |
| 6 | Commented-out `loadTestData()` | Deleted the line |
| 11 | `generateTicks()` silent guard | Added `console.warn` when limit hits |
| 12 | Export text-width heuristic | Added inline comment documenting 6.5px/char |
| 13 | `innerHTML` trust assumption | Added comments at both injection sites |
| 15 | CORS proxy trust note | Added inline comment on `GSHEET_PROXY` constant |

**Unit tests:** `test.html` — 65 tests, all passing @ `09fb974`. Run via `serve.sh`, open `http://localhost:8000/test.html`.

**Remaining from Stage 1 (small effort):**

| # | Issue | Effort |
|---|-------|--------|
| 4 | Fix or remove `fh.getParent()` | Small |
| 7 | Extract `isEventVisible()` | Small |
| 8 | Clear `accordionState` on reload | Small |
| 9 | Remove `FILTER_LAYOUT` stubs | Small |
| 10 | Named action functions for toolbars | Small |
| 14 | SRI hashes for CDN deps | Small |

---

## Stage 1 — Initial Audit

**Date:** 2026-03-10
**Branch:** `Timeline-AbTeC-Media` @ `637ff12`
**File:** `index.html` (~3,710 lines)
**Status:** Audit complete. Fixes applied in Stage 2.

### Bugs / Stale Code

#### 1. Stale HTTP fallback URL (`line 3136`)
The auto-load fallback for HTTP serving still references the old filename:
```js
fetch('data/timeline-data/IIF-Timeline-Data-Multi-Project.xlsx')
```
File was renamed to `timeline-data.xlsx` in an early session. This silently falls through to
synthetic test data whenever the app is served over HTTP without the pre-generated JS data file.

**Fix:** Change to `data/timeline-data/timeline-data.xlsx`.

---

#### 2. Export title reads back wrong element (`lines 3210, 3364`)
The Markdown list export and PDF export both get the title string by reading:
```js
document.getElementById('sidebar-title').textContent
```
`#sidebar-title` is the parent div, which includes the `#sidebar-byline` span ("by JEL & Claude").
Result: export title renders as `"AbTeC Timelineby JEL & Claude"` (no space, byline included).

**Fix:** Read `#sidebar-title-text` instead of `#sidebar-title`.

---

#### 3. Unreachable code in `renderMedia()` (`~line 2630`)
"Case 5: video only (fallthrough)" comment describes code that can never execute —
YouTube/Vimeo matches already `return` earlier in the function. `vidHtml` is always `''` here.

**Fix:** Delete the dead block and its comment.

---

#### 4. `fh.getParent()` non-standard API (`lines 3643, 3667`)
`FileSystemFileHandle.getParent()` does not exist in any browser (unshipped proposal).
The `.catch(() => null)` handles failure gracefully, but the "remember last directory" feature
silently does nothing in practice.

**Fix:** Either remove the feature entirely, or replace with `showDirectoryPicker()` at save time.

---

#### 5. `timeline.html` — stale file
The old filename before the `index.html` rename (for GitHub Pages). Still present in the repo.
Content is likely out of sync and will confuse new collaborators.

**Fix:** Delete `timeline.html` from the repo.

---

#### 6. Commented-out debug call (`line 3204`)
```js
// loadTestData();
```
Leftover from debugging. Harmless but noisy.

**Fix:** Delete the line.

---

### Maintainability

#### 7. Visibility filter logic duplicated in 3 places
The event visibility OR-logic (groupVis + orgVis + programVis + projVis) is copy-pasted in:
- `redraw()` at lines ~2407–2419
- `getVisibleEvents()` at lines ~2557–2566
- `buildExportSVG()` at lines ~3326–3334

A change to filter semantics requires updating all three sites consistently.

**Fix:** Extract to a single `isEventVisible(ev)` function; call it in all three places.

---

#### 8. `accordionState` never cleared on data reload
`accordionState` is a module-level `Map` keyed by section title. It is never reset when a new
file is loaded. Keys from a previous data source (e.g. CV filter sections) persist and can
surface subtle open/closed state oddities if same-named sections appear in a subsequent load.

**Fix:** Clear `accordionState` at the start of `parse()`, or scope it to the current dataset.

---

#### 9. `FILTER_LAYOUT` stubs — dead code
Three empty function bodies exist with TODO comments:
```js
function buildFiltersChipsBar() {}
function buildFiltersDocToggles() {}
function buildFiltersTabs() {}
```
`FILTER_LAYOUT` is hardcoded to `'accordion'` with no UI to change it. These stubs add noise
for any new reader trying to understand the filter system.

**Fix:** Remove the stubs and the `FILTER_LAYOUT` variable until this feature is actually built,
or add a `// PLANNED: ...` comment at the top of `buildFilters()` instead.

---

#### 10. Mobile toolbar delegates via `.click()` (`lines 3703–3706`)
```js
document.getElementById('mob-zoomin').addEventListener('click', () =>
  document.getElementById('btn-zoomin').click());
```
Four mobile toolbar buttons each fire `.click()` on their sidebar counterparts. Silently breaks
if sidebar button IDs change.

**Fix:** Extract zoom/fit/today actions into named functions; call those directly from both
toolbars.

---

#### 11. `generateTicks()` silent safety guard
```js
safety++ < 800
```
The loop has a hard cutoff at 800 iterations with no console warning or visible error if it hits.
Failure mode is a partially-drawn axis with no indication of why.

**Fix:** Add `console.warn('generateTicks: safety limit hit')` when the guard fires.

---

#### 12. Two parallel text-width calculations
`drawEventBar()` uses `getComputedTextLength()` (requires live DOM attachment) for precise
in-bar label fitting. `buildExportSVG()` uses a 6.5px/char heuristic instead. These can
produce different label truncation behavior between live view and PDF export.

**Note:** Acceptable as-is for now — document the discrepancy with a comment in `buildExportSVG()`.

---

### Security (Low Practical Risk)

These are low risk for a single-user local tool but worth documenting for collaborators.

#### 13. `innerHTML` with data-file values
Several innerHTML assignments use values from the loaded data file without sanitization:
- Event group label (`~line 2651`)
- Enrichment tag pill text (`~line 2738`)

If the tool ever becomes multi-user or accepts untrusted data sources, these are XSS vectors.

**Fix for now:** Add a comment noting the assumption that data is user-controlled and trusted.
**Fix for multi-user:** Use `textContent` / `createElement` instead of `innerHTML` for data values.

---

#### 14. CDN dependencies without SRI hashes (`lines 7–10`)
Google Fonts and SheetJS are loaded from CDNs without `integrity=""` (Subresource Integrity)
attributes. A compromised CDN could inject malicious code.

**Fix:** Add SRI hashes. SheetJS publishes them in their release notes.

---

#### 15. CORS proxy sends full URLs to third party (`line 1105`)
Google Sheets/Doc URLs are proxied through `https://corsproxy.io/?` as a fallback.
`noembed.com` is similarly third-party. Both receive the full resource URL.

**Note:** Acceptable for public URLs. Worth documenting for collaborators so they understand
the trust model.

---

### Stage 1 Priority Order

| # | Issue | Effort | Impact |
|---|-------|--------|--------|
| 1 | Stale HTTP fallback URL | Trivial | Fixes silent data-load failure over HTTP |
| 2 | Export title reads wrong element | Trivial | Fixes malformed export titles |
| 5 | Delete `timeline.html` | Trivial | Reduces collaborator confusion |
| 6 | Remove commented debug call | Trivial | Minor cleanup |
| 3 | Remove unreachable `renderMedia` code | Trivial | Cleanup |
| 11 | `generateTicks()` warning | Trivial | Better failure visibility |
| 13 | `innerHTML` data safety comments | Trivial | Documents trust assumption |
| 12 | Document export text-width heuristic | Trivial | Improves maintainability |
| 15 | CORS proxy trust note | Trivial | Documents for collaborators |
| 7 | Extract `isEventVisible()` | Small | Eliminates 3-way duplication |
| 10 | Named action functions for toolbars | Small | Removes fragile `.click()` delegation |
| 8 | Clear `accordionState` on reload | Small | Eliminates subtle state bugs |
| 9 | Remove `FILTER_LAYOUT` stubs | Small | Reduces dead code noise |
| 4 | Fix or remove `getParent()` | Small | Fixes silently broken feature |
| 14 | SRI hashes for CDN deps | Small | Reduces supply-chain risk |
