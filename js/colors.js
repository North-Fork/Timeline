// ── Shared color palette ────────────────────────────────────────────────
// Central place for every color re-used across the JS files (timeline
// canvas, print/export SVG, status messages, etc). Change a value here
// and it updates everywhere that color is used.
// Note: this is separate from the PALETTE array in config.js, which is
// the per-category event-color rotation, not repeated UI chrome.
const COLORS = {
  bgDark:      '#111827',  // main dark background (canvas, print background)
  panelBg:     '#1f2937',  // header / row-label panel background
  stripeDark:  '#161d2b',  // darker alternating row stripe
  stripeLight: '#1a2030',  // lighter alternating row stripe / fine gridlines
  border:      '#374151',  // panel borders, dividers, default gridlines/ticks
  textDim:     '#4b5563',  // dim label text
  textMuted:   '#6b7280',  // muted text, month-axis mid ticks
  textSubtle:  '#9ca3af',  // subtle text, month-axis year ticks
  textLight:   '#d1d5db',  // light label text
  white:       '#ffffff',  // white text / strokes
  accent:      '#6366f1',  // primary accent (links, buttons, highlights)
  watermark:   '#d97706',  // past/future watermark text
  success:     '#22c55e',  // success status text
  error:       '#ef4444',  // error status text
};
