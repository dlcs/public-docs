# Credentials behaviour on PUT needs revisiting

When making a PUT to `/customers/{customer}/originStrategies/{id}`, the API currently:
- Requires credentials to be present in the body for strategies that need them (e.g. basic-http-authentication), returning 400 if omitted
- Does NOT update the stored credentials when they are supplied in the PUT body

It is unclear whether this is intentional design (credentials are required for validation only) or whether the API should accept a PUT without credentials and simply leave the stored credentials unchanged. This behaviour should be confirmed and the documentation updated accordingly.

# Credentials sub-resource not yet implemented

The `/customers/{customer}/originStrategies/{id}/credentials` sub-resource returns 404 for both PUT and DELETE. When implemented, it is intended to allow credentials to be updated independently of the rest of the CustomerOriginStrategy. The following section was removed from the page until this is implemented:

---

You can update credentials independently of their CustomerOriginStrategy:

`/customers/{customer}/originStrategies/{id}/credentials`

| Method | Label | Expects | Returns | Status |
|:---|:---|:---|:---|:---|
| PUT | Update stored credentials | xsd:string | owl:Nothing | 200 OK |
| DELETE | Remove credentials | - | owl:Nothing | 204 No Content |

When sending credentials via PUT, the request body is an escaped JSON string, not a JSON object:

```
PUT /customers/2/originStrategies/48702c3d-0529-4b52-9433-7f7f04e91e33/credentials
{ \"user\": \"uuu\", \"password\": \"ppp\" }
```

Note that there is no GET operation on credentials.
