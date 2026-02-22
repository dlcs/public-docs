# pdf and zip output types not yet implemented

The output-type table in the page originally listed three values:

| output-type | |
|:---|:---|
| `iiif-resource` | Generates a IIIF Manifest |
| `pdf` | Generates a PDF |
| `zip` | Generates a zip file |

Restore the `pdf` and `zip` rows to the table once these are implemented.


# PDF-specific template parameters not yet implemented

> Check these again when making new docs PRs

The following parameters appeared in complex examples but are likely not yet supported:

| `objectname` | The filename used when the result is downloaded | `&objectname={s1}_{n1}.pdf` |
| `coverpage` | URL of a cover page to prepend to a generated PDF | `&coverpage=https://example.org/cover/{s1}` |
| `redactedmessage` | Message to display for access-controlled pages in a PDF | `&redactedmessage=This page is restricted` |
| `roles` | Restrict the named query result to a role | `&roles=https://api.dlcs.example/customers/2/roles/clickthrough` |

# Complex examples (use unimplemented PDF parameters)

```
manifest=s1&sequence=n1&canvas=n2&s1=p1&n1=p2&space=p3&#=5&objectname={s1}_{n1}.pdf&coverpage=http://wellcomelibrary.org/service/pdfcoverpageaspdf/{s1}/0&roles=https://api.dlcs.example/customers/2/roles/clickthrough&redactedmessage=This page is restricted and is not available in PDF downloads
```

```
manifest=s3&sequence=n1&canvas=n2&s3=p1&objectname={s3}&coverpage=http://wellcomelibrary.org/service/pdfcoverpage/{s3}/0&roles=https://api.dlcs.example/customers/4/roles/clickthrough
```

```
manifest=s3&canvas=n2&space=p1&s3=p2&objectname={s3}_{n2}.pdf&coverpage=https://iiif.wellcomecollection.org/pdf-cover/{s3}&roles=https://api.dlcs.example/customers/2/roles/clickthrough&redactedmessage=This page is restricted and is not available in PDF downloads
```

# manifest field

Verify what the manifest id should look like in this query (currently "xxxx")

# global named queries

should I be able to see other customer's NQs?

