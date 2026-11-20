#!/usr/bin/env bash
# Chạy BÊN TRONG container python:3.12-slim-bullseye (glibc 2.31, Python có libpython dùng chung).
set -euo pipefail
cd /src
apt-get update -qq && apt-get install -y -qq --no-install-recommends binutils >/dev/null
python -m venv /tmp/venv
. /tmp/venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet . "pyinstaller==6.*"
pyinstaller --noconfirm --onefile --clean --name "$NAME" \
  --distpath dist --workpath build-linux --specpath build-linux packaging/entry.py
chown -R "$HOST_UID:$HOST_GID" dist build-linux
