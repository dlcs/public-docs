# tags, roles and id queries not yet implemented

> ⟳ DIS-04 ruled (b) 2026-08-19 (session 4): feature is wanted — protagonist issue
> [#1279](https://github.com/dlcs/protagonist/issues/1279) raised asking for an **RFC**, to be
> put in front of the **portal team** so their search requirements drive the design.
> Prerequisite: #753 (tags/roles stored as comma-delimited text; commas unescaped).
> The examples below are the draft contract for that RFC. The live Aside stays as-is.
> Wire fact (stage, v1.13.2): unknown `q` keys are **silently ignored** — 200 with
> unfiltered results, never an error.

These examples belong in the `### Query object` section once supported:

```
?q={"tags": ["my-tag"]}
?q={"tags": ["my-tag", "another-tag"]}
?q={"roles": ["https://api.dlcs.example/customers/2/roles/clickthrough"]}
?q={"id":"PHOTO.2.22.36.2.tif"}
```

# Ordering — ✅ PROMOTED 2026-08-06 (session 0, DIS-01 ruling): `### Ordering` section restored to asset-queries.mdx with default = `created`. Kept below for the DIS-06 nuance (no field whitelist; unknown field → handled Hydra 500 not 400) which is NOT yet documented — that's DIS-06's call.

You can order by the value of a field of an asset:

```
?orderByDescending=width
?orderBy=height
```

~~If no ordering is provided the order is undefined.~~ **Answered:** default order is
`Created` (`AssetQueryX.GetPropertyName` falls back to "Created"). Note for the docs:
there is no field whitelist — an unknown field name yields a handled Hydra **500**,
not a 400 (DIS-06); matching is case-insensitive. The `p15` sample now has a
`get_images_ordered` example but its docstring still says "Not yet supported" (stale).

# More examples — ⟳ now valid (ordering implemented), restore with DIS-01

```
?q={"string1":"my-value","number1":99}&orderBy=width&pageSize=10&page=12
?string1=my-value&orderByDescending=string3&page=9
```

# Multiple values not yet implemented — ⟳ still true EXCEPT `manifests` (2026-08-03, DIS-03/05)

`manifests` is the one multi-value field that exists today (`?manifests=a,b`
comma-split, or `q` with a string array) — the precedent if this is ever generalised.
For the string1-3 fields below, an array still fails deserialisation → 400
"Could not parse query".

```
?q={"string1":["a","b"]}
```

`string1` can only take one value per asset, therefore this is interpreted as "assets where string1=a OR string1=b".

```
?q={"tags":["a","b"]}
```

`tags` could have both these values in a single asset, but we still treat this as an OR rather than an AND: "assets that have the tag "a" OR the tag "b" OR both. There is currently no syntax for requesting only assets that have BOTH tags.

```
?q={"id":["PHOTO.2.22.36.2.tif","other-image.jp2","my-video"]}
```

`id` is the internal _Model Id_ (see [Identifiers](identifiers)), the last part of the URI. This query returns all assets that match that identifier. If used to filter assets on `/customers/{customer}/allImages`, the returned assets could be in any of the customer's spaces (but never any other customer), so even a single value for `id` could return more than one asset. On `/customers/{customer}/spaces/{space}/images`, each requested `id` value can only return 0 or 1 assets, because this value must be unique within a space.

---

# Roadmap rationale (PROV-06, captured 2026-08-03) — **park (design context)**

Old-doc line explaining why the query surface is expected to grow, dropped with the
caution rewrite:

> "We will need a full set of query features for portal use."

# Applicable endpoints (⟳ 2026-08-03, DIS-22)

The batch endpoints also accept the full query syntax and are missing from the live
page's list: `GET .../queue/batches/{batchId}/images` and `.../batches/{batchId}/assets`
support `?q=`, shortcut params, ordering, paging and `include=adjuncts`.
