# AbTeC Timeline — Feature Wish List

---

## Storybox (event detail drawer)

- Pre-fetch Flickr CDN URLs into Media Thumbnail column (batch noembed script, ~1 req/sec)
  so Flickr images load instantly without the noembed round-trip (tracked as Timeline-013)
- Consider showing current position (e.g. 3 of 47) in navigation scope area

---

## Crosshair Date Line

- Crosshair currently draws on top of events (bars + text); it should sit above row
  backgrounds but below event content

> **Note:** Multiple SVG z-ordering strategies tried (DOM position, insertBefore, mix-blend-mode);
> root cause not yet identified — needs fresh investigation

---

## PDF Export

- Make PDF export work in Safari and Firefox (currently requires Chrome/Brave)

> **Note:** Blocked by browser differences in @page CSS, SVG scaling, and print APIs

---

## Offline Data Loading

- Make double-click `file://` loading work in Firefox and Safari

> **Note:** Currently blocked by stricter local file access policies in those browsers

---

## CV Auto-Update

### What's in place

A GitHub Actions workflow (`.github/workflows/update-cv.yml`) runs every Monday at 06:00 UTC
on the `Timeline-AbTeC-Media` branch. It:

1. Fetches the published Research-Creation Google Doc and rebuilds `cv-data-public.js`
2. Fetches the jasonlewis.org WP media library and rebuilds `pub-images.js`
3. Commits and pushes both files if anything changed

The Funding and Teaching & Service Google Docs are private (unpublished) and are skipped
gracefully. Only Research-Creation data goes into the public build.

### Remaining work — automated server deploy

Currently the updated files must be manually downloaded from GitHub and uploaded via FTP
after each weekly Actions run. Options for automating the final deploy step:

**Option A — GitHub Actions FTP deploy (recommended)**
Add a deploy step to the existing workflow using `SamKirkland/FTP-Deploy-Action`.
After committing the updated files, the action FTPs them directly to the web server.
FTP credentials stored as GitHub repository secrets. Fully hands-off.

**Option B — Server-side git pull**
If the server supports SSH, a cron job on the server can pull from the GitHub repo on a
schedule. Cleaner but requires SSH access and server-side cron.

**Option C — Manual re-upload**
Download the two updated files (`cv-data-public.js`, `pub-images.js`) from GitHub after
each Actions run and FTP them up manually.

### Publication cover images

New publication titles that appear on jasonlewis.org/category/publication/ must be added
manually to `WEBSITE_TITLES` in `fetch_pub_images.py` — the page is JavaScript-rendered
and cannot be scraped statically. New cover images for existing titles are auto-discovered
via the WordPress media REST API.
