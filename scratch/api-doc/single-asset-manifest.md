# Examples section

Added all six examples based on the documentation and observed image service URL patterns
from real platform output. The image service and thumbnail URL patterns are confirmed correct
(`iiif-img/v2/{customer}/{space}/{asset}` for ImageService2, `iiif-img/{customer}/{space}/{asset}`
for ImageService3, etc.). The AV and file delivery URL patterns are illustrative — verify
against real AV and file-channel assets when the platform is available.

# Manifest URL and asset.manifest

The asset doesn't yet expose a link to the single asset manifest:

```
"manifest": "https://dlcs.io/iiif-manifest/2/5/b2921371x_0001.jp2"
```

```
https://dlcs.example/iiif-manifest/{customer}/{space}/{assetId}
```

# Note on iiif-av Choice resource

Line 17 of the original had `(?)` after the note that the iiif-av painting annotation body is "always a Choice resource, even if there is only one output". This was an open question from the original author — confirm whether this is intentional.

# Source reference

The behaviour for file-only assets (placeholder image, `placeholder` and `original` behaviors) was sourced from https://github.com/wellcomecollection/docs/pull/77


# dlcs:channelOutputs

removed from copy:

In addition to the above, the single asset manifest has an extension property `dlcs:channelOutputs`: an array of content resources and services, one per delivery channel output, each including the channel it belongs to. This is more consistent in structure than the regular manifest properties and can be used for quick programmatic access to channel outputs.