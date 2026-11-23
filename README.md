# Komodo & Ko — Terms & Conditions Signing Pages

Three standalone, mobile-friendly pages that let a guest read the trip Terms & Conditions,
fill in a short reservation form, draw their signature, and download a signed PDF copy —
all from one link you send them.

## Files

```
index.html            -> hub page linking to the 3 trip types
full-day-trip.html     -> Full Day Trip Komodo Island T&C + signing
open-trip.html          -> Open Trip Komodo Island T&C + signing
private-trip.html       -> Private Trip Komodo Island T&C + signing
assets/
  style.css             -> all styling (green & cream luxury palette, matched to the logo)
  app.js                -> signature pad, full-form validation, PDF export logic
  logo.jpg               -> Komodo & Ko logo (cover page + company signature block)
  company-signature.png -> Komodo & Ko authorized signature (right side)
  signature_pad.umd.min.js
  jspdf.umd.min.js
  html2canvas.min.js
generate.py             -> source script that generated the 3 HTML pages
                            (only needed if you want to edit the legal text later)
```

## How it works

1. You send the guest a link, e.g. `https://yoursubdomain.com/full-day-trip.html`.
2. The guest reads the terms (English first, Indonesian translation in its own
   paragraph underneath — never joined with a slash), fills in **every field** of
   the Reservation Form, ticks the agreement box, and signs on the left-hand canvas
   with mouse or finger, writing their name on the line beneath their signature.
3. The Komodo & Ko signature on the right is already in place (your logo + your
   scanned signature), since your side doesn't sign live.
4. The "Sign & Download PDF" button stays disabled until the entire reservation
   form, the checkbox, and the guest's signature + name are all filled in — if the
   guest clicks it early, the missing fields are outlined in red and listed in the
   status message. Once everything is complete, clicking it captures the whole
   filled-in page (terms + form + both signatures) into a multi-page A4 PDF and
   downloads it straight to the guest's device.
5. The guest sends you that PDF back, and you forward it to the operator.

Everything runs in the guest's browser — no server, database or backend is required.
`generate.py` requires nothing; the published HTML/CSS/JS files are all you need to host.

## Logo &amp; signature

Your logo (`assets/logo.jpg`) and signature (`assets/company-signature.png`) are already
wired in — the logo appears on the cover of all 3 pages and, paired with your signature,
in the Komodo & Ko signature box. To update either later, just replace the file with the
same filename and re-open the pages (no need to re-run `generate.py` for this).

## Hosting on your subdomain

These are plain static files — upload the whole folder (keeping the `assets/`
subfolder alongside the HTML files) to any static host or your subdomain's web root:

- Netlify / Vercel: drag-and-drop the folder, or connect a Git repo.
- Any cPanel / shared hosting: upload via FTP into the subdomain's `public_html`.
- Cloudflare Pages, GitHub Pages, S3 + CloudFront — all work the same way.

Once live at your subdomain (e.g. `terms.komodoandko.com`), send guests the direct
link to the relevant trip page:

```
https://terms.komodoandko.com/full-day-trip.html
https://terms.komodoandko.com/open-trip.html
https://terms.komodoandko.com/private-trip.html
```

or send `index.html` if you'd like them to pick the trip type themselves.

## Editing the legal text later

The wording on all 3 pages was transcribed from your original PDFs with
"Komodo Luxury" replaced by "Komodo & Ko" (the only brand reference that appeared
in the source documents). If you need to change any clause later, edit the
relevant content block inside `generate.py` and re-run:

```powershell
python generate.py
```

This regenerates all three HTML files from the shared template, so styling and
the signing logic stay consistent across all three pages.

## Testing locally

From this folder, run a simple local server and open it in a browser
(opening the HTML file directly with a double-click also works for viewing,
but some browsers block canvas/PDF features on `file://` pages — a local
server avoids that):

```powershell
python -m http.server 8080
```

Then visit `http://localhost:8080/index.html`.
