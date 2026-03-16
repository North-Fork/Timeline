// orcid-utilities.js — ORCID record parser for Timeline-JEL
// Exports window.ORCIDFormat = { detect, parse, fetchByID }
//
// Handles:
//   - JSON records fetched live from the ORCID public API (v3.0)
//   - JSON files exported from orcid.org (same structure)
//
// ORCID public API endpoint (no auth required for public profiles):
//   https://pub.orcid.org/v3.0/{orcid-id}/record
//   Accept: application/json
//
// Sections parsed: Works, Employment, Education, Funding, Service,
//   Memberships, Distinctions, Invited Positions, Qualifications

(function () {
  'use strict';

  // Maps ORCID work types → timeline group labels
  const WORK_TYPE_GROUP = {
    'journal-article':      'Journal Articles',
    'book':                 'Books',
    'book-chapter':         'Book Chapters',
    'edited-book':          'Books',
    'conference-paper':     'Conference Papers',
    'conference-abstract':  'Conference Papers',
    'conference-poster':    'Conference Papers',
    'report':               'Reports',
    'dissertation':         'Dissertations',
    'preprint':             'Preprints',
    'working-paper':        'Working Papers',
    'magazine-article':     'Press',
    'newsletter-article':   'Press',
    'newspaper-article':    'Press',
    'lecture-speech':       'Lectures',
    'artistic-performance': 'Creative Works',
    'data-set':             'Datasets',
    'software':             'Software',
    'patent':               'Patents',
    'online-resource':      'Online Resources',
    'other':                'Works',
  };

  // ── Date helpers ──────────────────────────────────────────────────────────

  // Converts an ORCID date object { year, month, day } → "MM/DD/YYYY"
  // month and day may be null objects rather than undefined, so coerce carefully
  function fmtDate(d) {
    if (!d) return '';
    const y = d.year?.value;
    if (!y) return '';
    const m   = String((d.month?.value)  || 1).padStart(2, '0');
    const day = String((d.day?.value)    || 1).padStart(2, '0');
    return `${m}/${day}/${y}`;
  }

  // ── Section parsers ───────────────────────────────────────────────────────

  // Parses any affiliation section (employment, education, service, etc.)
  // affiliationGroups is the array at activities-summary.[section].affiliation-group
  function parseAffiliations(affiliationGroups, group) {
    const rows = [];
    for (const ag of affiliationGroups || []) {
      for (const s of ag.summaries || []) {
        // Each summary object has a single key like "employment-summary"
        const summary = Object.values(s)[0];
        if (!summary) continue;

        const start = fmtDate(summary['start-date']);
        if (!start) continue;

        const end  = fmtDate(summary['end-date']);
        const org  = summary.organization?.name || '';
        const role = summary['role-title'] || '';
        const dept = summary['department-name'] || '';

        // Build headline: "Role, Department, Organization" — omit blanks
        const parts = [role, dept, org].filter(Boolean);
        const headline = parts.join(', ');

        rows.push({
          'start date': start,
          'end date':   end || start,
          headline,
          description:  '',
          group,
          project:      '',
        });
      }
    }
    return rows;
  }

  // Parses the works section
  function parseWorks(groups) {
    const rows = [];
    for (const g of groups || []) {
      // ORCID may have multiple sources for a work; use the first (preferred) summary
      const ws = g['work-summary']?.[0];
      if (!ws) continue;

      const title = ws.title?.title?.value || '';
      if (!title) continue;

      const type    = ws.type || 'other';
      const group   = WORK_TYPE_GROUP[type] || 'Works';
      const start   = fmtDate(ws['publication-date']);
      if (!start) continue;

      const journal = ws['journal-title']?.value || '';

      // Prefer DOI URL, then any listed URL
      const doi = ws['external-ids']?.['external-id']
        ?.find(e => e['external-id-type'] === 'doi')?.['external-id-value'];
      const rawUrl  = ws.url?.value || '';
      const linkUrl = doi ? `https://doi.org/${doi}` : rawUrl;

      // Embed link in headline if available
      const headline = linkUrl ? `<a href="${linkUrl}">${title}</a>` : title;

      rows.push({
        'start date': start,
        'end date':   start,
        headline,
        description:  journal,
        group,
        project:      '',
      });
    }
    return rows;
  }

  // Parses the funding section
  function parseFundings(groups) {
    const rows = [];
    for (const g of groups || []) {
      const fs = g['funding-summary']?.[0];
      if (!fs) continue;

      const title = fs.title?.title?.value || '';
      const org   = fs.organization?.name  || '';
      const start = fmtDate(fs['start-date']);
      const end   = fmtDate(fs['end-date']);
      if (!start) continue;

      rows.push({
        'start date': start,
        'end date':   end || start,
        headline:     title,
        description:  org,
        group:        'Funding',
        project:      '',
      });
    }
    return rows;
  }

  // ── Public API ────────────────────────────────────────────────────────────

  // Returns true if data looks like an ORCID JSON record
  function detect(data) {
    return !!(data && (data['orcid-identifier'] || data['activities-summary']));
  }

  // Converts a full ORCID record object → array of timeline row objects
  function parse(data) {
    const acts = data['activities-summary'] || {};
    const rows = [];

    rows.push(...parseAffiliations(acts.employments?.['affiliation-group'],        'Employment'));
    rows.push(...parseAffiliations(acts.educations?.['affiliation-group'],         'Education'));
    rows.push(...parseAffiliations(acts.qualifications?.['affiliation-group'],     'Education'));
    rows.push(...parseFundings(acts.fundings?.group));
    rows.push(...parseWorks(acts.works?.group));
    rows.push(...parseAffiliations(acts.services?.['affiliation-group'],           'Service'));
    rows.push(...parseAffiliations(acts.memberships?.['affiliation-group'],        'Memberships'));
    rows.push(...parseAffiliations(acts.distinctions?.['affiliation-group'],       'Distinctions'));
    rows.push(...parseAffiliations(acts['invited-positions']?.['affiliation-group'], 'Invited Positions'));

    // Sort chronologically
    rows.sort((a, b) => {
      const da = new Date(a['start date']);
      const db = new Date(b['start date']);
      return da - db;
    });

    return rows;
  }

  // Fetches a public ORCID record by iD and returns parsed rows
  // orcidId may be a bare iD ("0000-0001-5000-0007") or a full URL
  async function fetchByID(orcidId) {
    const clean = orcidId.trim().replace(/^https?:\/\/orcid\.org\//, '');
    if (!/^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$/.test(clean))
      throw new Error('Invalid ORCID iD format — expected 0000-0001-5000-0007');

    const url = `https://pub.orcid.org/v3.0/${clean}/record`;
    const res = await fetch(url, { headers: { Accept: 'application/json' } });
    if (!res.ok) throw new Error(`ORCID API returned HTTP ${res.status}`);

    const data = await res.json();
    return parse(data);
  }

  window.ORCIDFormat = { detect, parse, fetchByID };
})();
