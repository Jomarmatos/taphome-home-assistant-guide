# GitHub repository setup

Recommended repository settings for:

`https://github.com/Jomarmatos/taphome-home-assistant-guide`

## Repository metadata

**Name**

```text
taphome-home-assistant-guide
```

**Description**

```text
Practical guide and tools for integrating TapHome with Home Assistant using the TapHome API and the community taphome-homeassistant integration.
```

**Visibility**

```text
Public
```

**Website**

Use the repository URL initially. GitHub Pages can be added later if desired.

**Topics**

```text
taphome
home-assistant
home-automation
smart-home
hacs
taphome-api
python
yaml
```

## Recommended features

- Issues: enabled
- Pull requests: enabled
- Discussions: optional
- Wiki: disabled initially (keep documentation in the repository)
- Secret scanning / push protection: enable when available for the account/repository
- Dependabot: not necessary for the current standard-library-only scripts

## Publishing with GitHub CLI

From the directory containing this repository:

```bash
git init
git add .
git commit -m "Initial TapHome + Home Assistant integration guide"
git branch -M main

gh repo create Jomarmatos/taphome-home-assistant-guide \
  --public \
  --source=. \
  --remote=origin \
  --description "Practical guide and tools for integrating TapHome with Home Assistant using the TapHome API and the community taphome-homeassistant integration." \
  --push

gh repo edit Jomarmatos/taphome-home-assistant-guide \
  --add-topic taphome \
  --add-topic home-assistant \
  --add-topic home-automation \
  --add-topic smart-home \
  --add-topic hacs \
  --add-topic taphome-api \
  --add-topic python \
  --add-topic yaml
```

Then create a release `v1.0.0` and attach the PDF from `docs/` if you want a stable downloadable release asset.
