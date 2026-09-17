#!/usr/bin/env bash
set -euo pipefail

: "${TAPHOME_API_URL:?Set TAPHOME_API_URL, e.g. http://192.168.1.50/api/cloudapi/v1}"
: "${TAPHOME_TOKEN:?Set TAPHOME_TOKEN to a valid TapHome API token}"

BASE="${TAPHOME_API_URL%/}"
AUTH="Authorization: TapHome ${TAPHOME_TOKEN}"

pretty() {
  python3 -m json.tool 2>/dev/null || cat
}

get() {
  local path="$1"
  echo
  echo "### GET ${path}"
  curl --fail --silent --show-error \
    -H "$AUTH" \
    -H "Accept: application/json" \
    "$BASE/$path" | pretty
}

get "location"
get "discovery"
get "getAllDevicesValues"

if [[ -n "${DEVICE_ID:-}" ]]; then
  get "getDeviceValue/${DEVICE_ID}"
else
  echo
  echo "Tip: set DEVICE_ID=<id> to also query getDeviceValue/<id>."
fi
