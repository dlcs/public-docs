from iiif_cs import get_cloud_services_resource, pprint
from p08_queue.get_adjunct_batches import get_adjunct_batches


def get_adjunct_batch(batch_url):
    """GET a specific adjunct batch by its URL."""
    r = get_cloud_services_resource(batch_url)
    print("GET Adjunct Batch returned:")
    batch = r.json()
    pprint(batch)
    print()
    return batch


def get_adjunct_batch_current(batch):
    """GET the collection of adjuncts currently associated with this batch.
    An adjunct belongs to only one batch: the most recent batch it was part of.
    If adjuncts have been re-submitted in a later batch, they will not appear here.
    """
    current_url = batch["currentAdjuncts"]
    r = get_cloud_services_resource(current_url)
    print("GET Adjunct Batch currentAdjuncts returned:")
    current = r.json()
    pprint(current)
    print()
    return current


def get_adjunct_batch_adjuncts(batch):
    """GET the collection of all adjuncts originally submitted in this batch.
    Unlike currentAdjuncts, this includes adjuncts that have since been claimed by a later batch.
    """
    adjuncts_url = batch["adjuncts"]
    r = get_cloud_services_resource(adjuncts_url)
    print("GET Adjunct Batch adjuncts returned:")
    adjuncts = r.json()
    pprint(adjuncts)
    print()
    return adjuncts


if __name__ == '__main__':
    adjunct_batches = get_adjunct_batches()
    members = adjunct_batches.get("member", [])
    if not members:
        print("No adjunct batches found. Submit adjuncts to the adjunct queue first.")
    else:
        example_batch_url = members[0]["@id"]
        example_batch = get_adjunct_batch(example_batch_url)

        get_adjunct_batch_current(example_batch)
        get_adjunct_batch_adjuncts(example_batch)
