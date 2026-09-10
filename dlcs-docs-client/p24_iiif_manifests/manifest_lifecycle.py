import settings
from iiif_cs import get_iiif_resource, put_iiif_resource, delete_iiif_resource, pprint

# A minimal Manifest lifecycle on the IIIF Presentation API: create with PUT,
# read it back (API view and public view), update it with If-Match, delete it.
# The Manifest here is plain IIIF - its one canvas paints an image that the
# platform does not manage - so no ingest happens and every step is immediate.

manifest_slug = "docs-manifest-lifecycle"
manifest_path = f"/{settings.IIIF_CS_CUSTOMER_ID}/manifests/{manifest_slug}"
root_collection = f"{settings.IIIF_CS_PRESENTATION_HOST}/{settings.IIIF_CS_CUSTOMER_ID}/collections/root"


def make_manifest(label):
    return {
        "type": "Manifest",
        "label": {"en": [label]},
        "parent": root_collection,
        "slug": manifest_slug,
        "items": [
            {
                "id": "https://example.org/canvas/1",
                "type": "Canvas",
                "width": 1000,
                "height": 800,
                "items": [
                    {
                        "id": "https://example.org/page/1",
                        "type": "AnnotationPage",
                        "items": [
                            {
                                "id": "https://example.org/anno/1",
                                "type": "Annotation",
                                "motivation": "painting",
                                "target": "https://example.org/canvas/1",
                                "body": {
                                    "id": "https://dlcs.github.io/public-docs/doc_fixtures/printed-seq/01.jpg",
                                    "type": "Image",
                                    "format": "image/jpeg",
                                    "width": 1000,
                                    "height": 800
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }


def delete_if_present():
    """A DELETE needs the current ETag, so GET first."""
    r = get_iiif_resource(manifest_path)
    if r.status_code == 200:
        delete_iiif_resource(manifest_path, r.headers["ETag"])


def create_manifest():
    """A PUT to a slug that doesn't exist yet creates the Manifest (201). No If-Match on create."""
    r = put_iiif_resource(manifest_path, make_manifest("Manifest lifecycle example"))
    pprint(r.json())
    return r


def read_manifest():
    """With Show-Extras the API view comes back (slug, parent, paintedResources...) and an ETag.
    Without it, and without auth, the same URL serves plain IIIF."""
    r = get_iiif_resource(manifest_path)
    api_view = r.json()
    print("API view keys:", sorted(api_view.keys()))
    # The flat URL is the API's; a public client is redirected to the hierarchical (public) URL...
    public = get_iiif_resource(manifest_path, extras=False)
    print("Redirected to:", public.headers["Location"])
    # ...which serves plain IIIF, with none of the API-view properties
    public = get_iiif_resource(public.headers["Location"], extras=False)
    print("Public view keys:", sorted(public.json().keys()))
    return r.headers["ETag"]


def update_manifest(etag):
    """A PUT to an existing slug replaces the Manifest; If-Match must carry the ETag from the GET."""
    r = put_iiif_resource(manifest_path, make_manifest("Manifest lifecycle example (updated)"), etag=etag)
    print("Updated label:", r.json()["label"])
    # ...and a stale or missing If-Match is refused:
    r = put_iiif_resource(manifest_path, make_manifest("This will not be saved"))
    print("PUT without If-Match on an existing Manifest ->", r.status_code)


if __name__ == "__main__":
    delete_if_present()
    create_manifest()
    etag = read_manifest()
    update_manifest(etag)
    delete_if_present()
    get_iiif_resource(manifest_path)  # 404 - it's gone
