...

## Registration of assets

[ The first two are more common for ad hoc... ] If you create IIIF Manifests, each of those has a queue also, that works the same way🆕. You can also POST assets directly into a Manifest.🆕

### Removed from the live "Registration of assets" list (2026-06-24)

POST-to-Space is not implemented: the space `images` collection controller (`API/Features/Image/ImagesController.cs`) has only GET and PATCH, so POST returns 405. The following bullet was removed from the live list of registration methods. **Restore it as the first item when POST-to-Space is implemented:**

```
 - HTTP POST an asset API object into a [Space](../space)
```

At the same time:
- the list intro was changed from "in one of **four** ways" back to "in one of **three** ways" — revert to "four";
- the prose after the list was changed from "The **first two** are more common for ad hoc, one-at-a-time asset registration. The **third** is recommended..." to "The **first** is more common... The **second** is recommended..." — revert the numbering.


As this asset was an image, and default delivery channels will create a IIIF Image API endpoint for an image, the returned asset has an `imageService` property:

THIS NEEDS TO BE REPLACED BY THE `manifest` PROPERTY of asset

### HTTP POST

> This comes after ## HTTP PUT
> NB this isn't supported currently but should be

```
POST /customer/99/spaces/37/images
{
  "id": "my-image.tiff",
  "mediaType": "image/tiff",
  "origin": "https://example.org/images/my-image.tiff"
}
```

This is very similar to the PUT above, expect that:

 - The address POSTed to is the [images](space#images) collection of the Space we want to create the image in
 - We have provided the last path element as the `id` property of the POST body:

 - `id`: the platform will use this for the last part of the asset's public and API URLs. Here it looks like a filename but it can be any string that's a valid URL path element.

Again, the PUT body did not specify any [deliveryChannels](asset#deliveryChannels), and is relying on configured defaults to provide the asset with suitable values for this property. 

See the [delivery channels topic](delivery-channels) for a detailed explanation.


...

> final comment

When POSTing assets into IIIF Manifests, you can supply additional fields that control how the assets are presented in the Manifest. See [IIIF Manifests and Collections](iiif).

---

## The `manifest` (singular) property and its URL pattern (PROV-17, captured 2026-08-03) — **park; feeds SPA-04/SPA-15**

The old page documented a `manifest` (singular) property — a *different* thing from
the new page's `manifests` (Manifests-this-asset-is-used-in). The bare TODO above
("THIS NEEDS TO BE REPLACED BY THE `manifest` PROPERTY") lacked the old semantics
and the worked URL pattern, preserved here:

> `manifest` "links to a document that contains all the outputs the platform is
> providing for the asset" — pattern: `https://dlcs.io/iiif-manifest/{customer}/{space}/{id}`

No `manifest` singular property exists in code (verified 2026-08-03); the
single-asset-manifest endpoint exists but is not surfaced as an asset property.

**Intended direction (PO, 2026-08-03):** ultimately `asset.manifest` (singular) links
to the [single asset manifest](single-asset-manifest), and `asset.manifests` (the
Manifests-this-asset-appears-in array) becomes the less-confusing `asset.scopes`.
Neither exists in code yet — this is the target state for SPA-04/SPA-15 to ratify and
turn into protagonist issues.

