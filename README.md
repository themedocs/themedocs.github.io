# Theme documentation home

Source for <https://themedocs.github.io/> — which no longer hosts anything. It
is a 301 to the two storefronts that took the manuals over in September 2026.

## How the 301 works

GitHub Pages cannot serve a 301 from a file; a `<meta http-equiv=refresh>` page
is a 200, and a crawler keeps the old URL. The one 301 Pages does emit is the
custom-domain redirect, so `docs/CNAME` here carries `themedocs.heronwp.com`.
Because this is the *user*-site repo, that covers every project repo on the
account too — `themedocs.github.io/fox/getting-started/` 301s to
`themedocs.heronwp.com/fox/getting-started/`, whole path kept. None of the
theme repos carry a CNAME of their own; a custom domain belongs to one Pages
site at a time.

`themedocs.heronwp.com` is a Cloudflare Pages project holding a single
`_redirects` file, which 301s each product onto the storefront that sells it —
fox / dine / simple-elegant / blank to `heronwp.com/docs/`, stoat / rural-blog
/ evermag to `owldraft.com/docs/`, fox-templates to `fox-templates.heronwp.com`.
Source lives in the company repo at `cf/themedocs-hop/`.

Two 301s, both keeping the path. `build.py` rewrites `docs/CNAME` on every run
because it empties `docs/` first — do not delete it.

Historically every theme's docs lived in their own repository, published at
`/<slug>/`. Those repos still exist and still build; nothing is served from
them any more:

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
