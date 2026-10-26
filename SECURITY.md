# Security and privacy

Gram Studio is a single static page. There is no server, account, database or analytics. Everything below is designed so that your photos and projects can only ever be seen by you, on your own device.

## What the app does with your data

- Photos are read by the browser and drawn on a canvas. They are never uploaded. The release build makes **no network requests at all**: the Content Security Policy forbids them, and the only external library (JSZip) is inlined and hash-verified at build time.
- Projects, including the photo files, are stored in the browser's IndexedDB for this site's origin. They are visible to nobody else, not even other websites. "About" in the app shows the storage used and offers one-click deletion.
- Exports are rendered fresh, so they carry no EXIF metadata (no location, camera or date).
- On phones the export can be handed to the system share sheet; what happens next is under the operating system's control, exactly like sharing any photo.

## Protections in the code

- Every string that comes from a user (file names, project names, captions) is escaped before it enters HTML, and nothing in the page is driven by the URL.
- Everything read from storage or from an imported project file is rebuilt from defaults with type checks and clamped ranges. Unknown fields are dropped; photo entries are limited in number, size and path.
- Only raster image types are accepted (JPEG, PNG, WebP, GIF, HEIC, AVIF, BMP, TIFF). SVG is refused because it can carry scripts.
- The hosted build ships a strict Content Security Policy (`default-src 'none'`, hashed inline scripts, no eval, no external origins) and a frame guard against clickjacking.
- `scripts/security_check.py` runs in CI on every push and fails the build if a network call, dynamic code, an external resource or an unescaped insertion is ever introduced.

## What it cannot protect against

- Anyone who can unlock your phone or computer can open the app and see your projects, like any local app.
- Browser extensions you install run with access to every page, including this one.
- A copy of the app hosted by someone else could be modified. Use the official address or build it yourself from source.

## Reporting a problem

Open an issue on GitHub, or email the address on the author's profile. Please do not include photos or personal data in reports.
