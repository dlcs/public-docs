"""Shared values for the searchable-manifest recipe steps."""
import os
from pathlib import Path
import settings

customer = settings.IIIF_CS_CUSTOMER_ID
space = settings.docs_space_id
presentation_host = settings.IIIF_CS_PRESENTATION_HOST

# The eight fixture pages: a public-domain book from Wellcome Collection
# (b3343136x, "The energy index"), committed to this repo. They are both the
# local input for the OCR step and, via the published docs site, the HTTP
# origins the platform fetches images and ALTO from.
PAGES = [f"{n:04d}" for n in range(1, 9)]
FIXTURE_BASE = os.environ.get(
    "RECIPE_FIXTURE_BASE",
    "https://dlcs.github.io/public-docs/doc_fixtures/recipes/energy-index")
LOCAL_FIXTURES = Path(__file__).resolve().parents[2].parent / "src" / "public" / "doc_fixtures" / "recipes" / "energy-index"

asset_id_prefix = "energy-index"
manifest_slug = "energy-index"
manifest_path = f"/{customer}/manifests/{manifest_slug}"
