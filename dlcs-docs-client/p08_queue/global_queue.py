from iiif_cs import get_cloud_services_resource, pprint


def get_global_queue():
    """GET the global queue to see its current status."""
    path = "/queue"
    r = get_cloud_services_resource(path)
    print("GET Global Queue returned:")
    queue = r.json()
    pprint(queue)
    print()
    return queue


if __name__ == '__main__':
    # Get the current global queue
    get_global_queue()