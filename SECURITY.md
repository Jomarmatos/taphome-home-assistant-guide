# Security

## Never publish a TapHome API token

Treat the TapHome API token as a secret credential.

Do not place a real token in:

- `configuration.yaml`
- screenshots
- issue reports
- shell history copied into issues
- `devices.csv` notes
- Git commits

Store the Home Assistant token reference in `secrets.yaml` and keep the real value out of version control.

For command-line testing, prefer temporary environment variables:

```bash
export TAPHOME_API_URL="http://192.168.1.50/api/cloudapi/v1"
export TAPHOME_TOKEN="replace-with-your-token"
```

Unset the token when finished:

```bash
unset TAPHOME_TOKEN
```

If a token is accidentally published, revoke/replace it in the TapHome app and remove it from the Git history. Assume a published token has been compromised even if the repository was public only briefly.

## Network exposure

Prefer LAN or VPN access to the TapHome Core. Do not expose the local TapHome API directly to the public Internet merely to make Home Assistant work remotely.

## Reporting repository issues

This repository documents a third-party integration. Security issues in TapHome products, Home Assistant, HACS, or the upstream `taphome-homeassistant` integration should be reported to the respective maintainers through their official channels.
