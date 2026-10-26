# Gram Studio

A layout tool for Instagram: seamless carousels, profile-grid splits, collages, captions and a phone preview. One HTML file, no server, no accounts. Photos never leave the browser.

## Features

- **Carousel** – split one wide photo into slides that line up edge to edge. Styles: Seamless, Peek-through (a matte window over a continuous photo) and Zoom-in (each slide a tighter crop). Optional cover and end slides, matte frames.
- **Grid** – cut a photo into 4:5 or 1:1 tiles that reassemble on a profile, numbered in posting order.
- **Collage** – 16 layouts, fit or fill per cell, edge masks (torn paper, instant-print frame, 35mm film, arch), tilt, looks.
- **Text** – layers with presets, fonts, outline, shadow, backdrops, snapping; captions can run across slides.
- **Phone preview** – feed post with swipe, profile grid, or story view.
- **Projects** – autosaved in the browser (IndexedDB), export and import as a `.gramstudio.zip` for backups or another device, undo/redo, light and dark themes, JPEG or PNG export.
- **Installable** – the hosted build is a PWA: add it to a phone's home screen and it works offline.

## Run it

Open `docs/index.html` in a modern browser (Chrome, Edge, Safari 17+, Firefox). Everything is local. On a phone, open a hosted copy in the browser and add it to the home screen. The preview fills the screen and a bottom bar (Photos, Edit, Text, Export, Preview) opens a sliding sheet with just those controls; pull the handle up for a taller sheet or down to dismiss it. Pinch zooms a crop or a collage cell, and exports go to the share sheet or Files. Looks (filters) need Safari 18 or Chrome; older Safari previews and exports without them.

## Host it

`docs/index.html` is self-contained. Put it on any static host (GitHub Pages, Netlify, Cloudflare Pages, an S3 bucket). No build step is needed at deploy time, no backend, no environment variables.

**GitHub Pages:** push this repository, then in the repository settings open *Pages*, choose *Deploy from a branch*, pick `main` and the `/docs` folder, and save. The site appears at `https://<your-user>.github.io/<repo>/` within a minute or two. Re-run `python3 build.py` and commit `docs/index.html` whenever you change the source.

Recommended response headers if your host lets you set them (the file already ships an equivalent Content Security Policy as a meta tag):

```
Content-Security-Policy: default-src 'none'; script-src 'sha256-…' (see docs/index.html); style-src 'unsafe-inline'; img-src 'self' blob: data:; connect-src 'self'; manifest-src 'self'; worker-src 'self'; base-uri 'none'; form-action 'none'; object-src 'none'; frame-ancestors 'none'
X-Content-Type-Options: nosniff
Referrer-Policy: no-referrer
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

## Build

`gram-studio.html` is the source; it loads JSZip from cdnjs with Subresource Integrity. `build.py` inlines the pinned copy from `vendor/`, verifies its hash, computes the inline-script hashes, writes `docs/index.html` with the strict CSP, and copies the PWA files from `pwa/` (manifest, icons, service worker) with a per-build cache stamp.

```bash
python3 build.py
```

Bump `VERSION` in the source when you release.

## Privacy and security notes

- No network requests are made by the app itself. The source file fetches one script from cdnjs (with SRI); the release build makes none.
- Projects, including photo files, are stored in the browser's IndexedDB for that origin only. "About" in the app shows storage use and offers a one-click delete of all data.
- All user-supplied strings (file names, project names, captions) are escaped before entering HTML.
- Everything read from storage or an imported project file is rebuilt from defaults with type checks and clamped ranges; unknown fields are dropped. Imported zips are limited to 80 photos of up to 80 MB each, with file paths restricted to a `photos/` folder.
- Photos larger than 3600 px on the long edge are downscaled in memory on import (the original file is still stored and exported), which keeps phones from running out of memory.
- Exports are rendered fresh on a canvas and carry no EXIF metadata.
- Images are decoded by the browser only; the app accepts image MIME types up to 80 MB, up to 80 photos per project.
- Not affiliated with Instagram or Meta. The phone preview uses generic icons.

## License

MIT. JSZip is © Stuart Knightley, MIT/GPLv3 dual licensed.
