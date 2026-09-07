# DIS-19 verification captures — 2026-09-07

Real single-asset manifests fetched (unauthenticated) from
`https://dlcs-stage.digirati.io/iiif-manifest/15/98765/{asset}` during the DIS-19
verification pass. These are the sources of the examples on the live
single-asset-manifest page (hostname/customer/space/asset ids substituted there).

| file | scenario | verdict |
|:---|:---|:---|
| `page_01.json` | image, iiif-img + thumbs | baseline re-confirmation |
| `put-example-1-rusty-boat.json` | image + four adjuncts (one per iiifLink) | placements ✓; no `provides`/`fileSize`/annotations-page `language`; scalar motivation/body/target → protagonist **#1299** |
| `dis19-audio.json` | audio, iiif-av, `default-audio` (single transcode) | bare `Sound` ✓ (DIS-25 wire-confirmed); parameterised body id; no label |
| `dis19-video.json` | video, iiif-av, two-**mp4** policy `dis19-video-choice` | `Choice` with two IDENTICAL ids — outputs share one storage key → evidence on protagonist **#970** |
| `dis19-video-2.json` | video, iiif-av, mp4+webm policy `dis19-video-choice2` | correct `Choice`, distinct ids, both serve 200 — source of the live video example |
| `dis19-file-txt.json` | text/plain, file channel only | placeholder canvas ✓; born-digital `@context` array; `/static/text/placeholder.png`; generated rendering label |
| `dis19-no-channels.json` | image, `none` channel | **no canvas at all** (no `items`) — old example wrong |

Origins: docs fixtures (gh-pages) + `dlcsstage-public-test-objects` S3
(`other-video/fish.mp4`, `audio/music.mp3` — same objects the automated tests use).

The five `dis19-*` assets and both `dis19-video-choice*` policies are **left in place on
stage** as persistent fixtures (re-verification without re-transcoding; the two-mp4 asset is
live evidence for #970). The four adjuncts on `put-example-1-rusty-boat` were deleted after
capture. Transcoder-dedupe note: `fish.mp4` was transcoded twice this session (different asset
ids, ~40 min apart) and `music.mp3` once, with no AWS rejection observed. Mechanism
clarified by the PO afterwards (2026-09-07) — the occasional failure is MediaConvert's
duplicate-job protection, rejecting a job whose settings are *identical* to a recently
submitted one:

> `Amazon.MediaConvert.Model.BadRequestException: You submitted a duplicate job that has
> identical settings as the job '1757926412516-m3mcum' you submitted previously. To help
> prevent unnecessary charges, MediaConvert did not create your duplicate job. To resolve:
> Edit any of your job settings. Then resubmit your job.`

So a **new asset id avoids it** (the output destination differs → different settings —
which is why today's runs never hit it), while **re-ingesting the same asset + policy
soon after a previous attempt triggers it** (identical input and outputs). Implication
for future AV samples: don't re-ingest an existing timebased asset in a tight loop;
prefer GET-only against the persistent `dis19-*` fixtures, or mint a fresh asset id.
A deliberately vague caveat (no AWS/MediaConvert specifics, per the PO — the mechanism
may change) lives in `dlcs-docs-client/iiif_cs.py` next to `wait_for_value`.
