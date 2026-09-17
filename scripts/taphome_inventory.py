#!/usr/bin/env python3
"""Export a TapHome API discovery snapshot and a best-effort CSV inventory.

Required environment variables (unless supplied as arguments):
  TAPHOME_API_URL  e.g. http://192.168.1.50/api/cloudapi/v1
  TAPHOME_TOKEN    TapHome API token

The script deliberately avoids third-party Python dependencies.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def api_get(base_url: str, token: str, endpoint: str) -> Any:
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"TapHome {token}",
            "Accept": "application/json",
            "User-Agent": "taphome-home-assistant-guide/1.0",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return json.loads(response.read().decode(charset))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {body[:500]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Unable to reach {url}: {exc.reason}") from exc


def find_device_list(payload: Any) -> list[dict[str, Any]]:
    """Find the most likely device list without assuming one API wrapper shape."""
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]

    if isinstance(payload, dict):
        for key in ("devices", "data", "result"):
            candidate = payload.get(key)
            if isinstance(candidate, list):
                return [x for x in candidate if isinstance(x, dict)]

        # Some API responses can be a single device object.
        if "deviceId" in payload:
            return [payload]

    return []


def supported_values_text(device: dict[str, Any]) -> str:
    raw = (
        device.get("supportedValues")
        or device.get("supported_values")
        or device.get("values")
        or []
    )
    if not isinstance(raw, list):
        return ""

    parts: list[str] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        value_id = item.get("valueTypeId", item.get("id", ""))
        value_name = item.get("valueTypeName", item.get("name", ""))
        if value_id != "" and value_name:
            parts.append(f"{value_id}:{value_name}")
        elif value_name:
            parts.append(str(value_name))
        elif value_id != "":
            parts.append(str(value_id))
    return "; ".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export TapHome discovery and current values to JSON + CSV."
    )
    parser.add_argument(
        "--api-url",
        default=os.getenv("TAPHOME_API_URL"),
        help="TapHome API base URL (or set TAPHOME_API_URL)",
    )
    parser.add_argument(
        "--token",
        default=os.getenv("TAPHOME_TOKEN"),
        help="TapHome API token (or set TAPHOME_TOKEN)",
    )
    parser.add_argument(
        "--out-dir",
        default="inventory",
        help="Output directory (default: inventory)",
    )
    args = parser.parse_args()

    if not args.api_url:
        parser.error("--api-url or TAPHOME_API_URL is required")
    if not args.token:
        parser.error("--token or TAPHOME_TOKEN is required")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    discovery = api_get(args.api_url, args.token, "discovery")
    all_values = api_get(args.api_url, args.token, "getAllDevicesValues")

    (out_dir / "discovery.json").write_text(
        json.dumps(discovery, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (out_dir / "all_values.json").write_text(
        json.dumps(all_values, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    devices = find_device_list(discovery)
    fieldnames = [
        "device_id",
        "name",
        "description",
        "type",
        "usage",
        "zone",
        "category",
        "supported_values",
    ]

    with (out_dir / "devices.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for device in devices:
            writer.writerow(
                {
                    "device_id": device.get("deviceId", ""),
                    "name": device.get("name", ""),
                    "description": device.get("description", ""),
                    "type": device.get("type", ""),
                    "usage": device.get("usage", ""),
                    "zone": device.get("zone", ""),
                    "category": device.get("category", ""),
                    "supported_values": supported_values_text(device),
                }
            )

    print(f"Saved raw discovery: {out_dir / 'discovery.json'}")
    print(f"Saved current values: {out_dir / 'all_values.json'}")
    print(f"Saved CSV inventory:  {out_dir / 'devices.csv'}")
    print(f"Discovered devices:   {len(devices)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
