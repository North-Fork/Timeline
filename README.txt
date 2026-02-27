AbTeC Timeline
==============

USE
Timeline Expand/Contract or Zoom In/Out: spacebar+mousewheel

PDF Export still requires alot of work.

RECOMMENDED: Chrome or Brave browser
--------------------------------------
Double-click timeline.html to open. The timeline data loads automatically.

If the data does not appear, the pre-generated data file may be out of date.
See "Keeping data current" below.


ALL OTHER BROWSERS (Firefox, Safari, etc.)
-------------------------------------------
Browsers other than Chrome/Brave block local file access, so the data
cannot load via double-click. Instead:

  1. Open a terminal and navigate to this folder:
       cd /path/to/Timeline

  2. Start a local server:
       python3 -m http.server 8000

  3. Paste this into your browser's URL bar:
       http://localhost:8000/timeline.html


LOADING A DIFFERENT DATA FILE
------------------------------
Drag any .xlsx file onto the drop zone in the sidebar to load it.


KEEPING DATA CURRENT
---------------------
When IIF-Timeline-Data-Multi-Project.xlsx is updated, regenerate the
pre-built data file by running:

    python3 data/timeline-data/make_data_js.py

This requires Python 3 and the openpyxl library:
    pip3 install openpyxl
