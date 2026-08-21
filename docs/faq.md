# Frequently asked questions

## What is Semantic SEO Geek?

Semantic SEO Geek is an open-source plugin that gives Codex and Claude Code 11 evidence-led workflows for technical SEO, topical planning, entity coverage, content production, visual SEO, and AI search visibility.

It is a workflow package, not an SEO data provider, crawler, rank tracker, or guarantee engine.

## Is Semantic SEO Geek open source?

Yes. It is licensed under the [Apache License 2.0](../LICENSE), which permits use, modification, and redistribution for any purpose, including commercial use, under the license's conditions.

Read [License and permitted use](license.md) for a plain-language summary. The license text governs if the summary differs.

## What use does the license permit?

Everything the Apache License 2.0 grants: use, private modification, redistribution of original or modified copies, sublicensing, and commercial use, by companies and individuals alike. Personal and hobby use are covered by the same grant.

If you redistribute, keep the [license](../LICENSE) and the attribution notices in [`NOTICE.md`](../NOTICE.md), preserve existing notices, and state significant changes to modified files.

This answer summarizes the repository terms; it is not legal advice.

## Can I fork the repository on GitHub?

Yes. GitHub's native forking is allowed by GitHub's terms, and the Apache License 2.0 also permits forks and redistribution directly, subject to its conditions.

Follow the [trademark policy](../TRADEMARKS.md) for naming, and see [`NOTICE.md`](../NOTICE.md) for the attribution that must travel with copies.

## Can I publish a modified version under my name?

You may publish modified versions under the Apache License 2.0's conditions, with your own branding. The license grants no trademark rights: a modified version must not use the Semantic SEO Geek™ name or logo as its branding, must not present itself as the official Semantic SEO Geek project, and must not imply affiliation, sponsorship, approval, or endorsement. Keep the required license and notice files and mark your changes.

## Does the plugin contain private learning or reference material?

No. The public package contains functional workflow instructions and narrow validation helpers. It contains no private reference collection, classroom material, publication text, transcripts, paid resources, private research, or personal notes.

The [public source register](../plugins/semantic-seo-geek/SOURCES.md) lists the primary public documentation used to define platform and policy boundaries.

## What are the 11 skills?

The package includes routing, technical SEO, topical mapping, entity and attribute modeling, evidence-controlled writing, content audit, voice refinement, page production, title and heading optimization, visual semantics, and AI-assisted search strategy.

See [Skills](skills.md) for the exact skill names and deliverables.

## Do I need to choose a skill myself?

No. Give the agent the artifact, desired outcome, usable evidence, and constraints. `using-semantic-seo-geek` can route a broad request to the smallest useful specialist set.

If you name a specialist explicitly, the router preserves that request.

## Does Semantic SEO Geek guarantee rankings, traffic, indexing, rich results, or AI citations?

No. The workflows do not promise outcomes controlled by search or answer providers. They separate:

- whether a page or feature may be eligible;
- whether a provider selects it; and
- how it performs if selected.

Each question needs its own evidence and measurement.

## Does the content humanizer evade AI detectors?

No. It refines voice, rhythm, diction, and specificity while preserving approved claims, citations, and qualifiers. It does not infer authorship, report detector scores, or promise detector evasion.

## Why do the workflows label evidence?

The labels distinguish what was directly verified, what a current primary source supports, what the workflow inferred, and what remains unknown. This makes a recommendation easier to review and keeps unsupported assumptions out of factual copy or markup.

Evidence labels do not create a ranking score or universal measure of quality.

## Does valid structured data guarantee a rich result?

No. Valid and policy-compliant structured data can support eligibility for a provider's supported feature. It does not guarantee display, ranking, traffic, or another presentation.

## Does the plugin use fixed word counts, title limits, keyword density, or schema quotas?

No universal thresholds are built into the workflows. Content length, titles, headings, entities, and markup should serve the real page purpose and the verified publishing context.

Provider-specific requirements should be checked against current primary documentation.

## Can I install it in another agent environment?

Version 1 packages and supports Codex and Claude Code first. The shared skills are plain Markdown, but other environments do not yet have a supplied installer, manifest, compatibility promise, or support policy.

## Why do the GitHub install commands fail before release?

The marketplace commands resolve the canonical public repository. They cannot fetch an unpublished local release candidate. Local structural and manifest checks can run before publication; remote install smoke tests require the repository to be public.

See [Installation](installation.md) for the local and publication-dependent steps.

## Do I need a separate license for commercial use or redistribution?

No. The Apache License 2.0 already covers commercial use and redistribution under its conditions. Only use of the Semantic SEO Geek™ name or logo as branding for another product or service falls outside the license; see the [trademark policy](../TRADEMARKS.md).

## How do I report a security issue?

Use GitHub private vulnerability reporting for the [canonical repository](https://github.com/nipun-arora/semantic-seo-geek). Do not publish an unpatched vulnerability or leaked credential in an issue. See [Security](../SECURITY.md).
