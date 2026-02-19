# tags, roles and id queries not yet implemented

These examples belong in the `### Query object` section once supported:

```
?q={"tags": ["my-tag"]}
?q={"tags": ["my-tag", "another-tag"]}
?q={"roles": ["https://api.dlcs.example/customers/2/roles/clickthrough"]}
?q={"id":"PHOTO.2.22.36.2.tif"}
```

# Ordering not yet implemented

You can order by the value of a field of an asset:

```
?orderByDescending=width
?orderBy=height
```

If no ordering is provided the order is undefined.

(It is unclear whether the default undefined order is by creation date.)

# More examples (use ordering, not yet implemented)

```
?q={"string1":"my-value","number1":99}&orderBy=width&pageSize=10&page=12
?string1=my-value&orderByDescending=string3&page=9
```

# Multiple values not yet implemented

```
?q={"string1":["a","b"]}
```

`string1` can only take one value per asset, therefore this is interpreted as "assets where string1=a OR string1=b".

```
?q={"tags":["a","b"]}
```

`tags` could have both these values in a single asset, but we still treat this as an OR rather than an AND: "assets that have the tag "a" OR the tag "b" OR both. There is currently no syntax for requesting only assets that have BOTH tags.

```
?q={"id":["PHOTO.2.22.36.2.tif","other-image.jp2","my-video"]}
```

`id` is the internal _Model Id_ (see [Identifiers](identifiers)), the last part of the URI. This query returns all assets that match that identifier. If used to filter assets on `/customers/{customer}/allImages`, the returned assets could be in any of the customer's spaces (but never any other customer), so even a single value for `id` could return more than one asset. On `/customers/{customer}/spaces/{space}/images`, each requested `id` value can only return 0 or 1 assets, because this value must be unique within a space.
