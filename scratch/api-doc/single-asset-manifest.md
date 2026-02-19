# Examples section - all code blocks empty in original

The original page had an Examples section with six headings but no JSON content in any of them. Restore once real IIIF JSON examples can be added.

## Examples

### Audio with one transcode derivative

### Video with two transcode derivatives and two adjuncts

### Image with image service and thumbnail

### Image with image service, thumbnail and file outputs, and three adjuncts

### Word document on file channel with one adjunct

### Image with no delivery channels

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