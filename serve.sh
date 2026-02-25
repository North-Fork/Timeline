#!/bin/bash
cd "$(dirname "$0")"
echo "Starting timeline server at http://localhost:8000/timeline.html"
open "http://localhost:8000/timeline.html"
python3 -m http.server 8000
