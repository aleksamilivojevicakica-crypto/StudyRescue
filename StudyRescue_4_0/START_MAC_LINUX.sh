#!/bin/sh
cd "$(dirname "$0")" || exit 1
if command -v python3 >/dev/null 2>&1; then
  echo 'Open http://127.0.0.1:8000/ in your browser.'
  python3 server.py
else
  echo 'Python 3.10 or later is needed.'
  exit 1
fi
