# DLCS Public Docs

This is the public documentation site for **IIIF Cloud Services (IIIF-CS)**, a platform by Digirati/DLCS that implements IIIF and related services. The repo has two main parts:

- **`src/`** — Astro + Starlight documentation website, deployed to GitHub Pages at `https://dlcs.github.io/public-docs`
- **`dlcs-docs-client/`** — Python code samples that accompany the API documentation pages
- **`scratch/`** — Draft markdown content not yet published to the site

## Site Development (Astro/Starlight)

All commands run from the `src/` directory:

```bash
cd src
npm install        # install dependencies
npm run dev        # dev server at localhost:4321
npm run build      # build to ./dist/
npm run preview    # preview production build
```

Locally the root is [http://localhost:4321/public-docs](http://localhost:4321/public-docs).

Deployment is automatic via GitHub Actions on push to `main`.

## Documentation Content

Content lives in `src/src/content/docs/` as `.mdx` files, organized into three sidebar sections (configured in `src/astro.config.mjs`):

- `usage/` — Conceptual guides (access control, collections, IIIF images/manifests, etc.)
- `portal/` — How to use the web UI without writing code
- `api-doc/` — Full API reference (assets, spaces, queues, batches, delivery channels, etc.)

Starlight auto-generates the sidebar from the directory structure. Route paths match file names relative to `docs/`. Static assets used in docs (sample images, fixture files) go in `src/public/doc_fixtures/`.

## Python Code Samples

The `dlcs-docs-client/` scripts are runnable examples that mirror the API documentation. Each `pNN_topic/` directory corresponds to a documentation section.

Setup:
```bash
cd dlcs-docs-client
cp example.env .env   # fill in your credentials
pip install -r requirements.txt
python p01_overview/overview.py
```

Required `.env` variables: `IIIF_CS_API_HOST`, `IIIF_CS_PRESENTATION_HOST`, `IIIF_CS_CUSTOMER_ID`, `IIIF_CS_CUSTOMER_NAME`, `IIIF_CS_BASIC_CREDENTIALS` (format: `key:secret`).

The shared `settings.py` loads these and defines fixed space IDs used across samples. `iiif_cs.py` contains shared HTTP helpers.
