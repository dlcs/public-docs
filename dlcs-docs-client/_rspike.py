import io, json, os, time, requests, settings
from iiif_cs import (get_iiif_resource, put_iiif_resource, delete_iiif_resource,
                     get_cloud_services_resource, delete_resource, PRESENTATION_HEADERS)
H = settings.IIIF_CS_PRESENTATION_HOST
PUB = "https://dlcs-stage.digirati.io"
ROOT = f"{H}/15/collections/root"
S3 = "https://dlcsstage-public-test-objects.s3.eu-west-1.amazonaws.com/images-with-text"
OUT = r"C:\git\dlcs\public-docs\scratch\hygiene-sprint\s7-captures"
def dump(name, obj):
    io.open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8", newline="\n").write(
        json.dumps(obj, indent=4, ensure_ascii=False) + "\n")
def wait_pipeline(path):
    for i in range(30):
        g = get_iiif_resource(path)
        b = g.json()
        if not b.get("pipeline") and not b.get("ingesting"):
            return g, b
        time.sleep(6)
    return g, b

print("########## SPIKE A: inline adjuncts at manifest save (v0.10.0?)")
m = {"type": "Manifest", "label": {"en": ["recipe spike A"]}, "slug": "hyg7-rspike", "parent": ROOT,
     "paintedResources": [{
        "asset": {"id": "page_01", "space": 98765,
                  "adjuncts": [
                     {"id": "spike-alto.xml", "origin": f"{S3}/b29820947_0014.jp2.xml", "@type": "Dataset",
                      "mediaType": "text/xml", "label": {"en": ["ALTO"]}, "iiifLink": "seeAlso"},
                     {"id": "spike-text.txt", "origin": "https://dlcs.github.io/public-docs/doc_fixtures/adjuncts/rusty-boat.txt",
                      "@type": "Text", "mediaType": "text/plain", "label": {"en": ["Text"]},
                      "iiifLink": "inlineAnnotation", "motivation": "supplementing"}]},
        "canvasPainting": {"canvasOrder": 0}}],
     "pipeline": [{"name": "text", "config": {"action": "Index"}}]}
r = put_iiif_resource("/15/manifests/hyg7-rspike", m)
print("A create ->", r.status_code, r.text[:250] if r.status_code >= 400 else "")
if r.status_code < 400:
    g, b = wait_pipeline("/15/manifests/hyg7-rspike")
    print("A finishedPipelines:", json.dumps(b.get("finishedPipelines"))[:180])
    ar = get_cloud_services_resource("/customers/15/spaces/98765/images/page_01/adjuncts")
    print("A adjuncts on page_01 now:", [m2["@id"].rsplit("/",1)[-1] for m2 in ar.json().get("member", [])])
    pub = requests.get(b["publicId"], allow_redirects=True)
    pm = pub.json() if pub.status_code == 200 else {}
    c0 = pm.get("items", [{}])[0]
    print("A public: seeAlso:", bool(c0.get("seeAlso")), "| annotations:", bool(c0.get("annotations")),
          "| search service:", bool(pm.get("service")))
    dump("rspike-A-public", pm)

    print("\n########## SPIKE PDF: probing text-services routes")
    for route in ["pdf", "fulltext", "text", "annotations", "figures", "textaugmented", "textbuilder"]:
        for form in [f"{PUB}/{route}/v2/15/iiif/hyg7-rspike", f"{PUB}/{route}/15/iiif/hyg7-rspike"]:
            rr = requests.get(form, allow_redirects=True)
            if rr.status_code != 404:
                print(f"  {form} -> {rr.status_code} ct={rr.headers.get('content-type','')[:40]} len={len(rr.content)}")
