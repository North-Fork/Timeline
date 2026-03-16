(function () {
  'use strict';

  // === GDOC lookup tables ===

  const GDOC_SECTION_MAP = {
    'employment history':        'Employment',
    'education':                 'Education',
    'honors and awards':         'Honors',
    'books':                     'Books',
    'book chapters':             'Book Chapters',
    'journal articles & conference proceedings (refereed)': 'Journal Articles',
    'journal articles & conference proceedings':            'Journal Articles',
    'journal articles and conference proceedings':          'Journal Articles',
    'conference / symposia presentations (refereed)':       'Conference Presentations',
    'conference / symposia presentations':                  'Conference Presentations',
    'keynote, plenary, and special guest speaker':          'Keynotes',
    'invited publications':      'Invited Publications',
    'invited lectures / artist talks / panels': 'Invited Lectures',
    "artist's books and exhibition publications": "Artist's Books",
    'symposium, workshop, and lecture series organizer or lead': 'Symposia Organized',
    'promotion review / peer reviewer / jury member / expert assessor': 'Service',
    'documentaries':             'Documentaries',
    'websites':                  'Websites',
    'residencies':               'Residencies',
    'residency organizer':       'Residency Organizer',
    'academic review & textbook inclusion': 'Academic Reviews',
    'op-ed':                     'Op-Ed',
    'press coverage / interviews / documentaries': 'Press Coverage',
    'policy papers, governmental presentations, reviews & consultations': 'Policy & Reports',
    'exhibitions - solo':        'Solo Exhibitions',
    'exhibitions - group':       'Group Exhibitions',
    'film screenings':           'Film Screenings',
    'commissions':               'Commissions',
    'poetry publication & performances': 'Poetry',
    'curatorial':                'Curatorial',
    'visiting artist & master classes':  'Visiting Artist',
    'producer / executive producer':     'Productions',
    'major works':               'Creative Works',
  };

  const GDOC_PROJECT_MAP = {
    'Employment':               'Concordia',
    'Education':                'Early Career',
    'Honors':                   'Recognition',
    'Books':                    'Research',
    'Book Chapters':            'Research',
    'Journal Articles':         'Research',
    'Conference Presentations': 'Research',
    'Keynotes':                 'IIF',
    'Invited Publications':     'Research',
    'Invited Lectures':         'Research',
    "Artist's Books":           'Creative',
    'Symposia Organized':       'Research',
    'Service':                  'Research',
    'Documentaries':            'AbTeC',
    'Websites':                 'Creative',
    'Residencies':              'Research',
    'Residency Organizer':      'Research',
    'Academic Reviews':         'Research',
    'Op-Ed':                    'Research',
    'Press Coverage':           'Research',
    'Policy & Reports':         'Research',
    'Solo Exhibitions':         'Creative',
    'Group Exhibitions':        'Creative',
    'Film Screenings':          'AbTeC',
    'Commissions':              'Creative',
    'Poetry':                   'Creative',
    'Curatorial':               'Creative',
    'Visiting Artist':          'Research',
    'Productions':              'AbTeC',
    'Creative Works':           'Creative',
  };

  const GDOC_MONTHS = {
    jan:1, feb:2, mar:3, apr:4, may:5, jun:6,
    jul:7, aug:8, sep:9, oct:10, nov:11, dec:12,
    january:1, february:2, march:3, april:4, june:6,
    july:7, august:8, september:9, october:10, november:11, december:12,
  };

  // === Date-parsing and gdoc helpers ===

  function gdocFmt(y, m = 1, d = 1) {
    return `${String(m).padStart(2,'0')}/${String(d).padStart(2,'0')}/${String(y).padStart(4,'0')}`;
  }

  function gdocYy4(yy) { return yy <= 29 ? 2000 + yy : 1900 + yy; }

  function gdocParseDateRange(s) {
    s = s.trim().replace(/[\u2013\u2014]/g, '-').replace(/\s*-\s*/g, '-');
    const today = new Date();
    const todayStr = gdocFmt(today.getFullYear(), today.getMonth() + 1, today.getDate());
    let m;

    // M.YY-present — must come before letter check
    m = s.match(/^(\d{1,2})\.(\d{2,4})-present$/i);
    if (m) {
      const yr = parseInt(m[2]);
      return [gdocFmt(yr > 100 ? yr : gdocYy4(yr), parseInt(m[1])), todayStr];
    }

    if (/[A-Za-z]/.test(s)) {
      if (s.toLowerCase() === 'present') return [todayStr, todayStr];
      // "Month. D-D, YYYY"
      m = s.match(/^([A-Za-z]+)\.?\s+\d{1,2}-\d{1,2},?\s*(\d{4})$/);
      if (m) { const mon = GDOC_MONTHS[m[1].toLowerCase().slice(0,3)]; if (mon) { const d = gdocFmt(parseInt(m[2]),mon,1); return [d,d]; } }
      // "D Month, YYYY"
      m = s.match(/^(\d{1,2})\s+([A-Za-z]+),?\s*(\d{4})$/);
      if (m) { const mon = GDOC_MONTHS[m[2].toLowerCase().slice(0,3)]; if (mon) { const d = gdocFmt(parseInt(m[3]),mon,parseInt(m[1])); return [d,d]; } }
      // "Month. D, YYYY"
      m = s.match(/^([A-Za-z]+)\.?\s+(\d{1,2}),?\s*(\d{4})$/);
      if (m) { const mon = GDOC_MONTHS[m[1].toLowerCase().slice(0,3)]; if (mon) { const d = gdocFmt(parseInt(m[3]),mon,parseInt(m[2])); return [d,d]; } }
      // "Month YYYY"
      m = s.match(/^([A-Za-z]+)\.?\s+(\d{4})$/);
      if (m) { const mon = GDOC_MONTHS[m[1].toLowerCase().slice(0,3)]; if (mon) { const d = gdocFmt(parseInt(m[2]),mon,1); return [d,d]; } }
      return [null, null];
    }

    // M.YY-M.YY or M.YY-present (numeric)
    m = s.match(/^(\d{1,2})\.(\d{2,4})-(present|\d{1,2}\.\d{2,4})$/i);
    if (m) {
      const yr = parseInt(m[2]), startY = yr > 100 ? yr : gdocYy4(yr);
      const start = gdocFmt(startY, parseInt(m[1]));
      const ep = m[3];
      if (ep.toLowerCase() === 'present') return [start, todayStr];
      const em = ep.match(/^(\d{1,2})\.(\d{2,4})$/);
      if (em) { const ey = parseInt(em[2]); return [start, gdocFmt(ey > 100 ? ey : gdocYy4(ey), parseInt(em[1]))]; }
      return [start, start];
    }
    // M.YY or M.YYYY
    m = s.match(/^(\d{1,2})\.(\d{2,4})$/);
    if (m) { const yr = parseInt(m[2]); const d = gdocFmt(yr > 100 ? yr : gdocYy4(yr), parseInt(m[1])); return [d,d]; }
    // YYYY-YY
    m = s.match(/^(\d{4})-(\d{2})$/);
    if (m) { const sy = parseInt(m[1]), ey = Math.floor(sy/100)*100 + parseInt(m[2]); return [gdocFmt(sy), gdocFmt(ey,6,30)]; }
    // YYYY-YYYY
    m = s.match(/^(\d{4})-(\d{4})$/);
    if (m) return [gdocFmt(parseInt(m[1])), gdocFmt(parseInt(m[2]))];
    // YYYY
    m = s.match(/^(\d{4})$/);
    if (m) { const d = gdocFmt(parseInt(m[1])); return [d,d]; }

    return [null, null];
  }

  function gdocSplitNbsp(text) {
    const m = text.match(/^(.+?)[\xa0]{2,}([\s\S]*)/);
    return m ? [m[1].trim(), m[2].trim()] : [null, text];
  }

  function gdocExtractTitle(text) {
    const m = text.match(/["\u201c]([^"\u201d]{4,})["\u201d]/);
    if (m) return m[1].trim();
    const parts = text.split(/(?<=[a-z)])[.;]/);
    return (parts[0] || text).trim().slice(0, 200);
  }

  function gdocExtractLink(tag) {
    const unwrap = a => {
      let href = a.getAttribute('href') || '';
      const qm = href.match(/[?&]q=([^&]+)/);
      return qm ? decodeURIComponent(qm[1]) : href;
    };
    // Look for a {text} link: an <a> whose text content is exactly "text" (or
    // "{text}" if the whole thing was hyperlinked). Google Docs places { and }
    // as plain text around it, but may insert empty spans between them and the
    // <a>, so sibling checks are unreliable — link text is the safe signal.
    for (const a of tag.querySelectorAll('a[href]')) {
      if (/^text$|^\{text\}$/i.test((a.textContent || '').trim()))
        return { url: unwrap(a), label: 'Text' };
    }
    // Fall back to first link
    const a = tag.querySelector('a[href]');
    return a ? { url: unwrap(a), label: 'More Info' } : { url: '', label: 'More Info' };
  }

  // === Parsers ===

  // Same 3-strategy logic as parseGDoc() but splits on tabs / 2+ spaces
  // instead of \xa0\xa0+, and works line-by-line on plain text.
  function parseCVText(text) {
    const rows = [];
    let group = null, lastRow = null;

    for (const rawLine of text.replace(/\r\n/g, '\n').replace(/\r/g, '\n').split('\n')) {
      const line = rawLine.trim();
      if (!line || line.length < 2) continue;

      // Section heading?
      const key = line.toLowerCase().replace(/[\s\xa0]+/g, ' ').trim().replace(/:$/, '');
      if (GDOC_SECTION_MAP[key]) { group = GDOC_SECTION_MAP[key]; lastRow = null; continue; }

      if (!group) continue;

      // Strategy 1: date prefix + tab or 2+ spaces
      const sep = rawLine.match(/^(.+?)(?:\t+|\s{2,})(.+)$/);
      if (sep) {
        const cleanDate = sep[1].trim();
        const rest      = sep[2].trim().replace(/\s*\{[^}]*\}\s*$/, '').trim();
        const [start, end] = gdocParseDateRange(cleanDate);
        if (start) {
          const row = { 'start date': start, 'end date': end || start,
            'headline': rest, 'description': '', 'group': group, 'project': GDOC_PROJECT_MAP[group] || '' };
          rows.push(row); lastRow = row;
          continue;
        }
      }

      // Strategy 2: continuation line
      const hasYear = /\b(19|20)\d{2}\b/.test(line);
      if (lastRow && lastRow['group'] === group && !hasYear && line.length < 150) {
        lastRow['description'] = lastRow['description'] ? lastRow['description'] + '  ' + line : line;
        continue;
      }

      // Strategy 3: bibliography — extract year from text
      const years = [...line.matchAll(/\b(19\d{2}|20\d{2})\b/g)].map(m => parseInt(m[1]));
      if (years.length) {
        const year = years[years.length - 1];
        const d = gdocFmt(year);
        const row = { 'start date': d, 'end date': d,
          'headline': gdocExtractTitle(line), 'description': line, 'group': group, 'project': GDOC_PROJECT_MAP[group] || '' };
        rows.push(row); lastRow = row;
      }
    }
    return rows;
  }

  function parseGDoc(html) {
    const doc = new DOMParser().parseFromString(html, 'text/html');
    const rows = [];
    let group = null, lastRow = null;

    for (const tag of doc.querySelectorAll('h1,h2,h3,h4,h5,h6,p,li')) {
      const rawTag = tag.textContent || '';
      const text = rawTag.trim();
      if (!text || text.length < 2) continue;

      if (/^H[1-6]$/.test(tag.tagName)) {
        const key = text.toLowerCase().replace(/[\s\xa0]+/g, ' ').trim().replace(/:$/, '');
        if (GDOC_SECTION_MAP[key]) { group = GDOC_SECTION_MAP[key]; lastRow = null; }
        continue;
      }

      if (!group) continue;

      const entryLink = gdocExtractLink(tag);

      // Strategy 1: date prefix + \xa0\xa0+ separator
      const [dateCandidate, rest] = gdocSplitNbsp(rawTag);
      if (dateCandidate) {
        const cleanDate = dateCandidate.replace(/\xa0/g, '').trim();
        const [start, end] = gdocParseDateRange(cleanDate);
        if (start) {
          const restClean = rest.replace(/\xa0/g, ' ').replace(/\s*\{[^}]*\}\s*$/, '').trim();
          const headlineVal = entryLink.url ? `<a href="${entryLink.url}">${restClean}</a>` : restClean;
          const row = { 'start date': start, 'end date': end || start,
            'headline': headlineVal, 'headline link label': entryLink.url ? entryLink.label : '',
            'description': '', 'group': group, 'project': GDOC_PROJECT_MAP[group] || '' };
          rows.push(row); lastRow = row;
          continue;
        }
      }

      // Strategy 2: continuation line
      const clean = text.replace(/[\xa0\s]+/g, ' ').trim();
      const hasYear = /\b(19|20)\d{2}\b/.test(clean);
      if (lastRow && lastRow['group'] === group && !hasYear && clean.length < 150) {
        const addition = clean.replace(/\s*\{[^}]*\}\s*/g, ' ').trim();
        if (addition) lastRow['description'] = lastRow['description'] ? lastRow['description'] + '  ' + addition : addition;
        continue;
      }

      // Strategy 3: bibliography — extract year from text
      const cleanFull = text.replace(/[\xa0]+/g, ' ').replace(/\s*\{[^}]*\}\s*/g, ' ').trim();
      const years = [...cleanFull.matchAll(/\b(19\d{2}|20\d{2})\b/g)].map(m => parseInt(m[1]));
      if (years.length) {
        const year = years[years.length - 1];
        const d = gdocFmt(year);
        const titleText = gdocExtractTitle(cleanFull);
        const headlineVal = entryLink.url ? `<a href="${entryLink.url}">${titleText}</a>` : titleText;
        const row = { 'start date': d, 'end date': d,
          'headline': headlineVal, 'headline link label': entryLink.url ? entryLink.label : '',
          'description': cleanFull, 'group': group, 'project': GDOC_PROJECT_MAP[group] || '' };
        rows.push(row); lastRow = row;
      }
    }
    return rows;
  }

  // === loadFromGDoc ===
  // Generic Google Doc CV loader.
  // opts: { statusEl, proxy, lsKey }
  async function loadFromGDoc(url, parse, opts) {
    const statusEl = opts && opts.statusEl;
    const proxy    = (opts && opts.proxy)  || '';
    const lsKey    = (opts && opts.lsKey)  || '';

    if (statusEl) { statusEl.textContent = 'Loading…'; statusEl.style.color = '#6b7280'; }

    // Ensure URL ends with /pub
    let pubUrl = url.trim();
    if (!pubUrl.match(/\/pub(\?|$)/)) {
      pubUrl = pubUrl.replace(/\/document\/d\/([^\/]+).*$/, '/document/d/$1/pub');
    }

    const tryFetch = async u => {
      const r = await fetch(u, { cache: 'no-store' });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return r.text();
    };

    let html;
    try {
      html = await tryFetch(pubUrl);
    } catch {
      try {
        html = await tryFetch(proxy + encodeURIComponent(pubUrl));
      } catch (ex) {
        if (statusEl) { statusEl.textContent = 'Failed: ' + ex.message; statusEl.style.color = '#ef4444'; }
        return;
      }
    }

    try {
      const rows = parseGDoc(html);
      if (!rows.length) throw new Error('No CV sections found — is the doc published to the web?');
      parse(rows);
      if (lsKey) localStorage.setItem(lsKey, url);
      if (statusEl) { statusEl.textContent = `✓ Loaded ${rows.length} entries`; statusEl.style.color = '#22c55e'; }
    } catch (ex) {
      if (statusEl) { statusEl.textContent = 'Parse error: ' + ex.message; statusEl.style.color = '#ef4444'; }
    }
  }

  // === Parse-phase helpers ===

  // CV-specific GROUP_ORDER
  const GROUP_ORDER = [
    'Employment', 'Honors', 'Education',
    'Creative Works', 'Books/Chapters', 'Journal Articles',
    'Keynotes', 'Conference Presentations', 'Invited Publications', 'Invited Lectures',
    'Policy Papers', 'Op-Ed', "Artist's Books", 'Poetry',
    'Solo Exhibitions', 'Group Exhibitions',
    'Film Screenings', 'Commissions', 'Curatorial', 'Visiting Artist', 'Productions',
    'Residencies', 'Residency Organizer',
    'Documentaries', 'Websites',
    'Press Coverage', 'Academic Reviews', 'Symposia Organized',
    'Funding (PI)', 'Funding (Co-I)', 'Funding (Internal)',
    'Courses Taught',
    'Postdoc', 'PhD', 'Masters', 'Grad Certificate', 'Undergraduate',
    'Service',
  ];

  // CV-specific dimension labels
  const DIM_LABELS = { orgs: 'Institution', programs: 'Funding Agency', projects: 'Role' };

  // Groups whose events may have publication cover images
  const DISSEMINATION_GROUPS = new Set([
    'Books/Chapters', 'Books', 'Book Chapters',
    'Journal Articles', 'Invited Publications', 'Op-Ed',
  ]);

  // Build category sub-groups for CV (Art, Dissemination, Supervision parent groupings)
  // Returns null if no events have a categoryGroup set.
  function catSubGroupsFor(groups, events) {
    const CG_ORDER = ['Art', 'Dissemination', 'Supervision'];
    const byCatGroup = new Map();
    const ungroupedCats = [];
    for (const g of groups) {
      const cg = events.find(e => e.group === g)?.categoryGroup || '';
      if (cg) {
        if (!byCatGroup.has(cg)) byCatGroup.set(cg, []);
        byCatGroup.get(cg).push(g);
      } else {
        ungroupedCats.push(g);
      }
    }
    if (!byCatGroup.size) return null;
    const result = CG_ORDER
      .filter(cg => byCatGroup.has(cg))
      .map(cg => ({ label: cg, items: byCatGroup.get(cg) }));
    if (ungroupedCats.length) result.push({ label: 'Other', items: ungroupedCats });
    return result;
  }

  // Build program sub-groups for CV (Tri-council, Concordia, then ungrouped)
  // Returns array (may be empty).
  function programGroupsFor(programs, events) {
    const FG_ORDER = ['Tri-council', 'Concordia'];
    const byGroup  = new Map();
    const ungrouped = [];
    for (const prog of programs) {
      const fg = events.find(e => e.program === prog)?.fundingGroup || '';
      if (fg) {
        if (!byGroup.has(fg)) byGroup.set(fg, []);
        byGroup.get(fg).push(prog);
      } else {
        ungrouped.push(prog);
      }
    }
    const result = FG_ORDER
      .filter(fg => byGroup.has(fg))
      .map(fg => ({ label: fg, items: byGroup.get(fg) }));
    if (ungrouped.length) result.push({ label: 'Other', items: ungrouped });
    return result;
  }

  // === Theme system ===

  // Compute per-theme lane assignments.
  // Returns { themeLaneCounts, themeRowH, themeLanes }.
  function computeThemeLanes(events, themeRows, minEffMs = 86400000) {
    const ROW_H   = 28;
    const LANE_H  = 22;
    const LANE_PAD = 4;
    const themeLaneCounts = {};
    const themeRowH = {};
    const themeLanes = {};
    for (const theme of themeRows) {
      const tEvs = events.filter(e => e.themes.includes(theme))
                         .sort((a, b) => a.startTs - b.startTs);
      const laneEnds = [];
      themeLanes[theme] = {};
      for (const ev of tEvs) {
        const effEnd = Math.max(ev.endTs, ev.startTs + minEffMs);
        let placed = false;
        for (let i = 0; i < laneEnds.length; i++) {
          if (ev.startTs >= laneEnds[i]) {
            themeLanes[theme][ev.id] = i; laneEnds[i] = effEnd; placed = true; break;
          }
        }
        if (!placed) { themeLanes[theme][ev.id] = laneEnds.length; laneEnds.push(effEnd); }
      }
      themeLaneCounts[theme] = Math.max(1, laneEnds.length);
      themeRowH[theme] = Math.max(ROW_H, themeLaneCounts[theme] * LANE_H + LANE_PAD * 2);
    }
    return { themeLaneCounts, themeRowH, themeLanes };
  }

  // Build themes filter panel, appending to filDiv.
  // makeAllNoneButtons and makeFilterItems are passed in from index.html.
  function buildFiltersThemes(filDiv, themeRows, themeVis, themeColor, cntEl,
                               makeAllNoneButtons, makeFilterItems) {
    const panelTitle = document.createElement('div');
    panelTitle.className = 'filter-panel-title';
    panelTitle.textContent = 'Themes';
    panelTitle.appendChild(cntEl);
    filDiv.appendChild(panelTitle);

    const allNone = makeAllNoneButtons(themeRows, themeVis, false, false);
    filDiv.appendChild(allNone);

    const body = document.createElement('div');
    makeFilterItems(body, themeRows, themeVis, t => themeColor[t], false, false);
    filDiv.appendChild(body);
  }

  // Append the sections/themes view-mode toggle to filDiv.
  // onModeChange(mode) is called when the user clicks a mode button.
  function appendViewModeToggle(filDiv, currentMode, onModeChange) {
    const tog = document.createElement('div');
    tog.className = 'view-mode-toggle';
    ['sections', 'themes'].forEach(mode => {
      const btn = document.createElement('button');
      btn.className = 'view-mode-btn' + (currentMode === mode ? ' active' : '');
      btn.textContent = mode.charAt(0).toUpperCase() + mode.slice(1);
      btn.addEventListener('click', () => {
        if (currentMode === mode) return;
        onModeChange(mode);
      });
      tog.appendChild(btn);
    });
    filDiv.appendChild(tog);
  }

  // === Drawer helpers ===

  // Render enrichment tag sections (themes, concepts, collaborators) for ev.
  // Mutates #d-themes, #d-concepts, #d-collaborators elements via document.
  function renderTags(doc, ev) {
    const render = (elId, tags, cssClass, title) => {
      const el = doc.getElementById(elId);
      if (!el) return;
      if (tags && tags.length) {
        // Trust assumption: tag strings come from user-controlled enrichment data; not sanitized.
        const pills = tags.map(t => `<span class="d-tag ${cssClass}">${t}</span>`).join('');
        el.innerHTML = `<div class="d-tags"><h3>${title}</h3><div class="d-tag-list">${pills}</div></div>`;
      } else {
        el.innerHTML = '';
      }
    };
    render('d-themes',        ev.themes,        'theme',        'Themes');
    render('d-concepts',      ev.concepts,      'concept',      'Concepts');
    render('d-collaborators', ev.collaborators, 'collaborator', 'Collaborators');
  }

  // Look up a publication cover image URL for ev from the pubImgs map.
  // Returns the URL string, or null if not found.
  // Only looks up images for events in DISSEMINATION_GROUPS.
  function lookupPubImage(ev, pubImgs) {
    if (!DISSEMINATION_GROUPS.has(ev.group)) return null;
    // Exact match first, then fuzzy: normalize to lowercase words and check if
    // any key starts with the headline (or vice versa)
    let imgUrl = pubImgs[ev.headline];
    if (!imgUrl) {
      const norm = s => s.toLowerCase().replace(/[^\w\s]/g, ' ').replace(/\s+/g, ' ').trim();
      const hNorm = norm(ev.headline);
      for (const [key, url] of Object.entries(pubImgs)) {
        const kNorm = norm(key);
        if (kNorm.startsWith(hNorm) || hNorm.startsWith(kNorm.slice(0, Math.max(15, hNorm.length)))) {
          imgUrl = url;
          break;
        }
      }
    }
    return imgUrl || null;
  }

  window.CVFormat = {
    parseCVText,
    parseGDoc,
    loadFromGDoc,
    GROUP_ORDER,
    DIM_LABELS,
    DISSEMINATION_GROUPS,
    catSubGroupsFor,
    programGroupsFor,
    computeThemeLanes,
    buildFiltersThemes,
    appendViewModeToggle,
    renderTags,
    lookupPubImage,
    _gdocParseDateRange: gdocParseDateRange,  // test-only
  };
}());
