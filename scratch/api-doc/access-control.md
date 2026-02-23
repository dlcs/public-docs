# THIS ENTIRE PAGE PORTED

Auth docs:
https://deploy-preview-2--dlcs-docs.netlify.app/api-doc/access-control and RFCs
https://github.com/dlcs/protagonist/issues/538 - Manage Auth Services via API
https://github.com/dlcs/iiif-auth-v2/issues/46 - auto create clickthrough role
Look at database tables in protagonist/iiif-auth db as they are now, and in RFCs etc

Write the full auth docs as a PR

this will have to come later though.

# Access Control

------------------------------

Need to synthesise 

https://github.com/dlcs/protagonist/blob/main/docs/rfcs/005-Access-Control.md
https://github.com/dlcs/protagonist/blob/main/docs/rfcs/008-more-access-control-oidc-oauth.md
https://github.com/dlcs/protagonist/blob/main/docs/rfcs/012-auth-service.md


Should we introduce a new API class, vocab:AccessService?

Or stick with AuthService?





---

This section is about end-user access control for assets and the services for those assets, not for the APIs of the platform itself. The user interaction with access control for assets is mediated by the IIIF Authorisation Flow 2.0 API, which is distinct from the REST HTTP API used to create and administer the assets.

The IIIF Authorisation Flow API is consumed (indirectly) by end-users, via IIIF Clients (viewers) in the browser. The REST API is consumed by systems integration workflows, tools, and possibly browser-based content creation tools.

## Sessions for users

In the following, "accessing an asset" or "see the asset" is used as shorthand for the various delivery channels. Requesting a transcoded derivative of a video, or requesting an image tile from a IIIF Image Service for an asset, are all covered by "accessing an asset".

The IIIF Cloud Services platform is the system serving the assets to end users, therefore it must establish a session (e.g., by using cookies, or other means) for each user.

Assets can have [roles](asset#roles). These are usually opaque URIs as far as the platform is concerned - they mean something to you, but they are just roles to match with users for the platform. An open, public asset has no roles: anyone can see it. An asset might have many roles; if the user has any of them, they can see the asset.

Access control requires the platform to know what roles the user has, and to establish a session for them so that it can authorise their access to assets based on their known roles - if the asset they are trying to access has the role, then the user's session needs to have the role too.

The platform learns what roles the user has from a **Role Provider**. It interacts with the role provider at runtime, to establish sessions for end users. 

* An Asset has [roles](asset#roles)
* A Customer has [authServices](customer#authservices)
* A Role has an AuthService
* An AuthService has a RoleProvider

There are three Role Providers included with the platform at present.


## The OIDC Role Provider

The system that knows who the user is, and can tell the platform what roles the user has, is _your_ user store. The platform implements a simple protocol to interact with your user store and acquire roles for a user. It then compares the roles the user has with the roles defined for an asset, to decide whether the user can see the asset.

The OIDC Role Provider is the bridge between the platform and your source of user information, authentication, and authorisation. The platform arranges for the user to establish an active relationship with the Role Provider. The Role Provider can then tell the platform what roles that user has.

It doesn't matter what those roles mean, or how the Role Provider decided they were appropriate for the user. They might be fixed - _this user is faculty, so can see images that require the "faculty" role_. Or they might be transient - _this user is in the "temporary-lesson" role for two hours only_. The platform doesn't need to know any of these details, they are delegated to the Role Provider.

The Role Provider doesn't authorise platform requests: it gives the platform the information it needs to authorise requests. The platform talks to the role provider to establish a session, but thereafter can authorise requests autonomously for the lifetime of the platform session. This is essential for performance, especially for image tile requests.

The OIDC Role Provider uses OAuth2 and OIDC. If your user store already implements these, it may be possible to just plug it in directly and use configuration to define endpoints, and mappings between OIDC _claims_ and the role URIs you're registering your assets with. If you have some other system, you might need to implement a bridge, so that the platform can speak to it using OAuth2 and OIDC, and your bridge speaks to the platform. This process can be greatly simplified with commercial services like Auth0.


## The Clickthrough Role Provider

The platform can enforce _clickthrough_ access control without further integration, as it does not need to know the identity of the user. It just needs to establish a session for them, and ensure they have accepted any clickthrough terms of use, or read a content-advisory notice.


## The IP-address Role Provider

