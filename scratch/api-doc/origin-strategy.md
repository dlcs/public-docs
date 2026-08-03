# Credentials behaviour on PUT — RESOLVED (2026-06-24)

Verified against `API/Features/OriginStrategies/Requests/UpdateCustomerOriginStrategy.cs`. A PUT to `/customers/{customer}/originStrategies/{id}`:
- **Does** update stored credentials when a _full_ strategy object (regex, strategy, credentials, optimised, order all present) is supplied — exported to secure storage (`existingStrategy.Credentials = S3Uri`). A partial object with credentials is rejected ("A full origin strategy object is required when updating credentials").
- Credentials may only be set when the strategy is `basic-http-authentication` or `sftp`; supplying them for any other strategy type is rejected.
- Setting strategy to `basic-http-authentication` requires credentials (400 if omitted); changing the strategy away from it wipes the stored credentials.

The page was corrected on 2026-06-24. Original (incorrect) live-doc text:
> For strategies that require credentials, [credentials](#credentials) must also be present in the PUT body for validation, but the stored credentials are not updated by a PUT to this resource — use the [credentials sub-resource](#http-operations-1) for that.

# Credentials sub-resource not yet implemented

The `/customers/{customer}/originStrategies/{id}/credentials` sub-resource returns 404 for both PUT and DELETE. When implemented, it is intended to allow credentials to be updated independently of the rest of the CustomerOriginStrategy. The following section was removed from the page until this is implemented:

---

You can update credentials independently of their CustomerOriginStrategy:

`/customers/{customer}/originStrategies/{id}/credentials`

| Method | Label | Expects | Returns | Status |
|:---|:---|:---|:---|:---|
| PUT | Update stored credentials | xsd:string | owl:Nothing | 200 OK |
| DELETE | Remove credentials | - | owl:Nothing | 204 No Content |

> ⟳ 2026-08-03 (PROV-22): the status codes above were silently *normalised* when this
> section was preserved. The ORIGINAL old-doc table said **201** for PUT and **201**
> for DELETE (yes, 201 on DELETE). Recording that here so the preserved text doesn't
> misrepresent the original — if the sub-resource is ever built, pick codes per the
> XC-01/XC-03 conventions, not either version of this table.

When sending credentials via PUT, the request body is an escaped JSON string, not a JSON object:

```
PUT /customers/2/originStrategies/48702c3d-0529-4b52-9433-7f7f04e91e33/credentials
{ \"user\": \"uuu\", \"password\": \"ppp\" }
```

Note that there is no GET operation on credentials.
