# Smart Mapper — Planning Document

A self-contained import layer that accepts arbitrary tabular or structured data files,
infers how their fields map to the timeline's internal structure, and lets the user
inspect and correct the mapping before applying it.

---

## Goals

- Accept any reasonable input file format without requiring the user to reformat their data
- Work offline when possible; escalate to Claude API only when needed
- Never incur API costs on behalf of users — API key is always the user's own
- Make the inferred mapping transparent: save it as an inspectable, editable file
- Allow a saved mapping to be reused on future imports of the same file structure

---

## Approach: Heuristic-first, Claude API fallback (Option C)

### Stage 1 — Heuristic mapper

Runs automatically on every unrecognised file. Scans column headers (and optionally
a few sample rows) for known synonyms, patterns, and data shapes:

| Target field | Example synonyms to match |
|---|---|
| `start date` | date, start, from, begin, year, when, published, event date |
| `end date` | end, to, until, finish, through |
| `headline` | title, name, headline, event, subject, item, work, label |
| `description` | description, text, body, notes, detail, abstract, summary |
| `group` | group, category, type, section, kind, tag, genre, department |
| `project` | project, initiative, program, theme |
| `media` | media, video, url, link, youtube, vimeo, image |

Matching is case-insensitive and fuzzy (edit distance or prefix match).
Each candidate mapping gets a **confidence score** (0–1).

**Proceed automatically** if:
- At least one date field maps with confidence ≥ 0.8
- At least one title/headline field maps with confidence ≥ 0.8

**Escalate to Stage 2** if:
- No date field found with confidence ≥ 0.5, OR
- No title field found with confidence ≥ 0.5, OR
- User explicitly requests "Try AI mapping" button

### Stage 2 — Claude API mapper

Triggered when heuristics are insufficient or user requests it.

**Input to Claude:**
- Array of column headers
- 5 sample rows (to give Claude data shape context)
- The target field list + descriptions

**Prompt strategy:**
Ask Claude to return a JSON object mapping source column names → target field names,
with a `confidence` ("high" | "medium" | "low") and a `notes` string per field
explaining its reasoning. This makes the output auditable.

**API key handling:**
- User enters their Anthropic API key once in the sidebar (collapsible "AI mapping" section)
- Key stored in `localStorage` under `timeline-claude-api-key`
- Never sent anywhere except directly to `api.anthropic.com` from the user's browser
- Clear warning shown: "Calls to the Claude API are charged to your account"
- Key input is type=password and never logged or persisted server-side (there is no server)

**Model:** `claude-haiku-4-5` — cheapest, fast, sufficient for structured mapping tasks.
A single mapping call should cost < $0.001.

---

## Supported input formats

| Format | How detected | Notes |
|---|---|---|
| `.xlsx` / `.xls` | File extension | Parsed with SheetJS (already loaded) |
| `.csv` | File extension | Parsed with SheetJS |
| `.txt` | File extension | Try CV plain-text parser first; fall through to smart mapper if no CV sections found |
| `.json` | File extension | Try ORCID detection first; fall through to smart mapper if not ORCID |
| `.tsv` | File extension | Parse as tab-delimited via SheetJS |

---

## Mapping file format

After inference (by either method), the mapper saves a `.mapping.json` file to the
user's downloads folder. Example:

```json
{
  "mappedAt": "2026-03-15",
  "sourceFile": "my-grants.xlsx",
  "method": "heuristic",
  "confidence": "high",
  "fields": {
    "Grant Title":   { "target": "headline",    "confidence": 0.91 },
    "Start Year":    { "target": "start date",  "confidence": 0.88 },
    "End Year":      { "target": "end date",    "confidence": 0.85 },
    "Description":   { "target": "description", "confidence": 0.95 },
    "Category":      { "target": "group",       "confidence": 0.80 },
    "Funding Body":  { "target": null,          "confidence": 0.0, "note": "No matching target field" }
  }
}
```

`target: null` means the column was not mapped — the user can edit the file and
assign it manually, then re-load the mapping.

---

## UI changes

### Sidebar — File section

Add a third subsection below the URL field:

```
[ Import ]
  Drop zone (existing)
  URL / ID field (existing)
  ─────────────────────
  [ Smart Import ]         ← new collapsible subsection
    [ AI mapping (optional) ] ← nested collapsible
      API key: [______________] ← type=password, stored in localStorage
      ⚠ Charges apply to your account
    Mapping file: [Browse…] ← load a saved .mapping.json
    Status: "Mapped 5 of 6 columns (heuristic, high confidence)"
    [ Save mapping… ] [ Apply ] ← shown after inference
```

### Mapping review

After inference, before applying:
- Show a compact table in the sidebar: source column → mapped field, confidence indicator
- Unmapped columns shown in amber
- Low-confidence mappings shown in yellow
- User can click **Apply** to proceed or **Save mapping…** to download the `.mapping.json`
  for inspection and editing before applying

---

## Implementation plan

1. **`utilities/smart-mapper.js`** — new file, exports `window.SmartMapper`
   - `SmartMapper.detect(headers, rows)` → mapping object (heuristic stage)
   - `SmartMapper.detectWithClaude(headers, rows, apiKey)` → mapping object (Claude stage)
   - `SmartMapper.applyMapping(rows, mapping)` → normalized rows ready for `parse()`
   - `SmartMapper.confidence(mapping)` → `'high' | 'medium' | 'low'`

2. **`index.html`** — wire up:
   - New "Smart Import" subsection in sidebar HTML + CSS
   - Call `SmartMapper.detect()` from `load()` as fallback when format is unrecognised
   - Show mapping review UI before calling `parse()`
   - API key input handling + localStorage persistence

3. **`utilities/orcid-utilities.js`** and **`utilities/cv-utilities.js`** — no changes needed;
   smart mapper only runs after both existing detectors have already declined the file

---

## Open questions

- Should the mapping review UI be inline in the sidebar, or a modal/drawer?
  (Sidebar keeps interaction contained; modal gives more space for a wider table)
- Should low-confidence heuristic mappings skip straight to Claude, or always show
  the heuristic result first and let the user decide whether to escalate?
- For `.txt` files that aren't CV-format: smart mapper would need to choose a
  delimiter and interpret the structure, which is harder than tabular data —
  may want to limit `.txt` smart mapping to "suggest re-saving as .csv" rather
  than attempting full inference
