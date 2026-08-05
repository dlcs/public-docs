# DLCS.HydraModel property flags

> GENERATED FILE — do not edit by hand; re-run `tools/hydra-model-dump` instead.
> Source: DLCS.HydraModel. Context: protagonist develop@5c13a2f5 + hygiene/session-0 (PR #1236); XC-07 link removals (PR #1237) NOT yet included
>
> Per XC-09: docs tables and these attributes must agree. A mismatch is a card-level
> decision (either side may hold the intended contract), not a silent fix.

## Adjunct

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| id | field | xsd:string | False | False |
| asset | field | xsd:string | False | False |
| mediaType | field | xsd:string | False | False |
| iiifLink | field | xsd:string | False | False |
| profile | field | xsd:string | False | False |
| label | field | xsd: | False | False |
| language | field | xsd:string | False | False |
| externalId | field | xsd:string | False | False |
| publicId | field | xsd:string | False | False |
| size | field | xsd:string | False | False |
| created | field | xsd:string | False | False |
| finished | field | xsd:string | False | False |
| origin | field | xsd:string | False | False |
| motivation | field | xsd:string | False | False |
| provides | field | xsd:string | False | False |
| ingesting | field | xsd:boolean | True | False |
| batch | link | hydra:Resource | True | False |
| error | field | xsd:string | False | False |

## AdjunctBatch

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| submitted | field | xsd:dateTime | True | False |
| count | field | xsd:nonNegativeInteger | True | False |
| completed | field | xsd:nonNegativeInteger | True | False |
| errors | field | xsd:nonNegativeInteger | True | False |
| finished | field | xsd:dateTime | True | False |

## ApiKey

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| key | field | xsd:string | False | False |
| secret | field | xsd:string | False | False |

## AuthService

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| name | field | xsd:string | False | False |
| profile | field | xsd:string | False | False |
| label | field | xsd:string | False | False |
| description | field | xsd:string | False | False |
| pageLabel | field | xsd:string | False | False |
| pageDescription | field | xsd:string | False | False |
| callToAction | field | xsd:string | False | False |
| timeToLive | field | xsd:nonNegativeInteger | False | False |
| nestedServices | link | hydra:Collection | True | False |
| roleProvider | link | vocab:RoleProvider | True | False |

## Batch

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| submitted | field | xsd:dateTime | True | False |
| count | field | xsd:nonNegativeInteger | True | False |
| completed | field | xsd:nonNegativeInteger | True | False |
| finished | field | xsd:dateTime | True | False |
| errors | field | xsd:nonNegativeInteger | True | False |
| superseded | field | xsd:boolean | True | False |
| estCompletion | field | xsd:dateTime | True | False |
| images | link | hydra:Collection | True | False |
| completedImages | link | hydra:Collection | True | False |
| errorImages | link | hydra:Collection | True | False |
| test | link | hydra:Collection | True | False |

## Customer

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| name | field | xsd:string | False | False |
| displayName | field | xsd:string | False | False |
| portalUsers | link | hydra:Collection | True | False |
| namedQueries | link | hydra:Collection | True | False |
| originStrategies | link | hydra:Collection | True | False |
| deliveryChannelPolicies | link | hydra:Collection | True | False |
| defaultDeliveryChannels | link | hydra:Collection | True | False |
| authServices | link | hydra:Collection | True | False |
| roleProviders | link | hydra:Collection | True | False |
| roles | link | hydra:Collection | True | False |
| queue | link | vocab:Queue | True | False |
| spaces | link | hydra:Collection | True | False |
| allImages | link | hydra:Collection | True | False |
| storage | link | vocab:CustomerStorage | True | False |
| keys | link | hydra:Collection | True | False |
| customHeaders | link | hydra:Collection | True | False |
| administrator | field | xsd:boolean | True | False |
| created | field | xsd:dateTime | True | False |
| acceptedAgreement | field | xsd:boolean | True | False |

## CustomerAdjunctQueue

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| size | field | xsd:nonNegativeInteger | True | False |
| batchesWaiting | field | xsd:nonNegativeInteger | True | False |
| adjunctsWaiting | field | xsd:nonNegativeInteger | True | False |
| batches | link | vocab:AdjunctBatch | True | False |
| active | link | vocab:AdjunctQueue | True | False |
| recent | link | vocab:AdjunctQueue | True | False |

## CustomerOriginStrategy

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| regex | field | xsd:string | False | False |
| strategy | link | vocab:OriginStrategy | False | False |
| credentials | field | xsd:string | False | True |
| optimised | field | xsd:boolean | False | False |
| order | field | xsd:integer | False | False |

## CustomerQueue

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| size | field | xsd:nonNegativeInteger | True | False |
| batchesWaiting | field | xsd:nonNegativeInteger | True | False |
| imagesWaiting | field | xsd:nonNegativeInteger | True | False |
| batches | link | vocab:Batch | True | False |
| images | link | vocab:Image | True | False |
| active | link | vocab:Queue | True | False |
| recent | link | vocab:Queue | True | False |
| priority | link | vocab:Queue | True | False |

## CustomerStorage

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| numberOfStoredImages | field | xsd:integer | True | False |
| totalSizeOfStoredImages | field | xsd:integer | True | False |
| totalSizeOfThumbnails | field | xsd:integer | True | False |
| numberOfStoredAdjuncts | field | xsd:integer | True | False |
| totalSizeOfStoredAdjuncts | field | xsd:integer | True | False |
| lastCalculated | field | xsd:dateTime | True | False |
| storagePolicy | link | vocab:StoragePolicy | True | False |

## CustomHeader

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| role | link | vocab:Role | False | False |
| key | field | xsd:string | False | False |
| value | field | xsd:string | False | False |
| space | field | xsd:integer | False | False |

## DefaultDeliveryChannel

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| channel | field | xsd:string | False | False |
| policy | link | vocab:deliveryChannelPolicy | False | False |
| mediaType | link | xsd:string | False | False |

## DeliveryChannel

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| channel | field | xsd:string | False | False |
| policy | link | vocab:deliveryChannelPolicy | False | False |

## DeliveryChannelPolicy

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| name | field | xsd:string | False | False |
| displayName | field | xsd:string | False | False |
| channel | field | xsd:string | False | False |
| policyData | field | xsd:string | False | False |
| policyCreated | field | xsd:dateTime | True | False |
| policyModified | field | xsd:dateTime | True | False |

## EntryPoint

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| customers | link | hydra:Collection | True | False |
| originStrategies | link | hydra:Collection | True | False |
| portalRoles | link | hydra:Collection | True | False |
| imageOptimisationPolicies | link | hydra:Collection | True | False |
| thumbnailPolicies | link | hydra:Collection | True | False |
| storagePolicies | link | hydra:Collection | True | False |

## Image

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| id | field | xsd:string | False | False |
| imageService | field | xsd:string | False | False |
| degradedInfoJson | field | xsd:string | False | False |
| thumbnailImageService | field | xsd:string | False | False |
| thumbnail400 | field | xsd:string | True | False |
| created | field | xsd:dateTime | True | False |
| origin | field | xsd:string | False | False |
| maxUnauthorised | field | xsd:integer | False | False |
| maxWidth | field | xsd:integer | False | False |
| openFullMax | field | xsd:integer | False | False |
| duration | field | xsd:integer | True | False |
| width | field | xsd:integer | True | False |
| height | field | xsd:integer | True | False |
| queued | field | xsd:dateTime | True | False |
| dequeued | field | xsd:dateTime | True | False |
| finished | field | xsd:dateTime | True | False |
| ingesting | field | xsd:boolean | True | False |
| error | field | xsd:string | False | False |
| tags | field | xsd:string | False | False |
| string1 | field | xsd:string | False | False |
| string2 | field | xsd:string | False | False |
| string3 | field | xsd:string | False | False |
| number1 | field | xsd:nonNegativeInteger | False | False |
| number2 | field | xsd:nonNegativeInteger | False | False |
| number3 | field | xsd:nonNegativeInteger | False | False |
| roles | field | vocab:Role | False | False |
| batch | link | vocab:Batch | True | False |
| imageOptimisationPolicy | link | vocab:ImageOptimisationPolicy | True | False |
| adjuncts | link | vocab:Adjunct | True | False |
| thumbnailPolicy | link | vocab:ThumbnailPolicy | True | False |
| metadata | link | vocab:ProcessingMetadata | True | False |
| storage | link | vocab:AssetStorageInfo | True | False |
| manifests | link | vocab:Manifests | True | False |
| mediaType | field | xsd:string | True | False |
| text | field | xsd:string | True | False |
| family | field | xsd:string | True | False |
| textType | field | xsd:string | True | False |
| deliveryChannels | field | xsd:string | False | False |

## ImageOptimisationPolicy

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| name | field | xsd:string | False | False |
| technicalDetails | field | xsd:string | False | False |
| global | field | xsd:boolean | False | False |

## ImageStorage

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| thumbnailSize | field | xsd:nonNegativeInteger | True | False |
| size | field | xsd:nonNegativeInteger | True | False |
| adjunctSize | field | xsd:nonNegativeInteger | True | False |
| lastChecked | field | xsd:dateTime | True | False |
| checkingInProgress | field | xsd:boolean | True | False |

## NamedQuery

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| name | field | xsd:string | False | False |
| global | field | xsd:boolean | False | False |
| template | field | xsd:string | False | False |

## OriginStrategy

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| name | field | xsd:string | False | False |
| requiresCredentials | field | xsd:boolean | True | False |

## PortalRole

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| name | field | xsd:string | False | False |

## PortalUser

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| email | field | xsd:string | False | False |
| password | field | xsd:string | False | True |
| created | field | xsd:dateTime | False | False |
| roles | link | hydra:Collection | True | False |
| enabled | field | xsd:boolean | False | False |

## Queue

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| size | field | xsd:nonNegativeInteger | True | False |
| batches | link | hydra:Collection | True | False |
| images | link | hydra:Collection | True | False |
| recent | link | hydra:Collection | True | False |
| active | link | hydra:Collection | True | False |

## QueueSummary

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| incoming | field | xsd:nonNegativeInteger | True | False |
| priority | field | xsd:nonNegativeInteger | True | False |
| timebased | field | xsd:nonNegativeInteger | True | False |
| transcodeComplete | field | xsd:nonNegativeInteger | True | False |
| file | field | xsd:nonNegativeInteger | True | False |

## Role

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| name | field | xsd:string | False | False |
| label | field | xsd:string | False | False |
| aliases | field | xsd:string | False | False |
| authService | link | vocab:AuthService | False | False |

## RoleProvider

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| configuration | field | xsd:string | False | False |
| credentials | field | xsd:string | False | True |

## Space

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| id | field | xsd:integer | False | False |
| name | field | xsd:string | False | False |
| created | field | xsd:dateTime | True | False |
| defaultTags | field | xsd:string | False | False |
| maxUnauthorised | field | xsd:integer | False | False |
| approximateNumberOfImages | field | xsd:integer | True | False |
| defaultRoles | field | xsd:string | False | False |
| images | link | hydra:Collection | True | False |
| defaultDeliveryChannels | link | hydra:Collection | True | False |
| metadata | link | vocab:Metadata | True | False |
| storage | link | vocab:CustomerStorage | True | False |

## StoragePolicy

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| maximumNumberOfStoredImages | field | xsd:nonNegativeInteger | False | False |
| maximumTotalSizeOfStoredImages | field | xsd:nonNegativeInteger | False | False |

## ThumbnailPolicy

| property | kind | range | readonly | writeonly |
|:---|:---|:---|:---|:---|
| name | field | xsd:string | False | False |
| sizes | field | xsd:nonNegativeInteger | False | False |
