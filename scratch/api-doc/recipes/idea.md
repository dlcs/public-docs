The following is a transcript from Slack on Friday. You don't need to have the full context of all it, you can decide once you read the section at the end how much of this you want to investigate further. The aim is to make a new recipes section of the docs site, with an initial recipe that goes from a manifest with just images to one with OCR text, search services, and a searchable PDF.

-----------------------------------


paulmollahan  [4:29 PM]
Hi @Donald Gray @tomcrane

I wanted to follow up here on the conversation yesterday and open this up a bit in terms of how we wrap up a suitable response and recommendation to Delft as a conclusion.

I've added the notes from yesterday to the ticket - https://digirati.atlassian.net/browse/DEL-131?focusedCommentId=168937

However in taking a slight step back - whilst it is clear the DLCS has moved on with the text-services and the RFC #1230 addresses next steps - the out of scope element:

> This proposal is to support generating PDFs from DLCS Assets via NamedQueries (NQ). It does not address generating PDFs from arbitrary IIIF Manifests, that functionality is suited to dlcs/iiif-presentation.

means that the RFC is not really itself addressing Delft's requirement directly, so probably not that useful to have Jules review this in isolation.

So, do we have a clear picture of how Delft (and by extension other customers with similar setup(s) - not sure how many) could use this?

Sending existing Manifests to an API was the point he brought up - and I wonder if that's the IIIF Presentation API, thus storing these manifests which are already DLCS aware, which then enables the use of the text-services?

Some other points to note:

* Although not directly related to this - Jules highlighted that ideally if Delft could "just trigger a workflow on existing assets" they would use Gemini or another model to create OCR for their content.. 
* Adjuncts hosted by the DLCS is exactly how he envisages storing and managing the OCR so how this applies in the Delft use case needs some thought

And finally, the goal of the spike was to give them a recommendation - clearly we think the DLCS based approach makes sense. But can we clearly answer:

"Does the offering effectively support what we want to achieve in generating our PDFs, using our existing IIIF Manifests and any leveraging any supporting text (OCR or hOCR) as part of the PDF available alongside / part of the object pages”
[4:30 PM]It feels to me that a conversation to discuss next steps is likely to be the most productive, but conscious Tom that you noted the question about the RFC:

> structureProvider vs groupby decision probably needs his input, if we go with structureProvider but he says "nah I can't do that" then we've wasted time

tomcrane  [5:02 PM]
I suspect the underlying Text Services is really what would benefit Jules, because it will take any Manifest, index its linked text, provide search and autocomplete services, and a searchable PDF with a hidden text layer. It's what DLCS now uses to generate those things for its own, managed manifests. But Jules' manifests are not currently managed.
The problem is that we can't just expose the underlying text services because people could use it for anything. Maybe we don't mind that but we'd at least have to work out access control and billing.

But he could do it the way you say.. I'm not sure we are quite there yet.


1. He takes one of his current manifests, which has DLCS-managed assets but is not itself a DLCS-managed manifest. 
2. He saves this Manifest to iiif-p so that it becomes a managed manifest at a new URL.
3. He runs his own OCR process by whatever means, to generate a bunch of METS-ALTO XML files. (this is the step that we will offer ourselves at some point, but we don't have it now).
4. He saves each METS-ALTO XML file as an adjunct for its corresponding image asset in the DLCS
5. The managed manifest now includes these hosted METS-ALTO files, hoisted to seeAlso or annotations links on each Canvas (Q - that won't happen automatically I think, he'd have to trigger a regeneration of the managed manifest somehow)
6. He adds the pipeline property to the Manifest and saves it again (https://dlcs.github.io/public-docs/api-doc/pipelines/#the-manifest-text-pipeline)
7. IIIF-CS processes the manifest and when done, the manifest now has search services and a rendering property that links to the PDF. These are all hosted by the platform.
8. He can either now use this new manifest as the "official" one, or (probably more likely for him, for now) copy the new bits out of it into his existing manifest. That represents a rather awkward workflow though for further updates.


What I'm not sure of - although I'm going to try and test this now - is whether all these steps are in the most logical order and whether they actually all work on current staging or 0.11. I know that they all work if done in one go from a fresh paintedAssets-style manifest, but heere Jules is not starting from scratch. I'm not sure at what point it would be best to associate the new generated METS-ALTO with the existing assets. It could be done like this: https://dlcs.github.io/public-docs/api-doc/adjuncts/#creating-an-adjunct-from-an-origin, at the asset level... or can it be done by re-stating the paintedResources with inline `.adjuncts: [..]` property?

I am going to try this and see what way feels natural and what actually works.

@Jack Lewis may shed some light on what sequence works here.

Jack Lewis  [5:28 PM]
looking at this, (4) - (6) could be combined - there's automatic handling so that it will run the text pipeline after assets/adjuncts are complete (if they need ingesting etc.)

To do this though, he'd need to take his manifests and convert them into painted resource blocks that can then be OCR'd (we can avoid reingesting the existing assets if the asset ids match his DLCS asset ids though) as the text pipeline doesn't run on items (edited) 


paulmollahan  [5:38 PM]
Thanks guys. Perhaps we can discuss this further on Monday.

---------------------------------------------------------


(end of transcript)

This gave me the idea of having a Recipes section in the docs. This shows you how to do certain tasks.

Our recipe section could be even more useful if it actually did the missing OCR step in a simple way, using tessarect, or a model driven from python... I'm not sure what today's best option is for local OCR. In the recipe this step should be very pluggable, obvious that you could invoke your own OCR/HTR/other text-generating operation at this point. So it introduces an extra step before registering adjuncts - actually generating the adjuncts, which is something our platform doesn't do yet but will do in future (OCR step in pipeline).

There are several different starting positions that could all be accomodated:

* I have just the images and some descriptive metadata `label`, `metadata`... I haven't got a manifest yet - the platform-hosted manifest can be the one-and-only final manifest, we can build the whole thing in the example, including the OCR files that can be registered as adjuncts.
* I already have a manifest, and it uses image assets hosted by the platform, to which adjuncts could be attached, but it is not a iiif-presentation "managed" manifest (this is Jules' scenario). It has no linked text/OCR (no METS-ALTO or annotations yet). We would need to create a new iiif-presentation manifest that referenced the existing assets (would it recognise its own assets just from the canvas bodies or would we need to ingest the manifest with explicit paintedResources? the latter I think from Jack's comment) - this new manifest becomes the canonical version
* The same but I keep my original non-managed manifest and copy the new features into it - the OCR links, annotations, searchable PDF, IIIF Search services.
* A completely external manifest, not my assets. In this scenario we'd still save this external manifest JSON to the platform, but with additional `adjuncts` properties on each Canvas (not sure we support that just yet)

This recipe could be even simpler with the as-yet unimplemented (I think?) abilty to simply POST the bytes of an adjunct, rather than having it staged at an origin to fetched. I think for now the examples will have to used some staged images (which can live in the repo as static assets). You could use [this short manifest](https://iiif.wellcomecollection.org/presentation/b3343136x) to get some jpg images at full/max to act as the fixtures for the example (the jpegs would become the assets just like our rusty boat etc.) But it makes a simple runnable recipe tricky if it has to stage the adjuncts created by the OCR process so that they can then be used as `origin` values. Not sure how best to do this in a recipe example (any ideas...?)

So - make a documented recipe, that includes Python to do the OCR as simply as possible (the best possible OCR is not the goal here, that sample manifest looks straightforward to OCR)

Something useful for Jules that he can use today
But also really identifying the friction points in the workflow - where planned features, or even as-yet-unthought-of features, would make the flow much easier.