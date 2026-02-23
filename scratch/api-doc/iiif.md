# THIS WHOLE PAGE IS COPIED TO SCRATCG

Will come back to it.

-----


# IIIF Manifests and Collections 🆕

{/* This will need rewriting for public consumption, there's no need be "historic" */}

## Two different concerns

Historically the IIIF Cloud Services Platform has been about _Asset Delivery_ - most obviously, providing IIIF Image API endpoints for [any image assets you register with it](registering-assets). The platform solves the problem of "I have these images on my desktop, how do I make them available as IIIF Image Services for deep zoom?"

The creation, management and serving of IIIF Presentation API resources - Manifest, Collections and Annotation Pages - can be an independent, external concern, typically varying from implementation to implementation. Whether constructed in a text editor or in a rich Manifest Editor, the platform didn't provide a solution for storing and hosting _hand-crafted_ Manifests. And nor did it provide a IIIF Presentation Server for machine-generated IIIF. 

A Manifest is a fairly small text document, but even if leaning on the platform to do the heavy lifting of Image API provision and AV transcoding for the Content Resources used by your Manifest, you were left with the problem of where you host the Manifest itself.

A good approach would be a document store, using simple HTTP semantics for create, read, update and delete (CRUD) operations. There are several options already for storing JSON documents (which all IIIF Presentation API resources are) in a document repository with HTTP CRUD operations, and these could be put to good use an an IIIF repository. For example, [CouchDB](https://couchdb.apache.org/).

**Now, IIIF Cloud Services offers a IIIF-aware document-store or repository for Presentation API resources - it can validate incoming IIIF, it understands the relationship between IIIF Manifests and Collections.**

You can PUT or POST a Manifest to the platform, and it will validate and serve it to public users. This can be completely independent of any asset delivery concerns:

 - On `https://api.dlc.services/customers/99/spaces/999/<asset>` the platform offers the ability to register assets and provision IIIF Image Services, AV transcodes and more, which are made available to the public as derivatives at `https://dlc.services/<delivery-channel>/99/999/<asset>` (the platform provides services for **content resources**)
 - On `https://iiif.dlc.services/99/collections/<collection>` and `https://iiif.dlc.services/99/manifests/<manifest>` the platform allows you to store IIIF Presentation API resources - JSON-LD documents, which are _typically_ made available to the public at `https://iiif.dlc.services/99/<hierarchical-resource-path>`

> _Customer 99 is used an an example throughout this documentation_

The Manifests in the second bullet point might reference the assets in the first - but they don't _have_ to. You could use the platform to store IIIF that you write in a Manifest Editor that uses existing IIIF resources on the web; you could use the platform to store Manifests without using it for delivering **any** image services or other asset derivatives.

>❓The RFC reference this discussion about [endpoints](020-files/api-endpoints.md) - Option 3a in that document puts the IIIF API on a different host from the rest of the API - and it's the public-facing endpoint too. Unlike assets, where the IIIF-CS API is very different from the derivatives and services it produces, the Presentation API support deals with IIIF at CRUD-time as well as public-facing runtime. This document assumes Option 3a is chosen.

## Named Queries

The Platform has always offered a way to _generate_ IIIF Manifests from assets - using [Named Queries](named-queries) you can _project_ registered assets into Manifests. 

A common pattern for use of IIIF Cloud Services is to register assets with at least two metadata fields - one to **group** a set of assets together (e.g., 37 assets all with the string metadata value "book-995"), and one to order them (e.g., those same 37 assets have an ascending integer metadata field that runs from 1 to 37). Then, use the Named Query feature to *project* those assets into what we usually refer to as a _Skeleton Manifest_ ([here's an example](https://dlcs.io/iiif-resource/wellcome/preview/5/b31477707) - this JSON is the projection of a query into IIIF-Manifest form).

But these Manifests are really just **query results**; you can't give them the full richness of IIIF, you can't set additional fields, you can't provide structure. A common technique is to generate "skeleton" manifests using named queries, and then decorate them with the full metadata you want them to have, and then store and serve them somewhere else.


## Asset-centric, or Presentation-API-centric, or both

The Asset-centric approach is very powerful in large integrations, with custom code **synchronising** the IIIF Cloud Services assets with their expected statuses, and managing the process with [Batches](batch), [queues](queues), and other workflow-friendly processes. Millions of assets can be synchronised in this way, with external processes responsible for using those assets in IIIF Manifests.

The Presentation-API-centric approach is very powerful for smaller scale or ad hoc collection building, especially when used as the back end of manual IIIF Creation tools. It's also useful to very large scale projects, as it takes care of IIIF serving and allows further enrichment services (such as full text search) to be built for IIIF Manifests and Collections.

The approach to IIIF Presentation API resources described here combines the best of both.

 - You can use the platform to store IIIF Manifests and Collections as JSON documents, repository-style.
 - You can use the platform to register assets into Spaces, with metadata, that you can use for named queries to generate skeleton manifests - or create and manage your own Manifests independently.
 - You can use the platform to create Manifests and register their assets at the same time: **a Manifest is both a container of assets (like a Space) and also a IIIF Presentation API resource capable of carrying any information a IIIF Manifest can carry.**

This part of the documentation will describe IIIF Collections and Manifests, and their relationship with assets registered with the platform, and with external content resources.

See also [Adjuncts](adjuncts) and [Pipelines](pipelines) for additional resources referenced from Manifests, and ways of creating them.

## Key Concepts

The API uses the following **storage** concepts - resources you can create an interact with over HTTP:

* **Manifests**, that can contain assets, similar to the way a [Space](space) can contain assets (in fact, the Manifest has its own dedicated Space)
* Collections, that can contain Manifests or other Collections, but that come in two flavours:
  * **IIIF Collections** - e.g., to represent multi-volume works and periodicals
  * **Storage Collections** - like folders to organise the storage of IIIF resources within the platform, in an arbitrary hierarchy

For assets, you manage them on `api.dlc.services` and expose services derived from them on `dlc.services` (e.g., a IIIF Image Service).
But Manifests and Collections share the same URIs for editing and serving to the public - on iiif.dlc.services. By default, you see what the public see, except that:

* You need to supply credentials in the request to see non-public resources, and to perform any creation, updating or deletion.
* You need to provide an additional header AND credentials to see the additional properties and services offered by the platform for managing and editing your IIIF Manifests and Collections, and the assets they reference.

> TODO: rewrite rules

Building from these storage/containment concepts:

* On `iiif.dlc.services`, all IIIF resources are **valid IIIF Manifests or Collections**, although they can carry additional information when you supply the header mentioned above. This is different from assets, where, for example, the API [Asset](asset) resource bears no resemblance to a IIIF Image Service that the platform might provide for that asset. Having the API as valid IIIF allows existing tools and libraries to work with it.
* A **IIIF Manifest** always has a stored JSON representation in the repository, that can carry **any information that we can model in valid IIIF** - the JSON representation is a IIIF Presentation API 3.0 Manifest.
* A **IIIF Collection** always has a stored JSON representation too. 
* A **Storage Collection** acts as a container, and doesn't have a rich stored JSON representation, and can't carry all that we can model in IIIF.
* However, the platform exposes Storage Collections as IIIF Presentation API 3.0 Collections. You can't add arbitrary additional IIIF properties to a Storage Collection, but it is _navigable_ by any client (an IIIF-browser) that understands a IIIF Collection. We don't have two completely different types of _container_. 
* The `items` property of a Storage Collection is not editable as JSON. It always reflects the child _contained_ manifests and collections stored in the platform, and is generated automatically. 
* The `items` property of a IIIF Collection is editable as JSON, and can reference ANY Manifests or Collections whether they are managed by the platform or not.
* An asset can appear in multiple Manifests if required - it's not confined to the Manifest it was put into.
* A stored Manifest can reference IIIF Image API endpoints and other content resources (images, AV, etc) _that are not being provided by the IIIF Cloud Services Platform_. A Platform-stored Manifest can have all of its assets registered with the Platform, or some of them, or even none of them.
* While you can **manually** construct the Canvases, Annotation Pages and Painting Annotations that populate your Manifests with Content Resources, the Platform APIs make it very easy to construct Manifests by simply adding assets to them.
* Having the platform generate the Canvases from assets automatically doesn't stop you later editing any IIIF details of the Canvases, or adding new assets.
* Clients of the Platform APIs can "synchronise" a Manifest _and_ its assets with the Platform in a single operation.

### IIIF Structure

A Manifest is not just a sequence of assets; a Manifest's `items` property is a sequence of Canvases, each of which has one or more Annotation Pages, each of which has one or more Annotations, of which at least one is usually an Annotation with the motivation `painting` that provides the Canvas's content. This multi-level structure is what gives IIIF its power, but we don't require Platform API consumers to navigate this structure just to add an asset to a Manifest. But neither do we pretend that the structure doesn't exist and prevent the use cases that need this structure.


## Hierachical URIs and Flat URIs for IIIF Manifests and Collections

It is often desirable to provide a hierarchical URL structure for Storage Collections, IIIF Collections and Manifests, so that you can have URLs like:

 - `https://iiif.dlc.services/99/manuscripts/14th-century/ms-125`

... which is a Manifest, inside a Collection, inside another Collection. URLs like this may also reflect archival hierarchy or any other logical organisation of content:

 - `https://iiif.dlc.services/99/` - the root of your IIIF Storage, exposed as a IIIF Collection
 - `https://iiif.dlc.services/99/manuscripts/` - a Storage Collection, exposed as a public IIIF Collection
 - `https://iiif.dlc.services/99/manuscripts/14th-century` - a Storage Collection, exposed as a public IIIF Collection
 - `https://iiif.dlc.services/99/manuscripts/14th-century/ms-125` - a IIIF Manifest

Each of these resources has a _parent_ and a _[slug](https://en.wikipedia.org/wiki/Clean_URL#Slug)_; for the last one, the parent is the Collection `https://iiif.dlc.services/99/manuscripts/14th-century` and the slug is the string `"ms-125"` - the string that contributes the last path element of the URL.

The IIIF-CS platform acts as a hierarchical IIIF Repository - like a file system but with Storage Collections acting as directories, and Manifests acting as files. IIIF Collections have both file and directory characteristics, as explained later.

It is also desirable to be able to _move_ resources from one part of the hierarchy to another, like moving a file from one folder to another. You should be able to change the parent of a resource ("move to a different folder"), and change its slug ("rename it").

However this gives us a problem of identity - changing either of these changes its public HTTP URI.

We solve this by allowing IIIF Presentation API resources to have a "flat", fixed identity that never changes, _as well as_ a resolvable URL derived from parent and slug, providing arbitrary depth of _path elements_. All IIIF resources are available on **both** versions. You can configure which you consider canonical, and a public GET request will redirect to the canonical version if requested on the other. As you build client applications, you can choose which approach to adopt. The default behaviour is for the hierarchical version to be canonical for public unauthenticated requests. If you have no need of a hierarchical representation in your public URLs, you can default to the flat, persistent form.

The flat API versions of the above examples may look something like this:

 - `https://iiif.dlc.services/99/collections/root` - the root of your IIIF Storage, exposed as a IIIF Collection
 - `https://iiif.dlc.services/99/collections/g7hb5f4e` - a Storage Collection, exposed as a public IIIF Collection
 - `https://iiif.dlc.services/99/collections/d44eeb7a` - a Storage Collection, exposed as a public IIIF Collection
 - `https://iiif.dlc.services/99/manifests/gb799m5z` - a IIIF Manifest

`/<customer-id>/collections/root` is created for you already. The last element of the flat identity URI is generated for you (here `g7hb5f4e`, `d44eeb7a` etc.) unless you specify it by creating the resource with a PUT, or by including the full `id` property (see below). For some applications, it is fine to leave the assignment of this identifier to the platform. But for others you will want this identifier to correspond to a unique identifier for the thing the IIIF Resource represents (e.g., a catalogue identifier) so will want to set it yourself. It must be URL-safe - that is, must not contain a character that would be URL-encoded.

### Reserved names

The following are reserved names; you can't create resources with these `slugs`:

 - `collections`
 - `manifests`
 - `paintedResources`
 - `canvases`
 - `annotations`
 - `adjuncts`
 - `pipelines`
 - `queue`
 - `assets` 
 - `configuration`
 - `publish`

Each of these special slugs partitions the URL space at the root of your IIIF space - we have already seen `https://iiif.dlc.services/99/collections/<flat-id>` and `https://iiif.dlc.services/99/manifests/<flat-id>`; `https://iiif.dlc.services/99/collections` and `https://iiif.dlc.services/99/manifests` are themselves paged IIIF Collections containing _all_ of your resources! The others are access points for other functionality described later. None of these may be used as a slug, at any level of the hierarchy.

>❓Should we better avoid the risk of users wanting these slugs by naming them `_collections`, `_manifests`, `_adjuncts` and so on?

## Storage Collections

>❓Examples assume the default configuration where the hierarchical form is canonical.

All customers start with a root Storage Collection that cannot be deleted:

 - `https://iiif.dlc.services/99` is the public root Storage Collection in the default hierarchical form.
 - `https://iiif.dlc.services/99/collections/root` is the flat form.

## Special Headers

Unlike the asset-centric parts of the DLCS, the public URLs of your IIIF are the same as the URLs you perform CRUD REST operations on. However, only `HTTP GET` on public resources is permitted without credentials (your root collection can be made private).

### X-IIIF-CS-Show-Extras

By default, all returned IIIF resources are plain IIIF Presentation API 3.0. But the platform has a large number of extra features that are designed to enable complex workflows. To see these extra properties and services, you need to supply an additional HTTP Header:

```
GET /99/manifests/yh8r5432 
Host: iiif.dlc.services
X-IIIF-CS-Show-Extras: All
Authorization: <(credentials here)>
```

Currently the only valid value of this header is `All`. Any other value will be treated as if the header was not supplied. This header MUST be accompanied by an Authorization header. If it lacks an Authorization header, it is automatically an HTTP 401 response. With an Authorization header, the response may be 401 or 403 as appropriate. 

With the header, the returned JSON is still valid IIIF, but it has an extra JSON-LD `@context` at the top, that defines additional property and service names used in the Manifest or Collection and described below. It is hidden by default to allow you to edit and create "vanilla" IIIF in any tool, without risking confusing that tool with fields it doesn't recognise, or more significantly, having that tool attempt to preserve extra fields it doesn't understand in round-trips. 

>❓The name of this header needs to be carefully chosen! This is a placeholder. `IIIF-CS-Extended` avoids the imperative "Show" and would also make it seem more natural on updates, if we need it.

>❓As we are starting a new application separate from the existing API, we should start a NEW auth scheme and use a standard OAuth2 flow. Eventually rolling that out to the existing API. Maybe... This might be a pain for integration with existing API calls.

### HTTP Operations

The following apply to all Storage Collections, including the root. The default behaviour (hierarchical path is canonical) is assumed.


| Method<br/>Headers                                 | Route                                 | Expects                                  | Returns                              | Status                       |
|:---------------------------------------------------|:--------------------------------------|:-----------------------------------------|:-------------------------------------|:-----------------------------|
| GET    <br/>-                                      | Hierachical                           | -                                        | `iiif:Collection`                    | 200, 401, 403, 404           |
| GET    <br/>-                                      | Flat                                  | -                                        | redirect to above                    | 303, 404                     |
| GET    <br/>Auth                                   | Hierachical                           | -                                        | `iiif:Collection`                    | 200, 401, 403, 404           |
| GET    <br/>Auth                                   | Flat                                  | -                                        | redirect to above                    | 303, 404                     |
| GET    <br/>Auth, Show-Extras                      | Hierachical                           | -                                        | redirect to flat                     | 303, 404                     |
| GET    <br/>Auth, Show-Extras                      | Flat                                  | -                                        | `iiif:Collection*`                   | 200, 401, 403                |
| POST   <br/>Auth, (Show-Extras)                    | Hierarchical                          | `iiif:Collection(*)`, `iiif:Manifest(*)` | `iiif:Collection*`, `iiif:Manifest*` | 201, 400                     |
| POST   <br/>Auth, (Show-Extras)                    | Flat                                  | `iiif:Collection(*)`, `iiif:Manifest(*)` | `iiif:Collection*`, `iiif:Manifest*` | 201, 400                     |
| PUT    <br/>Auth, (Show-Extras)                    | Hierarchical                          | `iiif:Collection(*)`                     | `iiif:Collection*`                   | 200, 201, 404                |
| PUT    <br/>Auth, (Show-Extras)                    | Flat                                  | `iiif:Collection(*)`                     | `iiif:Collection*`                   | 200, 201, 404                |
| PATCH  <br/>Auth, (Show-Extras)                    | Hierachical                           | partial `iiif:Collection(*)`             | `iiif:Collection*`                   | 202, 400, 404                |
| PATCH  <br/>Auth, (Show-Extras)                    | Flat                                  | partial `iiif:Collection(*)`             | `iiif:Collection*`                   | 202, 400, 404                |
| DELETE <br/>Auth                                   | Hierarchical                          | -                                        | -                                    | 202, 404                     |
| DELETE <br/>Auth                                   | Flat                                  | -                                        | -                                    | 202, 404                     |

 \* Indicates a regular IIIF Collection with the additional Storage Collection features described next. (*) Indicates either a regular or extended resource is acceptable.


>❓HTML form of table - experiment

<table>
    <thead>
        <tr>
            <th>Headers</th>
            <th>Route</th>
            <th>Expects</th>
            <th>Returns</th>
            <th>Status</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan="5"><b>GET: Retrieve a Storage Collection</b></td>
        </tr>
        <tr>
            <td>-</td>
            <td>Hierachical</td>
            <td>-</td>
            <td>`iiif:Collection`</td>
            <td>200, 401, 403, 404</td>
        </tr>
        <tr>
            <td>-</td>
            <td>Flat</td>
            <td>-</td>
            <td>redirect to above</td>
            <td>303, 404</td>
        </tr>
        <tr>
            <td>Auth</td>
            <td>Hierachical</td>
            <td>-</td>
            <td>`iiif:Collection`</td>
            <td>200, 401, 403, 404</td>
        </tr>
        <tr>
            <td>Auth</td>
            <td>Flat</td>
            <td>-</td>
            <td>redirect to above</td>
            <td>303, 404</td>
        </tr>
        <tr>
            <td>Auth, Show-Extras</td>
            <td>Hierachical</td>
            <td>-</td>
            <td>redirect to flat</td>
            <td>303, 404</td>
        </tr>
        <tr>
            <td>Auth, Show-Extras</td>
            <td>Flat</td>
            <td>-</td>
            <td>`iiif:Collection*`</td>
            <td>200, 401, 403</td>
        </tr>
        <tr>
            <td colspan="5"><b>POST: Add IIIF Collection or Manifest</b></td>
        </tr>
        <tr>
            <td>Auth, (Show-Extras)</td>
            <td>Hierarchical</td>
            <td>`iiif:Collection(*)`, `iiif:Manifest(*)`</td>
            <td>`iiif:Collection*`, `iiif:Manifest*`</td>
            <td>201, 400</td>
        </tr>
        <tr>
            <td>Auth, (Show-Extras)</td>
            <td>Flat (only to `/99/collections`)</td>
            <td>`iiif:Collection(*)`, `iiif:Manifest(*)`</td>
            <td>`iiif:Collection*`, `iiif:Manifest*`</td>
            <td>201, 400</td>
        </tr>
        <tr>
            <td colspan="5"><b>PUT: Create/update Storage Collection</b></td>
        </tr>
        <tr>
            <td>Auth, (Show-Extras)</td>
            <td>Hierarchical</td>
            <td>`iiif:Collection(*)`</td>
            <td>`iiif:Collection*`</td>
            <td>200, 201, 404</td>
        </tr>
        <tr>
            <td>Auth, (Show-Extras)</td>
            <td>Flat (only to `/99/collections/&lt;id&gt;`)</td>
            <td>`iiif:Collection(*)`</td>
            <td>`iiif:Collection*`</td>
            <td>200, 201, 404</td>
        </tr>
        <tr>
            <td colspan="5"><b>PATCH: Modify only some properties, e.g., `behavior` and/or `label` properties.</b></td>
        </tr>
        <tr>
            <td>Auth, (Show-Extras)</td>
            <td>Hierachical</td>
            <td>partial `iiif:Collection(*)`</td>
            <td>`iiif:Collection*`</td>
            <td>202, 400, 404</td>
        </tr>
        <tr>
            <td>Auth, (Show-Extras)</td>
            <td>Flat (only to `/99/collections/&lt;id&gt;`)</td>
            <td>partial `iiif:Collection(*)`</td>
            <td>`iiif:Collection*`</td>
            <td>202, 400, 404</td>
        </tr>
        <tr>
            <td colspan="5"><b>DELETE: This will not work unless the Storage Collection is empty, and is not permitted on the root Collection.</b></td>
        </tr>
        <tr>
            <td>Auth</td>
            <td>Hierarchical</td>
            <td>-</td>
            <td>-</td>
            <td>202, 404</td>
        </tr>
        <tr>
            <td>Auth</td>
            <td>Flat</td>
            <td>-</td>
            <td>-</td>
            <td>202, 404</td>
        </tr>
    </tbody>
</table>


### Differences between `X-IIIF-CS-Show-Extras` and public Storage Collections

Both resources are valid IIIF Collections as defined by the [IIIF Presentation API 3.0](https://iiif.io/api/presentation/3.0/). But there are obvious differences between the resource you operate on via the API, and the resource served to the public.

#### The `id` property

If requested with the X-IIIF-CS-Show-Extras header, the API Storage Collection always returns with the flat form of `id`:

```json
{
  "id": "https://iiif.dlc.services/99/collections/d44eeb7a"
}
```

If requested on the hierarchical form with the header, **the API will redirect to the flat form**. Clients should expect to follow redirects. This behaviour is so that CRUD operations always happen on the flat form, but you could start with just the known _public_ path of the Manifest or Collection. If you omit the header, and the _public_ behaviour is to use the hierarchical form, then the API won't redirect and the returned resource has its public ID.


```json
{
  "id": "https://iiif.dlc.services/99/manuscripts/14th-century"
}
```

You can still POST and PUT to the hierarchical form; with an authenticated request and the `X-IIIF-CS-Show-Extras` header, you can use either URL as the request target, and/or in `id` properties of supplied resources. This allows for a basic hierarchical JSON document repository with IIIF extras, for clients that don't want to see the extra information or the flat version.

#### JSON-LD @context

When requested with the header, the API Storage Collection has an additional JSON-LD `@context`, that defines the additional terms needed by the API

```json
{
   "@context": [
       "http://tbc.org/iiif-repository/1/context.json",
       "http://iiif.io/api/presentation/3/context.json"
   ]
}
```

Without the header, the resource only has the regular IIIF Presentation 3 context:

```json
{
   "@context": "http://iiif.io/api/presentation/3/context.json"
}
```
{/* ^ This may not be true for born digital stuff - Wellcome RFC */}


#### IIIF behaviors

The API Storage Collection has one or two additional [behavior](https://iiif.io/api/presentation/3.0/#behavior) property values:

```json
{
   "behavior": [ "storage-collection", "public-iiif" ]
}
```

* The `storage-collection` behavior identifies the Collection as a Storage Collection rather than a regular IIIF Collection. This means you can only edit its `label` property (a language map), and its slug. You cannot edit the `items` property via HTTP operations on JSON, only by adding or deleting child Manifests or Collections with PUTs and POSTs. The `items` property is only ever generated by the server, you cannot supply it for a Storage Collection.
* the `public-iiif` behavior indicates that a public request for this resource will be served. If the Storage Collection does not have this behavior, it won't be visible to the public and its equivalent public URL will return HTTP 404. You may not wish for purely organisation containers in your IIIF repository to be available to the public as (potentially huge) IIIF Collections.
* If the Storage Collection has the `public-iiif` behavior, it also has a `seeAlso` property that links to the public IIIF Collection.

#### Navigation properties

The API Storage Collection has properties that govern the resource location in the hierarchy and therefore the public URL of the Collection (if using the default configuration):

```json
{
   "slug": "14th-century",
   "parent": "https://iiif.dlc.services/99/collections/g7hb5f4e",
   "publicId": "https://iiif.dlc.services/manuscripts/14th-century"
}
```

The hierarchical URL is composed of path elements provided by the resource `slug`, its parent's slug, and so on up to the root.

For Storage Collections, IIIF Collections and Manifests returned by the platform with Show-Extras:

* `parent` is always the flat form, not the hierarchical form.
* the `publicId` property shows what URL the public version of this resource is available on (it may be the same) which is also the value of `id` tha appears in that resource when viewed publicly.

For Storage Collections, IIIF Collections and Manifests supplied to the platform by POST and PUT:

* `parent` may be the hierarchical form or the flat form.
* the `publicId` is not settable, it is read-only. If supplied it will be ignored.

#### Paging

The API Storage Collection has `totalItems` and `view` properties, which work the same way as paging resources in the rest of the API (this is documented in [Hydra Collections](collections)). It also has a `totals` property which provides useful summary information about contained resources.

```json
{
   "totals": {
      "childStorageCollections": 4,
      "childIIIFCollections": 0,
      "childManifests": 0,
      "descendantStorageCollections": 12,
      "descendantIIIFCollections": 6,
      "descendantManifests": 3412
   },
   "totalItems": 4,
   "view": {
      "id": "https://iiif.dlc.services/99/collections/d44eeb7a?page=1&pageSize=2",
      "@type": "PartialCollectionView",
      "next": "https://iiif.dlc.services/99/collections/d44eeb7a?page=2&pageSize=2",
      "last": "https://iiif.dlc.services/99/collections/d44eeb7a?page=2&pageSize=2",
      "page": 1,
      "pageSize": 2,
      "totalPages": 2
  }
}
```

A normal IIIF Collection has no paging features - it is intended for human interaction as a single resource, so should not be arbitrarily large (i.e., it would be a poor user experience to have a 10,000 item IIIF Collection). But we need one for Storage Collections _on the API view_, to allow them to be used as containers and still ensure a good user experience in any interfaces we build.

>❓ Paging on IIIF Collections may make an appearance in IIIF 4.0; likely there'll be a proposal for this soon. If so we will adopt that paging mechanism.

#### Modification metadata

The API Storage Collection has `created`, `createdBy`, `modified` and `modifiedBy` properties:

```json
{
  "created": "2024-01-01T12:00:00",
  "modified": "2024-02-01T12:00:00",
  "createdBy": "https://api.dlc.services/users/tom",
  "modifiedBy": "https://api.dlc.services/users/tom",
}
```

>❓ Note that these are `api.` not `iiif.` as they are API users too. We don't have this idea yet.

#### seeAlso links

The API Storage Collection has one or two `seeAlso` links, that point at the canonical public equivalent collection (but only if the Storage Collection has the `public-iiif` behavior), and also at the hierarchical form of the API version:

```json
{  
  "seeAlso": [
    {
      "id": "https://iiif.dlc.services/99/manuscripts/14th-century",
      "type": "Collection",
      "label": { "en": ["14th Century Manuscripts"] },
      "profile": [ "public" ]
    },
    {
      "id": "https://iiif.dlc.services/99/manuscripts/14th-century",
      "type": "Collection",
      "label": { "en": ["14th Century Manuscripts"] },
      "profile": [ "api-hierarchical" ]
    }
  ]
}
```

>❓ These two are possible redundant given `id` and `publicId` but in some circumstances you may want to be more explicit. And also provide as plain IIIF. In the default configuration they will be the same.

### Public and API Storage Roots

If you haven't yet made any changes or additions to your IIIF Storage yet, the two _storage root_ endpoints will return responses like this:

Public:

```json
{
   "@context": "http://iiif.io/api/presentation/3/context.json",
   "id": "https://iiif.dlc.services/99/",
   "type": "Collection",
   "label": { "en": ["(repository root)"] },
   "items": []
}
```

With credentials and X-IIIF-CS-Show-Extras header:

```json
{
   "@context": [
       "http://tbc.org/iiif-repository/1/context.json",
       "http://iiif.io/api/presentation/3/context.json"
   ],
   "id": "https://iiif.dlc.services/99/collections/root",
   "publicId": "https://iiif.dlc.services/99",
   "type": "Collection",
   "behavior": [ "storage-collection", "public-iiif" ],
   "label": { "en": ["(repository root)"] },

   "slug": null,
   "parent": null,

   "items": [],   
   "totals": {
      "childStorageCollections": 0,
      "childIIIFCollections": 0,
      "childManifests": 0,
      "descendantStorageCollections": 0,
      "descendantIIIFCollections": 0,
      "descendantManifests": 0,
   },
   "totalItems": 0,
   "view": {
      "@id": "https://iiif.dlc.services/99/collections/root?page=1&pageSize=100",
      "@type": "PartialCollectionView",
      "page": 1,
      "pageSize": 100,
      "totalPages": 1
  },
  "seeAlso": [
    {
      "id": "https://iiif.dlc.services/99",
      "type": "Collection",
      "label": { "en": ["(repository root)"] },
      "profile": [ "public" ]
    },
    {
      "id": "https://api.dlc.services/customers/99/iiif",
      "type": "Collection",
      "label": { "en": ["(repository root)"] },
      "profile": [ "api-hierarchical" ]
    }
  ],
  "created": "2024-01-01T12:00:00",
  "modified": "2024-02-01T12:00:00",
  "createdBy": "https://api.dlc.services/users/tom",
  "modifiedBy": "https://api.dlc.services/users/tom",
}
```

The `null` value for `parent` and `slug` indicates that this is the root. Only this collection can have null values here. Even if you don't intend to use a hierarchical URL structure in your public IIIF URL scheme, you still need to provide values - they are used to organise your content in the Platform Portal (although there's nothing stopping you putting all your Manifests directly in the root Collection).


### Example: Create a Storage Collection

>❓(MOVE read the following afterwards)

>❓Consider the Manifest Editor client; doesn't care about internal identifiers, doesn't want to use flat canonical form, only interested in POSTing to containers. Parent is provided by POST target, slug is provided by ID, can't specify system ID, must be allocated. It never even knows about the "canonical" flat path, that's an internal identifier and all it sees is hierarchy. It's more like the [IIIF Repository](https://github.com/digirati-co-uk/iiif-manifest-editor/wiki/REST-Protocol) for CRKN ([POST expts](https://github.com/tomcrane/iiif-repository/blob/main/ProtocolTests/PostTests.cs), [PUT expts](https://github.com/tomcrane/iiif-repository/blob/main/ProtocolTests/PutTests.cs))

>❓For a Manifest Editor, the Manifests it is loading and saving and editing should probably be "normal" - not our extensions with their extra context. We want to feel like we are editing regular Manifests. The grey area is a Manifest Editor client that knows how to register assets for the user, understands the API for POSTing or PUTting an asset into a Manifest and using it. The portal page isn't this client because it's much more focused on the `paintedResources` array; a Manifest editor. The Manifest Editor can load and save WITHOUT using the X-IIIF-CS-Show-Extras header, and add assets to the Manifest "alongside" (see the RFC)

You can POST a Storage Collection into `iiif.dlc.services/<customer>` or you can PUT it to its Flat API ID `iiif.dlc.services/<customer>/collections/<identifier>`. The following two HTTP operations are equivalent. The body of the request is the same in both cases. You do not need to supply a `@context`. 

```
POST /99/collections
Host: https://iiif.dlc.services
```
```json
{
   "id": "https://iiif.dlc.services/99/collections/my-flat-identifier",
   "type": "Collection",
   "behavior": [ "storage-collection", "public-iiif" ],
   "label": { "en": ["My first Storage Collection"] },
   "slug": "my-first-storage-collection",
   "parent": "https://iiif.dlc.services/99/collections/root"
}
```
Returns `201 Created` with `Location` header

or

```
PUT /99/collections/my-flat-identifier
Host: https://api.dlc.services
```
```json
{
   "type": "Collection",
   "behavior": [ "storage-collection", "public-iiif" ],
   "label": { "en": ["My first Storage Collection"] },
   "slug": "my-first-storage-collection",
   "parent": "https://iiif.dlc.services/99/collections/root"
}
```

Returns `201 Created`

* The `id` is optional in the `PUT` request but if present, must have a path that matches the request URL. 
* The storage-collection behavior tells the platform that you are creating a Storage Collection and not a regular IIIF Collection content resource.
* There is no `items` property, and the request is invalid if one is present.
* The same operations can be used to update the Storage Collection, but if `my-flat-identifier` already exists the operations will fail unless accompanied by a valid ETag - see _Updates_ below.
* The canonical flat API URL is returned in a `Location` header.
* You must explicitly provide the `parent` property, and it can be **either** of the two variant forms of the parent resource - the flat URL or the hierarchical URL. The platform will resolve to the correct parent and "attach" the resource at the right point in the hierarchy.

Assuming the default configuration, either of the above two operations would later produce the following:

| Request | Response |
|---------|----------|
| GET /99/collections/my-flat-identifier<br/>X-IIIF-CS-Show-Extras: All | HTTP 200<br/>API Storage Collection |
| GET /99/my-first-storage-collection<br/>X-IIIF-CS-Show-Extras: All | HTTP 303 (?)<br/>Redirect to API Storage Collection |
| GET /99/collections/my-flat-identifier<br/>(no header) | HTTP 301<br/>Redirect to hierarchical Public view |
| GET /99/my-first-storage-collection<br/>(no header) | HTTP 200<br/>Public view of Storage Collection |


#### Allowing the platform to assign an identity

```
POST /99/collections/root
Host: https://iiif.dlc.services
```
```json
{
   "type": "Collection",
   "behavior": [ "storage-collection", "public-iiif" ],
   "label": { "en": ["My first Storage Collection"] },
   "slug": "my-first-storage-collection",
   "parent": "https://iiif.dlc.services/99/collections/root"
}
```

If your public IIIF resources default to the hierarchical scheme, you may not have any need to assign your own flat identifiers to the IIIF resources. An example of this might be a IIIF Manifest Editor, that only presents a mock folder-and-file model to users. In this scenario it may be incovenient to have to mint identifiers yourself.

The above POST will create a Storage Collection as the immediate child of the root, and will assign it an identity. The newly minted URL can be seen in the `Location` header returned from the POST request.

If all you have is the public hierarchical URL `/99/<path>` (e.g., if you didn't record the returned Location) you can always obtain the API canonical flat URL by requesting `/99/<path>` with the Show-Extras header and looking at the HTTP Location header on a redirect, or the `seeAlso` property of the eventual resturned resource.


### Example: PATCHing a Storage Collection

Here we are modifying the `label` of the Storage Collection, adding an additional value to the `label` property language map:

```
PATCH /99/collections/my-flat-identifier
Host: https://iiif.dlc.services
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
```
```json
{
   "label": { 
      "en": ["My first Storage Collection"],
      "it": ["La mia prima collezione di archiviazione"]
    }
}
```

As this an update of an existing resource, it must be accompanied by an ETag acquired on a previous GET. If the ETag doesn't match the latest GET the request will be rejected.

The PATCH operation returns the updated resource.

Other fields that may be patched:

| Property | Description |
|----------|-------------|
| `label`  | IIIF Label property - a JSON-LD language map |
| `slug`,<br/>`parent`   | Changing either of these will change the public URL of the Storage Collection, if the default hierarchical identifier is the canonical one.<br/> **It will also change the public URL of all child and descendant resources - Collections and Manifests - below this resource in the hierarchy.**<br/>This is how you _move_ a resource. |

### Example: Create a Storage Collection within a Storage Collection

This may be a PUT or POST, exactly as above, except that the `parent` is no longer the root collection. Here we are providing our own identifier, `.../zf567gbn`.

```
POST /99/collections
Host: https://iiif.dlc.services
```
```json
{
   "id": "https://iiif.dlc.services/99/collections/zf567gbn", 
   "type": "Collection",
   "behavior": [ "storage-collection", "public-iiif" ],
   "label": { "en": ["My Child Storage Collection"] },
   "slug": "my-child-storage-collection",
   "parent": "https://iiif.dlc.services/99/collections/my-flat-identifier"
}
```

or 

```
PUT /99/collections/zf567gbn
Host: https://iiif.dlc.services
```
```json
{
   "type": "Collection",
   "behavior": [ "storage-collection", "public-iiif" ],
   "label": { "en": ["My Child Storage Collection"] },
   "slug": "my-child-storage-collection",
   "parent": "https://iiif.dlc.services/99/collections/my-flat-identifier"
}
```

If you want the platform to assign an ID, you can only use POST, without the `id` field.

The API Storage Collection obtained after creating this child resource would look like this:

```
GET /99/collections/zf567gbn
Host: https://api.dlc.services
```
```json
{
   "@context": [
       "http://tbc.org/iiif-repository/1/context.json",
       "http://iiif.io/api/presentation/3/context.json"
   ],
   "id": "https://iiif.dlc.services/99/collections/zf567gbn",
   "publicId": "https://iiif.dlc.services/99/my-first-storage-collection/my-child-storage-collection",
   "type": "Collection",
   "behavior": [ "storage-collection", "public-iiif" ],
   "label": { "en": ["My Child Storage Collection"] },

   "slug": "my-child-storage-collection",
   "parent": "https://iiif.dlc.services/99/collections/my-flat-identifier",

   "items": [],
   "totals": {
      "childStorageCollections": 0,
      "childIIIFCollections": 0,
      "childManifests": 0,
      "descendantStorageCollections": 0,
      "descendantIIIFCollections": 0,
      "descendantManifests": 0,
   },
   "totalItems": 0,
   "view": {
      "@id": "https://iiif.dlc.services/99/collections/zf567gbn?page=1&pageSize=100",
      "@type": "PartialCollectionView",
      "page": 1,
      "pageSize": 100,
      "totalPages": 1
  },
  "seeAlso": [
    {
      "id": "https://iiif.dlc.services/99/my-first-storage-collection/my-child-storage-collection",
      "type": "Collection",
      "label": { "en": ["My Child Storage Collection"] },
      "profile": [ "public" ]
    },
    {
      "id": "https://iiif.dlc.services/99/my-first-storage-collection/my-child-storage-collection",
      "type": "Collection",
      "label": { "en": ["My Child Storage Collection"] },
      "profile": [ "api-hierarchical" ]
    }
  ],
  "created": "2024-01-01T12:00:00",
  "modified": "2024-02-01T12:00:00",
  "createdBy": "https://api.dlc.services/users/tom",
  "modifiedBy": "https://api.dlc.services/users/tom",
}
```

Given that we have now created a Storage Collection in the root, and another one inside the first one, we have some navigable IIIF on both our public and API endpoints:

```
GET /99
Host: https://iiif.dlc.services
```
```json
{
   "@context": "http://iiif.io/api/presentation/3/context.json",
   "id": "https://iiif.dlc.services/99",
   "type": "Collection",
   "label": { "en": ["(repository root)"] },
   "items": [
    {
      "id": "https://iiif.dlc.services/99/my-first-storage-collection",
      "type": "Collection",
      "label": { "en": ["My first Storage Collection"] }
    }
   ]
}
```

```
GET /99/my-first-storage-collection
Host: https://iiif.dlc.services
```
```json
{
   "@context": "http://iiif.io/api/presentation/3/context.json",
   "id": "https://iiif.dlc.services/99/my-first-storage-collection",
   "type": "Collection",
   "label": { "en": ["My first Storage Collection"] },
   "items": [
    {
      "id": "https://iiif.dlc.services/99/my-first-storage-collection/my-child-storage-collection",
      "type": "Collection",
      "label": { "en": ["My Child Storage Collection"] }
    }
   ],
   "partOf": [
      {
        "id": "https://iiif.dlc.services/99",
        "type": "Collection",
        "label": { "en": ["(repository root)"] }
      }    
   ]
}
```

```
GET /99/my-first-storage-collection/my-child-storage-collection
Host: https://iiif.dlc.services
```
```json
{
   "@context": "http://iiif.io/api/presentation/3/context.json",
   "id": "https://iiif.dlc.services/99/my-first-storage-collection/my-child-storage-collection",
   "type": "Collection",
   "label": { "en": ["My Child Storage Collection"] },
   "items": [],
   "partOf": [
      {
        "id": "https://iiif.dlc.services/99/my-first-storage-collection",
        "type": "Collection",
        "label": { "en": ["My first Storage Collection"] }
      }    
   ]
}
```

The `items` property provides the immediate children, and the `partOf` property provides a link to the immediate parent - neither direction goes more than one level.

For each of the three requests above, an request with the `X-IIIF-CS-Show-Extras` header would return the richer Storage Collection model described earlier, with additional properties, a `view` for paging, and links to the different public and API forms of the resource.


### General rules for Create and Update HTTP request bodies

We have five variables:

 - The request verb could be PUT, POST or PATCH
 - The request URL may be the flat form, or the hierarchical form
 - The `parent` (if supplied) may be the flat form, or the hierarchical form 
 - The `id` (if supplied) of the request body may be the flat form, or the hierarchical form 
 - The `slug` only effects the hierarchical URL
 - The `publicId`, which can be used to determine the `slug` and `parent` (e.g. `"https://iiif.dlc.services/99/my-storage/my-manifest"` is shorthand equivalent of `{"slug":"my-manifest",`"parent":"https://iiif.dlc.services/99/my-storage"`}` )

 Any combination of these variables can be used to create or update content, as long as:

 - there is enough information to create/edit the resource
 - none of the information contradicts itself.

For example:

 - The slug must agree with `id`, if `id` is present and hierarchical
 - The slug must agree with PUT target, if PUT target is hierarchical

The flat identifier will be assigned by the platform for create operations, unless either of these are true:

 - It's a PUT to a flat URL
 - The request body `id` is the flat URL      

If both of these are true, they must be the same. As an example of how these rules combine, if both of those were true, the hierarchical URL must be specified by `parent` (hierarchical value) and `slug`. Whereas a PUT to the hierarchical URL with the `id` of the body having the an explicit flat `id` value would allow you to set both the hierarchical URL and the flat identifier without using either `parent` or `slug`.



### Example: Create a IIIF Collection within a Storage Collection

So far the examples have been Storage Collections - containers to organise content. But we can also create IIIF Collections, too.

In advance of introducing IIIF Manifests managed by the platform, we'll add a IIIF Collection that references external IIIF Manifests - so essentially a JSON document with no platform dependencies.

We'll use this Collection, which references two Manifests:

[https://iiif.wellcomecollection.org/presentation/b29000798](https://iiif.wellcomecollection.org/presentation/b29000798)

We won't reproduce the full JSON payload here - but inspecting it reveals use of properties such as `homepage`, `metadata`, `provider`, `thumbnail` and other IIIF properties. All this is supported in a IIIF Collection but not a Storage Collection, as it it standard IIIF - but we will need to change the `id` if a POST, or use a different one and remove the `id` from the payload if a PUT:

```
PUT /99/collections/wellcome-b29000798
Host: https://iiif.dlc.services
```
```jsonc
{
   // body of IIIF Collection, without the id property, and with the mandatory parent and slug:
   //..
   "parent": "https://iiif.dlc.services/99/collections/my-flat-identifier",
   "slug": "b29000798", 
   //..
}
```

or

```
POST /99/my-first-storage-collection
Host: https://iiif.dlc.services
```
```jsonc
{
  // This is "PURE" IIIF, I've just changed the `id` to suit its new home
  "id": "https://iiif.dlc.services/99/my-first-storage-collection/b29000798",
  // The rest of the Collection as-is...
}
```

or

```
PUT /99/my-first-storage-collection/b29000798
Host: https://iiif.dlc.services
```
```jsonc
{
  // This is "PURE" IIIF, and the `id` must match if supplied
  "id": "https://iiif.dlc.services/99/my-first-storage-collection/b29000798",
  // The rest of the Collection as-is...
}
```

or

```
PUT /99/my-first-storage-collection/b29000798
Host: https://iiif.dlc.services
```
```jsonc
{
  // This is "PURE" IIIF, just without any `id`
  //
  // The rest of the Collection as-is...
}
```


This IIIF Collection is now available for public use on `https://iiif.dlc.services/99/my-first-storage-collection/b29000798`. This looks the same as Wellcome's original apart from the `id`. 

Only the first of the above had an internal (flat) identifier that we supplied ourselves. You would have to find out what flat `id` was minted by examining the Location header returned at creation time, or asking for the hierarchical path (always known in the above) and seeing what the redirected `id` is.

If you requested the extended form with the header on `https://iiif.dlc.services/99/collections/wellcome-b29000798`, it would look the same, except that it has the same additional `@context` as the API Storage Collections, and the same additional properties as the Storage Collection (`parent`, `slug`, `publicId`, `created`, `createdBy`, `modified`, `modifiedBy`), as well as the `seeAlso` links to other forms. It does **not** have the `view` and `totalItems` properties - only Storage Collections can be paged. However, it does have the `totals` property for information.

If you now requested the _parent_ of this IIIF Collection on the public URL, it would look like this:

```
GET /99/my-first-storage-collection
Host: https://iiif.dlc.services
```
```json
{
   "@context": "http://iiif.io/api/presentation/3/context.json",
   "id": "https://iiif.dlc.services/99/my-first-storage-collection",
   "type": "Collection",
   "label": { "en": ["My first Storage Collection"] },
   "items": [
    {
      "id": "https://iiif.dlc.services/99/my-first-storage-collection/b29000798",
      "type": "Collection",
      "label": { "en": ["Life, letters and journals of Sir Charles Lyell, bart / edited by his sister-in-law, Mrs. Lyell."] }
    },
    {
      "id": "https://iiif.dlc.services/99/my-first-storage-collection/my-child-storage-collection",
      "type": "Collection",
      "label": { "en": ["My Child Storage Collection"] }
    }
   ],
   "partOf": [
      {
        "id": "https://iiif.dlc.services/99",
        "type": "Collection",
        "label": { "en": ["(repository root)"] }
      }    
   ]
}
```

The default ordering of items within a storage collection is by their `slug` value.

>❓Later we will look at ways of ordering items in Storage Collections. This is analogous to ordering directory listings in a file system, and is different from ordering of items within a IIIF Collection, which can only have one explicit ordering.


### Recap - Collections

* The Platform knows about your Storage Collections as Containers
* The Platform knows about their hierarchical relationships
* The Platform knows that one of the Storage Collections contains a IIIF Collection
* The Platform stores and manages the complete IIIF JSON for the latter, and you can put any valid IIIF in, including links to external Manifests and Content Resources.
* All of these resources are available via both flat and hierarchical URIs, with the flat API version being the canonical form for CRUD operations, and the hierarchical form the public default (unless you change that behaviour).

## IIIF Collections - Containment vs Content

TODO: Work in containment behaviour example here.

Allow new additions to container to append to `items`




### Configuration - default URLs for public URLs
 
The endpoint `https://iiif.dlc.services/99/configuration` returns the following resource, which you can patch to change behaviour:

```json
{
  "id": "https://iiif.dlc.services/99/configuration",
  "@type": "IIIFConfiguration",
  "publicUriStructure": "hierarchical",
  "defaultStorageCollectionBehavior": "public-iiif",
  "publicStorageCollectionMaxItems": 500,
  "paintingAssetThumbnailSize": "!100,100",
  "imageServices": [ "ImageService3" ]
}
```

| Property | Description |
|----------|-------------|
| `publicUriStructure` | `"flat"` (default) or `"hierachical"`<br/>Defines which is the canonical form for public IIIF resources; the other form will redirect. |
| `defaultStorageCollectionBehavior` | `"public-iiif"` (default) or `null`<br/>Whether Storage Collections are public by default (do we need this? - you have to specify on create anyway) |
| `publicStorageCollectionMaxItems` | Public IIIF representations of storage collections do not have paging, so we can't let the JSON responses be arbitrarily large. Only the first 500 items will be returned by default. This can be set lower but not higher. |
| `paintingAssetThumbnailSize` | A IIIF Size parameter that specifies how large the `thumbnail` on `PaintedResource::canvasPainting` is (see below). You should only change this if building your own admin UI and require a larger thumbnail in it. If you do change it, you MUST have a deliveryChannelPolicy for thumbs that includes this size exactly. |
| `imageServices` | For image assets, which version(s) of the Image API to emit into generated Manifests. For both 2 and 3, you would set `[ "ImageService3", "ImageService2" ]`. The order determines the order they appear in the Manifest. |


### Example: store an arbitrary Manifest

So far we have only dealt with Collections managed by the platform. The previous IIIF Collection referenced two external Manifests, but the platform doesn't know anything about them.

We can do the same for a Manifest referencing external content resources. For example:

`https://iiif.wellcomecollection.org/presentation/b28831299`

This time with a POST for variety:

```
POST /99/manifests
Host: https://iiif.dlc.services
```
```jsonc
{
   "id": "https://iiif.dlc.services/99/manifests/wellcome-b28831299",

   // body of IIIF Manifest, with the additional mandatory parent and slug:
   //..
   "parent": "https://iiif.dlc.services/99/collections/my-flat-identifier",
   "slug": "b28831299"
   //..
}
```

We have still specified our own flat identifier even though we created the resource with a POST rather than a PUT.

As well as the two extra properties above, the API view of this Manifest also has the `created`, `createdBy`, `modified`, `modifiedBy` properties, as well as the `seeAlso` links to other forms. It does **not** have the `view`, `totals` and `totalItems` properties. Only Storage Collections can be paged.

It also has two extra direct properties:

```jsonc
{
  "ingesting": null,
  "paintedResources": [{}, {}] // details omitted for now
}
```

With the IIIF Collection introduced earlier, the referenced Manifests are external and the platform doesn't track them or know anything about them, they are just part of the JSON payload. The platform is acting as a JSON document store. If however the Manifests had been managed by the platform (the platform can recognise its own URLs for linked resources, even if they are rewritten), then it would keep track of the containment (parent/child) relationship between the Collection and its Manifests. We will see this shortly.

The situation is different for Content Resources linked to IIIF Canvases through `painting` annotations. The platform keeps track of all content resources linked this way, **whether they are derived from its own assets or not**. This tracking becomes apparent if you start adding your own assets, described shortly.

## Assets in Manifest

The combination of Storage Collections, IIIF Collections and storing arbitrary Manifests gives you a full IIIF Repository that you could integrate with a Manifest Editor or digital production workflow.

Use of the hierachical paths only, with PUT and POST operations to create a hierarchical document store, provides a relatively simple HTTP storage protocol for IIIF. 

> ❓ Compare with [CRKN prototype](https://github.com/tomcrane/iiif-repository/blob/main/ProtocolTests/PutTests.cs#L95)

However, we are not dealing with two crucial points:

* People have assets (images most commonly but could be anything) and they want to turn them into a Manifest
* We have a platform that has rich APIs and processes for handling assets at scale

It could also be used to store Manifests that reference the platform's own assets, treating them no different from external content resources. But it has a much more powerful feature, which is _understanding an asset in the context of a Manifest_ - using the Manifest as a _container_ of assets, adding assets to Manifests or specifiying through API the assets that are used indirectly as the content resources of the Manifest. The purpose of this is to be able to construct Manifests quickly from sequences of assets, without manually building the canvases, annotation pages and painting annotations.

* A common scenario is to have a sequence of images; you want to turn that sequence into a Manifest. The only piece of data you want to add for each image is a label. You also have label and metadata for the Manifest itself. It should be trivial to go from that sequence of images on your desktop, or in DropBox, to a published IIIF Manifest.  (Later you might want to add OCR, HTR, annotations and more to each Canvas - that will be covered in _adjuncts_).

## PaintedResource

A `PaintedResource` represents, in a compact non-IIIF form, the relationship between a Content Resource and a Manifest. If the Content Resource is an Asset managed by the platform, this asset is part of the PaintedResource.  It has two fields:

```json
{
  "id": "https://iiif.dcl.services/paintedResources/t454knmf/ae4b77wd/0/0",
  "type": "PaintedResource",
  "canvasPainting": {  
  },
  "asset": {
  },
  "reingest": true
}
```

### canvasPainting

This field is **always** present, whether the content resource is an asset managed by the platform or not. 

```json
{
  "id": "https://iiif.dcl.services/paintedResources/t454knmf/ae4b77wd/0/0",
  "type": "PaintedResource",
  "canvasPainting": {  
    "canvasId": "https://iiif.dlc.services/99/canvases/ae4b77wd",
    "canvasOriginalId": null,
    "canvasOrder": 0,
    "choiceOrder": null,
    "thumbnail": null,
    "label": null,
    "canvasLabel": { "en": [ "Canvas 1" ] },
    "target": null,
    "staticWidth": 1200,
    "staticHeight": 1885 
  },
  "asset": {   
    // see later
  }
}
```

| Field                 | Description   |
| --------------------- | ------------- |
| `canvasId`            | The IIIF Canvas `id` in the Manifest the asset is painted on. The platform automatically assigns Canvas identifiers when you register paintedResources; they are always of the form shown in the example above (i.e., flat). If you provide the `canvasId` property yourself, it must match this form of flat identifier, and must not be the `id` of a Canvas used in another Manifest (see note below for how to have the same public `id` values for Canvases in different Manifests). This URI is dereferenceable; the platform will return a standalone Canvas with a `partOf` link to the Manifest. |
| `canvasOriginalId`    | In the Wellcome example above the Canvas arrived in an existing Manifest, with existing external Canvas URIs. These existing URIs are not modified by the platform in the Manifest JSON (a Manifest is stored unaltered) but a record is kept here to match the external URI to the internal URI for the Canvas. This value may also be of the API form, where you want canvases in different Manifests to have the same public `id`.  This URI is also dereferenceable _only when of this form_; the platform will return a standalone Canvas with `partOf` link(s) to the Manifest this `id` appears in.  |
| `canvasOrder`         | This value is a `painting` order across the whole Manifest, and is used to derive Canvas sequence order within a Manifest. This value keeps incrementing for successive paintings on the same Canvas. It is always >= number of canvases in the Manifest. For most manifests, the number of canvases equals the number of assets equales the highest value of canvasOrder. **It stays the same** for successive content resources within a Choice (see choice_order). It gets recalculated on a Manifest save by walking through the manifest.items, incrementing as we go.  The index within `manifest.items` of the Canvas that the content resource is on. |
| `choiceOrder`         | Normally null; a positive integer (not zero) indicates that the asset is part of a [Choice](https://iiif.io/api/cookbook/recipe/0033-choice/) body. Multiple choice bodies share same value of order. When the successive content resources are items in a `Choice` body, `canvasOrder` holds constant and `choiceOrder` increments. The combination of these two fields also allows for multiple choice bodies on the same Canvas each with their own assets. It is a Bad Request to supply an explicit `choiceOrder` of 0, to avoid accidentally implying a choice because an integer is at its default value. It must either be omitted, or null, or positive.|
| `thumbnail`             | This is filled in automatically when the content resource is an asset managed by the platform, and when the content resource is external, the platform will attempt to find a good value for it from the imported Manifest. It's not a IIIF `thumbnail` resource, it's a single URI pointing to a single image resource. It's for use in admin interfaces like the IIIF-CS portal, rather than public facing applications like a viewer which should use the regular IIIF. It's not visible in the public view, because `paintedResources` is not visible. Usually that "single image resource" is a request to the asset's IIIF Image API thumbnail endpoint. The size of the image, for managed assets, is determined by the value of `paintingAssetThumbnailSize` in the configuration data mentioned earlier. A typical value might be `https://dlc.services/thumbs/99/my-image/full/!100,100/0/default.jpg`. |
| `label`                 | Stored JSON-LD language map - the label for the _Resource_. Most of the time this will be used as the `label` for the Canvas. For Content Resources that make up a `Choice`, or for multiple content resources on the same Canvas, each may have a different `label`. The first value of this will be used as the label on the Canvas, unless `canvasLabel` is explicitly set. |
| `canvasLabel`           | JSON-LD language map to use on the canvas specified by `canvasId`, to override the value that would be chosen from available `label` fields. There may be many `PaintedResource` with the same Manifest; if more than one for the same Canvas has a `canvasLabel`, the first in Canvas order will be used. (remember that this is two-way, see note below) |
| `target`                | Is null when the whole Canvas is the target, otherwise a parseable IIIF selector (fragment or JSON). For assets making up a Choice, the first non-null value will be assumed to be the target of the Choice annotation. |
| `staticWidth`           | For images, the width of the image in the Manifest for which the IIIF API is a service. This and static_height next two default to 0 in which case the largest thumbnail size is used - which may be a secret thumbnail. See **Special Treatment of Images with Image Services** below. |
| `staticHeight`         | For images, the height of the image in the Manifest for which the IIIF API is a service. |

#### A note about Canvas `id` values

All canvases in saved Manifests have an internal ID of the form `/<customer-id>/canvases/<identifier>`. This is always the `id` of the Canvas in the API representation when requested with the `X-IIIF-CS-Show-Extras` header. If the Manifest is newly created in the platform and the canvases have been created by ingesting assets into the manifest via `paintedResources`, then these `id` values are also the `id` values  of the canvases in the publicly visible Manifest.

Where a Manifest has been saved with existing Canvas `id` values (e.g., JSON imported from an existing third party manifest), these existing values are retained in the publicly visible Manifest, and the API version's canvases have `publicId` fields showing these values. The `canvasOriginalId` property also shows these values. 

##### Examples

The user has POSTed Manifest JSON with Canvas `id` values already:

API/Flat Manifest:

```json
{
  "id": "https://iiif.dlc.services/99/canvases/abc123",
  "type": "Canvas",
  "publicId": "https://iiif.wellcomecollection.org/presentation/b30273249/canvases/b30273249_0001.jp2"
}
```

Hierarchical (public) Manifest:

```json
{
  "id": "https://iiif.wellcomecollection.org/presentation/b30273249/canvases/b30273249_0001.jp2",
  "type": "Canvas"
}
```

The user has not supplied any canvas `id` values:

API/Flat Manifest:

```json
{
  "id": "https://iiif.dlc.services/99/canvases/abc987",
  "type": "Canvas",
  "publicId": "https://iiif.dlc.services/99/canvases/abc987"
}
```
(note that the two identical values are explicitly asserted).

Hierarchical (public) Manifest:

```json
{
  "id": "https://iiif.dlc.services/99/canvases/abc987",
  "type": "Canvas"
}
``` 

The _internal_ Canvas ID form is always in the context of a particular Manifest. Two canvases in different stored Manifests cannot have the same _internal_ id. But using `canvasOriginalId`, any number of Manifests can feature canvases with the same public `id` property. A variant of this scenario is where a Manifest originally created by the platform is saved back as a new Manifest.

API/Flat Manifest:

```json
{
  "id": "https://iiif.dlc.services/99/canvases/def874",
  "type": "Canvas",
  "publicId": "https://iiif.dlc.services/99/canvases/xyz731"
}
```

Both are of the internal form, and the `canvasPainting` would look like this:

```json
"canvasPainting": {  
  // ...
  "canvasId": "https://iiif.dlc.services/99/canvases/def874",
  "canvasOriginalId":"https://iiif.dlc.services/99/canvases/xyz731",
  // ...
}
```


Hierarchical (public) Manifest:

```json
{
  "id": "https://iiif.dlc.services/99/canvases/xyz731",
  "type": "Canvas"
}
```

> ❓See the UI demo and the manifest behind it for an example of how the `canvasPainting` is used to generate a Manifest, and then UI from the Manifest. When looking at that remember that the journey is two-way - this resource is derived from IIIF and is a summary of it, in scenarios where the IIIF is created and then imported, or is being further edited. But you can also create a manifest _from_ this data, without having to construct the actual IIIF representation, as seen later.

### asset 

This field is **only** present when the Content Resource is a IIIF-CS-managed [Asset](asset).

```json
{
  "id": "https://iiif.dcl.services/paintedResources/t454knmf/ae4b77wd/0/0",
  "type": "PaintedResource",
  "canvasPainting": {  
    // see above
  },
  "asset": {
    "@id": "https://api.dlc.services/customers/99/spaces/76/MS_125_001",
    "@type": "vocab:Image",
    "customer": 99,
    "space": 76,
    "origin": "s3://some-bucket/...(could be any valid origin).../MS_125_001.tiff",
    "contentType": "image/tiff",
    "width": 6000,
    "height": 9000,
    "deliveryChannels": [
      {
        "@type": "vocab:DeliveryChannel",
        "channel": "iiif-img",
        "policy": "use-original"
      },
      {
        "@type": "vocab:DeliveryChannel",
        "channel": "thumbs",
        "policy": "https://api.dlc.services/customers/99/deliveryChannelPolicies/thumbs/standard"
      }
    ],
    "...": "...(other asset fields from IIIF-Cloud-Services)",   
  }
}
```

When a Manifest is requested with the X-IIIF-CS-Show-Extras header:

* Each resource that is the body of a painting annotation, or a member of a Choice body, will include a _reference_ to the corresponding `PaintedResource`
* The full `PaintedResource` is included in the Manifest's extra `paintedResources` property. 

Example:

```json
{
   "@context": [
       "http://tbc.org/iiif-repository/1/context.json",
       "http://iiif.io/api/presentation/3/context.json"
   ],
  "id": "https://iiif.dlc.services/99/manifests/t454knmf",
  "publicId": "https://iiif.dlc.services/99/manuscripts/14th-century/ms-125",
  "type": "Manifest",
  //
  "items": [
    {
      "id": "https://iiif.dlc.services/99/canvases/ae4b77wd",
      "type": "Canvas",
      "items": [
        {
          "id": "...",
          "type": "AnnotationPage",
          "items": [
            {
              "id": "...",
              "type": "Annotation",
              "motivation": "painting",
              "body": {
                "id": "https://dlc.services/iiif-img/99/76/MS_125_001/full/1200,/0/default.jpg",
                "type": "Image",
                "format": "image/jpeg",
                "width": 1200,
                "height": 1885,
                "service": [
                  {
                    "id": "https://dlc.services/iiif-img/99/76/MS_125_001",
                    "type": "ImageService3",
                    "profile": "level2"
                  }
                ],
                "paintedResource": {
                  "id": "https://iiif.dlc.services/99/paintedResources/t454knmf/ae4b77wd/0/0",
                  "type": "PaintedResource"
                }
              },
              "target": "https://iiif.dlc.services/99/canvases/ae4b77wd"
            }
          ]
        }
      ],
      "thumbnail": [
        {"...": "..."}
      ]
    }
  ],
  "paintedResources": [
    {
      "id": "https://iiif.dlc.services/99/paintedResources/t454knmf/ae4b77wd/0/0",
      "type": "PaintedResource",
      "canvasPainting": {
        "canvasId": "https://iiif.dlc.services/99/canvases/ae4b77wd",
        "canvasOriginalId": null,
        "canvasOrder": 0,
        "choiceOrder": null,
        "thumbnail": null,
        "label": null,
        "canvasLabel": { "en": [ "Canvas 1" ] },
        "target": null,
        "staticWidth": 1200,
        "staticHeight": 1885    
      },
      "asset": {
        "@id": "https://api.dlc.services/customers/99/spaces/76/MS_125_001",
        "@type": "vocab:Image",
        "customer": 2,
        "space": 76,
        "origin": "s3://some-bucket/...(could be any valid origin).../MS_125_001.tiff",
        "contentType": "image/tiff",
        "width": 6000,
        "height": 9000,
        "deliveryChannels": [
          {
            "@type": "vocab:DeliveryChannel",
            "channel": "iiif-img",
            "policy": "use-original"
          },
          {
            "@type": "vocab:DeliveryChannel",
            "channel": "thumbs",
            "policy": "https://api.dlc.services/customers/99/deliveryChannelPolicies/thumbs/standard"
          }
        ],
        "...": "...(other asset fields from IIIF-Cloud-Services)",                        
      }
    }
  ],
  "assets": "https://iiif.dlc.services/99/manifests/t454knmf/assets",
  "queue": "https://iiif.dlc.services/99/manifests/t454knmf/queue"
}
```


A Manifest's `paintedResources` list can be used to add assets to a Manifest directly, with the additional fields in `canvasPainting` that determine how the asset is "painted". It can be used to add previously registered assets, and to register assets for the first time. The same asset can be referenced more than once in the `paintedResources` list. Each manifest also has a [Queue](queue) for asynchronous processing of assets.

### Reingest

This field is **optional** and only relevant when the Content Resource is a IIIF-CS-managed Asset. 

By default an Asset specified via the `"asset"` property will be ingested by IIIF-CS if it is new (ie the IIIF-CS instance doesn't know about it). In all other instances it is assumed to be usable as-is, without additional processing, as the `"asset"` property is a conveniance mechanism for generating manifests.

If the consumer is aware that the `"asset"` should be reprocessed then it can override the default behaviour by specifying `"reingest": true`.

### Special Treatment of Images with Image Services

Almost always, when a IIIF Image API endpoint is available, the Image content resource painted onto the Canvas that has that image service is itself a parameterised request to the image service, rather than some other image. This is reflected in the example above. The `paintedResource` reference is on the annotation body, not on the image service on the body. But this leaves something undecided - how big should the image painted onto the canvas be? This is set with the `staticHeight` and `staticWidth` properties.


### Assets property

The example Manifest above also includes an `assets` property, a link to a Hydra Collection. This works exactly like [space.images](space#images). Very often, the assets in that collection (the assets "in" the Manifest) are the same as the assets shown in `paintedResources` (the assets "on" the Canvases of the Manifest). But not always! You can add assets to the Manifest - to this collection - for later use.


#### Assets and Spaces

This `assets` property works exactly like [space.images](space#images) because it is in fact an alias for a [Space](space). If you ingest assets via `paintedResources`, and don't explicitly specify a Space, they end up in a Space that is created on demand for the Manifest. Not all Manifests have a Space; if it has no ingested assets of its own, it does not need one. But as soon as it is needed it will be created, and appear in the `space` property of the Manifest (visible only with the `X-IIIF-CS-Show-Extras` header). Here, Space 87341 has been created for this Manifest and can be used like any other Space via the [Space](space) API, including adding assets to the Space independently. This allows the Space to be used as a "working area" for the Manifest - you don't have to use all the assets in the Space in the manifest, and the Manifest can reference assets in other spaces or external to the platform. 

```json
{
   "@context": [
       "http://tbc.org/iiif-repository/1/context.json",
       "http://iiif.io/api/presentation/3/context.json"
   ],
  "id": "https://iiif.dlc.services/99/manifests/t454knmf",
  "publicId": "https://iiif.dlc.services/99/manuscripts/14th-century/ms-125",
  "type": "Manifest",
  //
  "space": "https://api.dlc.services/customers/99/spaces/87341",
  // 
  "items": [
    // ...
  ],
  "paintedResources": [
    // ...
  ],
  "assets": "https://iiif.dlc.services/99/manifests/t454knmf/assets",
  "queue": "https://iiif.dlc.services/99/manifests/t454knmf/queue"
}
```

In this example,

```
"space": "https://api.dlc.services/customers/99/spaces/87341"
```

is an alias for 

```
  "assets": "https://iiif.dlc.services/99/manifests/t454knmf/assets"
```

...the two URIs will show the same set of assets when followed and behave with identical Space semantics.

Although the Space is created on-demand when assets are registered via the Manifest's `queue`, or by POSTing to `assets`, or via `paintedResources`, you might wish to create the Space beforehand. This is done by sending an additional HTTP Header, either:

 - When creating the Manifest via a POST to the `/99/manifests` API endpoint:

```
POST /99/manifests
Host: https://iiif.dlc.Services
Link: <https://dlcs.io/vocab#Space>;rel="DCTERMS.requires"
```
```json
{
   // manifest body
}
```

 - When creating the Manifest via a PUT to its intended flat identifier:

 ```
PUT /99/manifests/my-identifier
Host: https://iiif.dlc.Services
Link: <https://dlcs.io/vocab#Space>;rel="DCTERMS.requires"
```
```json
{
   // manifest body
}
```

 - Later, by a POST with an empty body to the Manifest's flat URL:

```
POST /99/manifests/hy64fgbdeth765
Host: https://iiif.dlc.Services
Link: <https://dlcs.io/vocab#Space>;rel="DCTERMS.requires"
```

In the first two examples, the `space` property of the Manifest has a value immediately, with a newly created Space.

In the third example, assuming the Manifest did not already have a Space, the Space value is immediately available on the next GET request for the Manifest.

If a Manifest has a Space already, this operation does nothing. It is also impossible to remove a Manifest's space by this mechanism.



### Queue property

Assets, or collections of assets, can be POSTed to the manifests's queue just as they can to the platform API queue. Assets ingested via `paintedResources` are reflected in this queue too. Assets on this queue go into the underlying Space surfaced in the Assets property, but do not get used on Canvases in the manifest - that needs to be done manually.


## API Operations

### Example: Create an empty Manifest

Manifests must exist within a Collection - which can be a Storage Collection (even the repository root) or a IIIF Collection.

```
PUT /99/manifests/demo-1
Host: https://iiif.dlc.Services
```
```json
{
  "type": "Manifest",
  "label": { "en": [ "Demo Manifest"] },
  "parent": "https://iiif.dlc.services/99/collections/my-flat-identifier",
  "slug": "demo-manifest"
}
```

This will be immediately available to the public, but has no canvases yet. We could add canvases by PUTting it again with `items` JSON referencing content resources - either platform or external. But there is a shortcut, and we can construct the canvases automatically in several ways beyond constructing all the IIIF manually:

* POST `PaintedResource` objects one by one to the URI `../paintedResources`
* POST a Hydra Collection of `PaintedResource` to `../paintedResources` (it will behave like a [Queue](queues)).
* PUT the Manifest with a populated `paintedResources` list. If the assets included are already known to the platform, they will be used; if they are new to the platform, they will be ingested and added to the Manifest's `assets`.
* Add assets to the platform via the `../assets` URI on the Manifest (they will be added behind the scenes to a Space dedicated just to this Manifest), and then later in a separate operation reference those assets in a new PUT of the Manifest with additional `paintedResources` or valid IIIF.


>❓https://deploy-preview-2--dlcs-docs.netlify.app/manifest-view.html is an experiment to verify that tabular data like the above can be expressed first as a manifest (https://deploy-preview-2--dlcs-docs.netlify.app/manifest-builder/ms125_full-example.json) and then as a tabular HTML representation in the demo. Note the `paintedResources` property in that example.

Given the above definition of `PaintedResource`, we can now add an asset to our currently empty Manifest, _and create the Canvas IIIF at the same time_. This is the minimal payload, just as it is for a regular [Asset](registering-assets#http-post):

```
POST /99/manifests/demo-1/paintedResources
Host: https://iiif.dlc.services
```
```json
{
  "asset": 
  {
    "id": "my-image.tiff",
    "mediaType": "image/tiff",
    "origin": "https://example.org/images/my-image.tiff"
  }
}
```

Assume that the tiff image at `https://example.org/images/my-image.tiff` is 6000 pixels wide by 3000 pixels high. We don't specify this on ingest, the platform will measure it. These figures are chosen to make the various figures below more obvious.

>❓What is returned in this POST?

If you omit the additional `canvasPainting` object and just POST a regular asset in here, the platform will assume that it is a new Canvas (and will mint an ID), and that it is a simple Canvas where the asset targets the whole Canvas. The Platform will set canvas_order, thumbnail, label etc, appending it to the Canvas list.

If we _immediately_ request the Manifest, it will return with `ingesting` indicating that some assets are still processing, and it will include one entry in its `paintedResources` list where the `ingesting` property of the `asset` is also `true`. **Later** (and this my be a second or less) the API Manifest will look like this:

```
GET /99/manifests/demo-1
Host: https://iiif.dlc.services
```
```json
{
  "@context": [
       "http://tbc.org/iiif-repository/1/context.json",
       "http://iiif.io/api/presentation/3/context.json"
  ],
  "id": "https://iiif.dlc.services/99/manifests/demo-1",
  "type": "Manifest",
  "label": { "en": [ "Demo Manifest"] },
  "parent": "https://iiif.dlc.services/99/collections/my-flat-identifier",
  "slug": "demo-manifest",
  "ingesting": {
    "finished": 1,
    "total": 1    
  },
  "space": "https://api.dlc.services/customers/99/spaces/5498",
  "items": [
    {
      "id": "https://iiif.dlc.services/99/canvases/7tgbn3wa",
      "type": "Canvas",
      "items": [
        {
          "id": "https://iiif.dlc.services/99/canvases/7tgbn3wa/painting",
          "type": "AnnotationPage",
          "items": [
            {
              "id": "https://iiif.dlc.services/99/canvases/7tgbn3wa/painting/0/n",
              "type": "Annotation",
              "motivation": [ "painting" ],
              "body": {
                "id": "https://dlc.services/iiif-img/99/5498/my-image.tiff/full/2000,1000/0/default.jpg",
                "type": "Image",
                "width": 2000,
                "height": 1000,
                "format": "image/jpeg",
                "service": [
                  {
                    "id": "https://dlc.services/iiif-img/99/5498/my-image.tiff",
                    "type": "ImageService3",
                    "profile": "level2",
                    "width": 6000,
                    "height": 3000
                  }
                ],
                "paintedResource": {
                  "id": "https://iiif.dlc.services/99/paintedResources/demo-1/7tgbn3wa/0/0",
                  "type": "PaintedResource"
                }
              },
              "target": "https://iiif.dlc.services/99/canvases/7tgbn3wa"
            }
          ]
        }
      ],
      "thumbnail": [
        {
          "id": "https://dlc.services/thumbs/99/5498/my-image.tiff/full/100,50/0/default.jpg",
          "type": "Image",
          "width": 100,
          "height": 50,
          "format": "image/jpeg",
          "service": [
            {
              "id": "https://dlc.services/thumbs/99/5498/my-image.tiff",
              "type": "ImageService3",
              "profile": "level0",
              "width": 2000,
              "height": 1000,
              "sizes": [
                { "width": 100, "height": 50 },
                { "width": 200, "height": 100 },
                { "width": 400, "height": 20 },
                { "width": 1000, "height": 500 },
                { "width": 1000, "height": 1000 }
              ]
            }
          ]
        }
      ]
    }
  ],
  "paintedResources": [
    {
      "id": "https://iiif.dlc.services/99/paintedResources/demo-1/7tgbn3wa/0/0",
      "type": "PaintedResource",
      "canvasPainting": {
        "canvasId": "https://iiif.dlc.services/99/canvases/7tgbn3wa",
        "canvasOrder": 0,
        "choiceOrder": null,
        "thumbnail": "https://dlc.services/thumbs/99/5498/my-image.tiff/full/100,50/0/default.jpg",
        "label": null,
        "canvasLabel": null,
        "target": null,
        "staticWidth": 2000,
        "staticHeight": 1000
      },
      "asset": {
        "id": "https://api.dlc.services/customers/99/spaces/5498/images/my-image.tiff",
        "mediaType": "image/tiff",
        "space": 5498,    
        "origin": "https://example.org/images/my-image.tiff",
        "created": "2024-05-23T09:56:39.0649160Z",
        "batch": null,
        "ingesting": false,
        "finished": "2024-05-23T09:56:40.0649160Z",
        "error": "",    
        "duration": 0,
        "width": 6000,
        "height": 3000,    
        "deliveryChannels": [
          {
            "@type": "vocab:DeliveryChannel",
            "channel": "iiif-img",
            "policy": "default"
          },
          {
            "@type": "vocab:DeliveryChannel",
            "channel": "thumbnail",
            "policy": "https://api.dlcs.io/customers/99/deliveryChannelPolicies/thumbnail/standard"
          },
          {
            "@type": "vocab:DeliveryChannel",
            "channel": "file",
            "policy": "none"
          }
        ],      
        "manifest": "https://dlc.services/iiif-manifest/99/5498/my-image.tiff",    
        "roles": [],
        "maxWidth": 0,
        "openFullMax": 0,
        "openMaxWidth": 0,    
        "tags": [],
        "string1": null,
        "string2": null,
        "string3": null,
        "number1": 0,
        "number2": 0,
        "number3": 0,      
        "adjuncts": "https://api.dlc.service/customers/99/spaces/5498/images/my-image.tiff/adjuncts",    
        "metadata": "https://api.dlc.service/customers/99/spaces/5498/images/my-image.tiff/metadata",
        "storage": "https://api.dlc.service/customers/99/spaces/5498/images/my-image.tiff/storage",    
        "usedBy": "https://api.dlc.service/customers/99/spaces/5498/images/my-image.tiff/usedBy"
      }
    }
  ],
  "assets": [
    {
      "@id": "https://iiif.dlc.services/99/manifests/t454knmf/assets",
      "@type": "hydra:Collection"                    
    }
  ]
}
```

The very small asset payload produced a lot of IIIF. Stepping through this example:

* There are two `@context` values 
* `parent` and `slug` define the Manifest's position in the hierarchy as before
* `ingesting` is now `false` on the individual asset, and the `ingesting` property of the Manifest shows all completed. This means that canvases and assets on them have `width`, `height` and/or `duration` values, measured by the Platform.
* There is now one Canvas. The platform has minted an identifier for it, as none was provided: `https://iiif.dlc.services/99/canvases/7tgbn3wa`. **Note that this is public form - there is no hierarchical form for a Canvas, it cannot be manipulated outside of a Manifest**. 
* The Canvas has one AnnotationPage, whose `id` is formed by default as `<canvas-id>/painting`
* The AnnotationPage has one Annotation with motivation `painting`. The `id` of the Annotation is formed by default from `<annotation-page-id>/<canvasOrder>/<choiceOrder>`
* The body of the Annotation is an Image derived from the Image Service created from the Asset. For other content types, this will be an AV derivative, or a Choice of AV derivative.
* The dimensions of the image match those of the largest configured thumbs channel policy setting, if the asset has that channel, or the system default. They won't match the actual size of the image unless a thumbs channel size happens to match.
* The image has a service, which is the IIIF Image API service derived from the asset.
* When the asset was POSTed, we didn't specify a Space - only the `id` (not `@id`) property. The Platform created a Space 5498 for the new Manifest. This asset, and all subsequent _new_ assets introduced to the Platform in the context of this Manifest, will be added to that space.
* In the example above there is only an ImageService3 service, but you can have version 2 instead, or both, as set in configuration (see above).
* The image has a `paintedResource`. Its `id` should be treated as opaque, though in practice you may observe that it is formed of `/<customer>/paintedResources/<manifestId>/<canvasId>/<canvasOrder>/<choiceOrder>`. Do not parse values out of this identifier.
* The Canvas (not the image) has a `thumbnail`, which is derived from the thumbnail delivery channel output for the asset. The Platform always tries to use the first asset thumbnail as the Canvas thumbnail. If multiple assets are present on the same Canvas, then each asset also gets a thumbnail property, but not if only one.
* The Manifest has a `paintedResources` list, which contains the full information referred to in the Annotation Body. This has an `asset` property with all the properties of a regular Asset, and a `canvasPainting` property summarising the relationship between the asset and the manifest.


>❓If the canvases are "simple" can can be entirely round-tripped from the table alone, then synchronisation of a Manifest with the platform can _omit_ the `items` property altogether. This is the 99% use case for digitised material.

If your canvases carry no other information other than `label`, you can just use the `paintedResources` construction.

Where the manifest is configured with pipelines that will produce adjuncts, these too can be inferred.

You only need to explicitly provide the Manifest.items where your Canvases have additional properties or constructions that would be lost in this model.

>❓Come back to adjuncts. They can I think be entirely accomodated in this model, but we should get the adjunct-free version done first.

You can POST more assets in their extreme stripped down form, and they will result in Canvases being appended to the Manifest.

Or, you can POST a Hydra Collection of `PaintedResource` to the manifest's `../paintedResources` endpoint, just as you can with the regular queue. The order is significant _if you don't include explicit ordering information via canvasOrder and choiceOrder_.

If you specify `canvas` explicitly, you can mint new Canvas identifiers. These can either be wholly external, fully-qualified URLs, or they can follow the pattern `https://iiif.dlc.services/99/canvases/<canvas-identifier-part>`, which is recommended.

### Example: PUT the Manifest with a populated `paintedResources` list

```
PUT /99/manifests/demo-2
Host: https://api.dlc.Services
```
```json
{
  "type": "Manifest",
  "label": { "en": [ "Demo Manifest 2"] },
  "parent": "https://iiif.dlc.services/99/collections/my-flat-identifier",
  "slug": "demo-manifest-2",
  "paintedResources": [    
    {
      "asset": {
        "id": "MS-77-1recto.tiff",
        "mediaType": "image/tiff",
        "origin": "https://example.org/images/MS-77-1r.tiff"
      },
        "canvasPainting": {
        "canvas": "https://iiif.dlc.services/99/canvases/demo-manifest-2-ms-77-1r",
        "canvasOrder": 0,
        "label": { "en": [ "1 recto" ] }
      }
    },
    {
      "asset": {
        "id": "MS-77-1verso.tiff",
        "mediaType": "image/tiff",
        "origin": "https://example.org/images/MS-77-1v.tiff"
      },
      "canvasPainting": {
        "canvas": "https://iiif.dlc.services/99/canvases/demo-manifest-2-ms-77-1v",
        "canvasOrder": 1,
        "label": { "en": [ "1 verso" ] }
      }
    },
    {
      "asset": {
        "id": "MS-77-2recto-visible.tiff",
        "mediaType": "image/tiff",
        "origin": "https://example.org/images/MS-77-2r-v.tiff"
      },
      "canvasPainting": {
        "canvas": "https://iiif.dlc.services/99/canvases/demo-manifest-2-ms-77-2r-vis",
        "canvasOrder": 2,
        "choiceOrder": 1,
        "canvasLabel": { "en": [ "2 recto (with choice)" ] },
        "label": { "en": [ "Visible light" ] }
      }
    },
    {
      "asset": {
        "id": "MS-77-2recto-uv.tiff",
        "mediaType": "image/tiff",
        "origin": "https://example.org/images/MS-77-2r-uv.tiff"
      },
      "canvasPainting": {
        "canvas": "https://iiif.dlc.services/99/canvases/demo-manifest-2-ms-77-2r-uv",
        "canvasOrder": 2,
        "choiceOrder": 2,
        "label": { "en": [ "Ultraviolet" ] }
      }
    },
    {
      "asset": {
        "id": "MS-77-2recto-xray.tiff",
        "mediaType": "image/tiff",
        "origin": "https://example.org/images/MS-77-2r-x.tiff"
      },
      "canvasPainting": {
        "canvas": "https://iiif.dlc.services/99/canvases/demo-manifest-2-ms-77-2r-x",
        "canvasOrder": 2,
        "choiceOrder": 3,
        "label": { "en": [ "X Ray" ] }
      }
    },
    {
      "asset": {
        "id": "MS-77-2verso.tiff",
        "mediaType": "image/tiff",
        "origin": "https://example.org/images/MS-77-2v.tiff"
      },
      "canvasPainting": {
        "canvas": "https://iiif.dlc.services/99/canvases/demo-manifest-2-ms-77-2v",
        "canvasOrder": 0,
        "label": { "en": [ "2 verso" ] }
      }
    }
  ]
}
```

The above payload would:

* Create a new Manifest
* Register 6 assets
* Create 4 canvases in the Manifest
* The first, second and fourth Canvases just have one Image painted on them, targeting the whole Canvas
* The third Canvas has a `Choice` of three different wavelengths of light. The Annotation with the Choice body targets the whole Canvas (the `target` has been absent, i.e., null, throughout).


## "JSON is King" - handling complex update scenarios

So far you have seen that:

- `paintedResources` offers a concise, asset-centric way to construct IIIF quickly
- You can save any valid IIIF JSON for Manifests and IIIF Collections
- A IIIF Collection can be a container, like a Storage Collection, AND have arbitrary JSON content in its `items` property.

Both `paintedResources` for canvases and `items` for containment relationships are potentially in conflict. If you POST a Manifest that has existing canvases in its `items` property AND has a non-empty `paintedResources` property, what are you telling the server to do? The two sources of information may disagree with each other.

For IIIF Collections, we have seen that the `items` property is automatically populated from the contained items (just like a Storage Collection), until you supply JSON in `items` that differs _in any way_ from the JSON that would have been automatically produced by the containment relationship.

There is a general principle at work, and that is "JSON is King":

- You are saving JSON; the server respects that JSON, any JSON you post is always regarded as authoritative and intended to be what is served to the public.
- `paintedResources` on a Manifest, and containment relationships on a Collection, are shortcuts that will generate JSON where none exists.
- This generated JSON can round-trip on edit cycles.
- The server will evaluate the canvases in the manifest's `items` property and generate its internal `paintedResources` equivalent. This is what gets served back in that property - it's always derived from existing JSON items when serving a Flat/API Manifest.
- When you POST or PUT a Manifest with `paintedResources` as part of the payload, the server will evaluate your supplied paintedResources with those implied by the existing `items`. 
- If they are in conflict, e.g., your `items` has an asset on the first canvas but your `paintedResources` has it on the 7th - then it's a Bad Request.
- If any difference is purely **additive**, with no conflicts with existing `items`, then the server will process the `paintedResources`, and add canvases where necessary. An obvious example is a new manifest where `items` is empty; `paintedResources` is entirely additive.
- removal, reordering and restructuring are done by providing updated JSON. This is unambiguous; this is what the Manifest should have.
- a round trip of requesting a Flat/API Manifest and then saving it back without changes would be a no-op - the `paintedResources` should still be those exactly inferred from the `items`, so no work is needed on the server.
- If I make some changes - a reordering and a couple of deletions - from `items`, but leave the `paintedResources` intact, then the server will detect a conflict. My canvasOrders won't line up; the generated paintedResources won't match the supplied. Even though we could use the "JSON is King" rule and just ignore paintedResources, it's better to reject as a Bad Request. It's easiest for the user if POSTing an update with re-arrangement and/or deletions is accompanied by an _empty_  `paintedResources`. Because _JSON is King_ nothing will be lost.



### Further questions to shortcut

1. What does the flat API manifest look like while any assets used on its canvases are ingesting? It doesn't know the full details of the IIIF there yet.
2. What does the public one look like (I suspect this is easier as it simply looks like the previous version until everything has finished)




### IGNORE THIS - CONSIDER THIS LATER Example: Synchronise a Manifest with inline Assets

An alternative but equivalent approach is to construct the Manifest's items manually, including the Annotation Pages and painting annotations, but instead of the Annotation body being an Image, it's the Asset to synchronise. The following just has one example for brevity. Leave the `paintedResources` field blank. Also notice that the `id` of the Canvases, AnnotationPages and Annotations have been omitted - the platform will assign them. The annotation target has also been omitted; the platform will fill it in.

You can supply your own specific identifiers, though.

```
PUT /99/manifests/demo-3
Host: https://api.dlc.Services
```
```json
{
  "type": "Manifest",
  "label": { "en": [ "Demo Manifest 3"] },
  "parent": "https://iiif.dlc.services/99/collections/my-flat-identifier",
  "slug": "demo-manifest-3",
  "items": [
    {
      "type": "Canvas",
      "items": [
        {
          "type": "AnnotationPage",
          "items": [
            {
              "type": "Annotation",
              "motivation": [ "painting" ],
              "body": {
                "type": "vocab:Image",                
                "id": "MS-77-1recto.tiff",
                "mediaType": "image/tiff",
                "origin": "https://example.org/images/MS-77-1r.tiff",
                "label": { "en": [ "1 recto" ] }
              }
            }
          ]
        }
      ]
    }
  ]
}
```

The additional paintedResource properties are not required, because they can be inferred from the IIIF structure. Even the `target` - which if not the full Canvas, still needs to be specified in the payload above.

>❓What is the `type` there? Is it really a `vocab:Image`?

## Important Point!

>❓Remember that in all these examples, shorthand JSON constructs for paintedResources are creating the IIIF. But all subsequent operations, the JSON is king. And while you can still mix and match, the canvas_paintings table is always led by what the JSON says; it's decomposed into that table, reconciled with any additional assets.

>❓Getting this right will be hard!


- add an additional Canvas that is external

- add AV assets

- add file assets

- Handling of non-image assets (new section describing Wellcome approach)

- Make changes to Manifest and update.


### Example: modify a Manifest by manipulating its paintedResources


### Example: reference assets in spaces


### Example: paging in Collections


> <small>touched 2025-09-23T12:04:54</small>