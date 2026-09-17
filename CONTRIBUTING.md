# Contributing

Contributions that improve clarity, portability, or troubleshooting are welcome.

## Before opening an issue

1. Confirm the TapHome device works in the TapHome app.
2. Test the TapHome API directly with `/discovery` and, when relevant, `/getDeviceValue/<id>`.
3. Check Home Assistant logs for `taphome`, `ValueError`, and `Error while setting up`.
4. Remove all private tokens, public IP addresses, customer details, and unrelated device data from logs/screenshots.
5. Confirm the behavior against the current upstream integration: <https://github.com/martindybal/taphome-homeassistant>.

## Pull requests

Keep examples generic. Do not add customer/site-specific IP addresses, credentials, internal project names, or personal data.

When changing scripts, run:

```bash
python3 -m py_compile scripts/taphome_inventory.py
bash -n scripts/taphome_api_probe.sh
```

Documentation changes should reference primary sources whenever possible.
