import settings
from iiif_cs import get_cloud_services_resource, post_resource, patch_resource, delete_resource, pprint, wait_for_value
from p06_space.ensure_space import ensure_space


def setup_assets():
    """Ensure the space exists and register two groups of assets with varied metadata.
    The different string1, string3, number1 and number2 values make it possible to
    demonstrate several named query templates."""
    space_path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{settings.named_query_space_id}"
    ensure_space(settings.named_query_space_id, settings.named_query_space_name)
    patch_resource(space_path, {"name": settings.named_query_space_name})

    space = settings.named_query_space_id
    collection = {
        "@type": "hydra:Collection",
        "member": [
            {
                "id": "nq_01", "space": space, "mediaType": "image/jpeg",
                "origin": "https://dlcs.github.io/public-docs/doc_fixtures/printed-seq/01.jpg",
                "string1": "autumn-1985", "string3": "prints", "number1": 1, "number2": 10
            },
            {
                "id": "nq_02", "space": space, "mediaType": "image/jpeg",
                "origin": "https://dlcs.github.io/public-docs/doc_fixtures/printed-seq/02.jpg",
                "string1": "autumn-1985", "string3": "prints", "number1": 2, "number2": 20
            },
            {
                "id": "nq_03", "space": space, "mediaType": "image/jpeg",
                "origin": "https://dlcs.github.io/public-docs/doc_fixtures/printed-seq/03.jpg",
                "string1": "autumn-1985", "string3": "prints", "number1": 3, "number2": 30
            },
            {
                "id": "nq_04", "space": space, "mediaType": "image/jpeg",
                "origin": "https://dlcs.github.io/public-docs/doc_fixtures/printed-seq/04.jpg",
                "string1": "summer-1984", "string3": "photos", "number1": 1, "number2": 10
            },
            {
                "id": "nq_05", "space": space, "mediaType": "image/jpeg",
                "origin": "https://dlcs.github.io/public-docs/doc_fixtures/printed-seq/05.jpg",
                "string1": "summer-1984", "string3": "photos", "number1": 2, "number2": 20
            },
            {
                "id": "nq_06", "space": space, "mediaType": "image/jpeg",
                "origin": "https://dlcs.github.io/public-docs/doc_fixtures/printed-seq/06.jpg",
                "string1": "my-string", "number1": 1
            },
            {
                "id": "nq_07", "space": space, "mediaType": "image/jpeg",
                "origin": "https://dlcs.github.io/public-docs/doc_fixtures/printed-seq/07.jpg",
                "string1": "my-string", "number1": 2
            },
        ]
    }
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/queue"
    r = post_resource(path, collection)
    batch = r.json()
    print(f"Batch {batch['@id']} has {batch['count']} items")
    print()
    wait_for_value(path=batch['@id'], field="completed", value=7, interval=2, retries=10)
    print("Assets ready.")
    print()


def make_public_manifest_url(customer_name, nq_name, *params):
    """Construct the public-facing named query URL:
        https://dlcs.example/iiif-resource/{customer-name}/{query-name}/{p1}/{p2}/..."""
    public_host = settings.IIIF_CS_API_HOST.replace("//api.", "//", 1)
    param_path = "/".join(str(p) for p in params)
    if param_path:
        return f"{public_host}/iiif-resource/{customer_name}/{nq_name}/{param_path}"
    return f"{public_host}/iiif-resource/{customer_name}/{nq_name}"


def print_manifest_summary(manifest):
    canvases = manifest.get('items', [])
    print(f"Manifest: {len(canvases)} canvas(es)")
    for canvas in canvases:
        label_text = next(iter(canvas.get('label', {}).values()), ['?'])[0]
        w = canvas.get('width', '?')
        h = canvas.get('height', '?')
        meta = {
            next(iter(e['label'].values()), ['?'])[0]: next(iter(e['value'].values()), [''])[0]
            for e in canvas.get('metadata', [])
        }
        meta_str = ', '.join(f"{k}={v}" for k, v in meta.items() if v)
        print(f"  {label_text} ({w}x{h}): {meta_str}")
    print()


def demonstrate(nq_name, template, *params):
    """Create a named query with the given template, construct the public URL,
    fetch the resulting manifest, then delete the named query."""
    print(f"=== Template: {template} ===")
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/namedQueries"
    nq = post_resource(path, {"name": nq_name, "template": template}).json()
    pprint(nq)
    print()

    url = make_public_manifest_url(settings.IIIF_CS_CUSTOMER_NAME, nq_name, *params)
    print(f"Public URL: {url}")
    r = get_cloud_services_resource(url)
    print_manifest_summary(r.json())

    delete_resource(nq['@id'])
    print()


if __name__ == '__main__':
    # Set up the space and assets
    setup_assets()

    # canvas=n1&s1=p1
    # Selects assets where string1 equals the first URL parameter, across all spaces.
    # Ordered by number1. Returns 3 canvases for "autumn-1985".
    demonstrate("nq-by-s1", "canvas=n1&s1=p1",
                "autumn-1985")

    # canvas=n2&spacename=p1&s1=p2
    # Restricts to the named space (p1) and selects by string1 (p2).
    # Ordered by number2. Returns 3 canvases for "autumn-1985" in the named space.
    demonstrate("nq-by-spacename-s1", "canvas=n2&spacename=p1&s1=p2",
                settings.named_query_space_name, "autumn-1985")

    # canvas=n2&space=p1&s3=p2
    # Restricts to the space by numeric id (p1) and selects by string3 (p2).
    # Ordered by number2. Returns 3 canvases where string3="prints".
    demonstrate("nq-by-space-s3", "canvas=n2&space=p1&s3=p2",
                settings.named_query_space_id, "prints")

    # canvas=n2&s1=p1&n1=p2
    # Selects by string1 (p1) AND number1 (p2) — both fields are selectors.
    # Ordered by number2. Since both string1 and number1 must match, in this simple case
    # it only returns a single canvas (the asset where string1="autumn-1985" and number1=2).
    # In a real world example, it might constrain a volume number.
    demonstrate("nq-by-s1-n1", "canvas=n2&s1=p1&n1=p2",
                "autumn-1985", 2)

    # canvas=n1&s1=p1&#=my-string
    # The "&#=my-string" syntax hardcodes the value of p1 to "my-string" in the template.
    # No URL parameters are needed — the public URL is just /{nq-name}.
    demonstrate("nq-hardcoded", "canvas=n1&s1=p1&#=my-string")
