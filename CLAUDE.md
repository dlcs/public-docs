
This is a platform documentation website.

Read the pages under the /usage path, starting at https://dlcs.github.io/public-docs/usage/concepts/ for an overview of what the platform does.

At the moment we are in the process of gradually moving the API documentation pages to this new site, from an older version at https://deploy-preview-2--dlcs-docs.netlify.app/api-doc/overview (the source code for these pages is the wip-skeleton branch at https://github.com/dlcs/docs/tree/wip-skeleton/pages/api-doc, which is locally at C:\git\dlcs\docs\pages\api-doc). The old version uses the Nextra framework (https://nextra.site/), the new version uses Starlight (https://starlight.astro.build/).

# Python sample code

In the new site, each page of API documentation under C:\git\dlcs\public-docs\src\src\content\docs\api-doc\ will be accompanied by some sample code, stored in the C:\git\dlcs\public-docs\dlcs-docs-client directory and linked from the documentation markdown pages using a LinkCard component (for an example see C:\git\dlcs\public-docs\src\src\content\docs\api-doc\overview.mdx).

Analyse how the code here works and how it uses a very simple set of helper functions. The aim of this sample code is to be as clear as possible, focusing on the HTTP operations. It doesn't have async code, error handling or other features you would expect in a production-ready client library because its aim is to show the API as concisely as possible.

# Older documentation is not accurate

Rather than just copy across all the mdx files from C:\git\dlcs\docs\pages\api-doc and adapting them to the new site framework, I am copying one section of a page at a time and rewriting some as I go, because the older documentation sometimes describes features that are not yet implemented. In moving the documentation to the new site, I want to ensure that everything in the documentation is accurate and works. Important concepts will be accompanied by a Python code sample as described. When I want to save some text that describes a feature that is not yet implmented, I copy it to a file in C:\git\dlcs\public-docs\scratch\api-doc - there is a .md file here for each mdx file in the C:\git\dlcs\public-docs\src\src\content\docs\api-doc folder. The contents of these "scratch" markdown files are really to act as notes for when the feature does become implemented.

# Help port the code

You will help me do this by helping me move documentation code over one section of a page at a time. I will ask you to write the Python code samples one by one as directed, and running them to see if they do as intended. This includes using the astro framework features like LinkCard instead of Nextra. Don't make any changes until asked and then proceed slowly as instructed.

Only do one ## markdown section at a time, always stop and wait for further instructions after each section as we port it.

# Current porting progress

All 16 api-doc pages below have been ported and have accompanying Python code samples. They are in good shape. The next pages to work on are those linked from existing pages but not yet created (see "Pages not yet ported" below).

| sidebar order | page file | code sample dir | notes |
|:---|:---|:---|:---|
| 1 | overview.mdx | p01_overview/ | |
| 2 | registering-assets.mdx | p02_registering/ | |
| 3 | collections.mdx | (none needed) | |
| 4 | entrypoint.mdx | p04_entrypoint/ | |
| 5 | customer.mdx | p05_customer/ | |
| 6 | space.mdx | p06_space/ | |
| 7 | asset.mdx | p07_asset/ | |
| 8 | queues.mdx | p08_queue/ | |
| 9 | batch.mdx | p09_batch/ | |
| 10 | (pipelines — skipped for now) | | scratch notes at scratch/api-doc/pipelines.md |
| 11 | delivery-channels.mdx | p11_delivery_channels/ | |
| 12 | origin-strategy.mdx | p12_origin_strategies/ | |
| 13 | adjuncts.mdx | p13_adjuncts/ | |
| 15 | asset-queries.mdx | p15_asset_queries/ | |
| 16 | identifiers.mdx | (none needed) | written from scratch, not ported |
| 17 | named-queries.mdx | p16_named_queries/ | note: code dir is p16, not p17 |
| 18 | single-asset-manifest.mdx | p17_single_asset_manifest/ | note: code dir is p17, not p18 |

## Pages not yet ported (linked from existing pages, will 404 until created)

- `iiif.mdx` — IIIF Manifests and Collections
- `pipelines.mdx` — order 10 (scratch notes exist)
- `storage.mdx`
- `custom-headers.mdx`
- `roles.mdx`
- `auth-service.mdx`
- `access-control.mdx`
- `size-restrictions.mdx`

# Established conventions

## Starlight internal links

All internal links between pages in this Starlight site **must use `../` prefix** for sibling pages, e.g. `[Space](../space)` not `[Space](space)`. This is because Starlight serves pages with a trailing slash (e.g. `/api-doc/asset/`), so a bare relative link like `space` resolves to `/api-doc/asset/space` instead of `/api-doc/space`. Same-page anchor links (`[foo](#bar)`) do not need the prefix.

## Starlight components

Use these from `@astrojs/starlight/components`:
- `LinkCard` — to link to a Python code sample on GitHub. Always use the emoji 💻 in the title.
- `Aside` — replaces Nextra `Callout`. Types: `note`, `caution`, `danger`.
- `Card` — used on overview page only.

## Python code sample conventions

- Samples live in `dlcs-docs-client/p{N}_{page-name}/` numbered by sidebar order of the linked page.
- Each sample imports from `iiif_cs.py` (the helper module in `dlcs-docs-client/`) and `settings.py`.
- Key helpers: `get_cloud_services_resource(path)`, `post_resource(path, body)`, `put_resource(path, body)`, `patch_resource(path, body)`, `delete_resource(path)`, `pprint(obj)`, `wait_for_value(path, field, value, interval, retries)`, `BASIC_AUTH_HEADER`, `normalise_path(path)`.
- `settings.docs_space_id` is the space used for documentation examples.
- Public host (for IIIF-facing URLs, not the API) is derived as: `settings.IIIF_CS_API_HOST.replace("//api.", "//", 1)`.
- Code is intentionally simple: no async, no error handling, no retries — clarity over robustness.
- The LinkCard `href` points to the GitHub raw URL: `https://github.com/dlcs/public-docs/blob/main/dlcs-docs-client/{dir}/{file}.py`

## Resource conventions

- Most resources use `id` as their model identifier; exceptions: `DeliveryChannelPolicy` and `NamedQuery` use `name` as the path element instead. This inconsistency is documented in `identifiers.mdx`.
- Domain/range tables follow this format in every property section:

```
| domain | range | readonly | writeonly |
|:---|:---|:---|:---|
| vocab:Type | xsd:type | True/False | True/False |
```

## Scratch files

`scratch/api-doc/{pagename}.md` holds text from the old docs that describes features not yet implemented, plus notes about open questions. These are not published — they're reference for when the feature lands.
