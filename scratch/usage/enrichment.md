
## Adjuncts providing text for search

If an adjunct is in a text format understood by the platform, it can be used to generate IIIF Search services. Formats include plain text, METS-ALTO, hOCR and W3C TextualBody annotations.

Currently these services would sit outside the platform, but in a future version, the platform will generate search services from text-bearing adjuncts.

There are two types of Search Service provided by the platform.

* Manifest-level _Search Within_ is available on any _managed_ IIIF Manifest (not manifests generated from named queries). This is suitable for finding particular words and phrases within one book or document, and is supported by viewers like UV and Mirador.<sup>[63p](https://github.com/dlcs/private-protagonist/issues/63)</sup>
* Fuzzy<sup>name</sup> search is available on Collections, including virtual collections from queries<sup>[61pc](https://github.com/dlcs/private-protagonist/issues/61#issuecomment-1644232499)</sup> (e.g., search within a facet). It supports typical Lucene-derived search features. You would typically consume this in your own custom web applications rather than from a viewer.<sup>[83p](https://github.com/dlcs/private-protagonist/issues/83)</sup>

Both types of search are provided as IIIF Search API endpoints.

## Platform-generated adjuncts<sup>[13p](https://github.com/dlcs/private-protagonist/issues/13)</sup>

Sometimes you may already have adjuncts, and can use the platform to store them (and sometimes generate search services from them). These may come from a digitisation workflow (e.g., OCR files), or they may come from ad hoc enrichment (e.g., a project generating datasets for each image, or AI-driven descriptions of each image).

But you can also get the IIIF Cloud Services Platform to generate adjuncts using a number of _enrichment services_ such as:

* OCR
* Handwriting recognition
* Image analysis and description
* ...more to come

You can do this in the Portal or via the API.

## Putting it together

This means that in the portal, or via the API, you can:
 
* Create a manifest by registering a set of images using any of the methods described in [IIIF Images](iiif-images) (these methods apply to any asset type not just images).
* Specify you want the platform to generate OCR data from the images.
* Specify you want the platform to attach a IIIF Search API service to the Manifest.

These latter two behaviours can be set as defaults, so you could simply go to the portal, select some images by browsing your own Dropbox or Google Drive, and immediately create a published, searchable IIIF Manifest that works in any viewer.


> <small>touched 2025-09-23T12:04:54</small>