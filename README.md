# Theme documentation home

Source for <https://themedocs.github.io/> — the front door that points at each
theme's documentation.

Every theme's docs live in their own repository and are published at
`/<slug>/`, so this site is a single page plus a 404:

| theme | repo | published at |
| --- | --- | --- |
| Fox | `themedocs/fox` | <https://themedocs.github.io/fox/> |
| Dine | `themedocs/dine` | <https://themedocs.github.io/dine/> |
| Simple & Elegant | `themedocs/simple-elegant` | <https://themedocs.github.io/simple-elegant/> |
| Blank | `themedocs/blank` | <https://themedocs.github.io/blank/> |
| Stoat | `themedocs/stoat` | <https://themedocs.github.io/stoat/> |

## Adding a theme

Add a `[[theme]]` block to `themes.toml`, rebuild, and commit. Create the
matching repository separately and enable Pages on its `docs/` folder.

## Building

```bash
python3 -m venv venv && venv/bin/pip install markdown   # first time
venv/bin/python build.py                                # -> docs/
```

Commit `docs/` along with the source — that folder is what Pages publishes.
