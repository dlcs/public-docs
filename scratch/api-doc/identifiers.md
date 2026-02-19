# Inconsistency: some resources use `name` rather than `id` as the model identifier

`DeliveryChannelPolicy` and `NamedQuery` use a `name` property for the value that becomes the last URL path element, whereas most other resources use `id` for this. The existing code sample for delivery channel policies even has a TODO comment noting this (`# TODO: why not "id" for consistency?`).

Consider whether to address this inconsistency — options include: documenting it as an intentional design choice (e.g. `name` signals a human-readable slug whereas `id` is more opaque), asking the platform team whether `id` could be accepted as an alias, or simply accepting it as a quirk and noting it clearly in the documentation (as done on this page).

# Original notes from old page

@id, id, ModelId

Minting identifiers and supplying your own (see origin strategy)

Consistency of supplying in POST

Special nature of asset identifiers

origin strategies and delivery channels as controlled vocabulary

## Asset Identifiers

Discussion of cust/space/id
