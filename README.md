# Semantic SEO Geek: SEO Skills for Codex and Claude Code

![Semantic SEO Geek — 11 SEO workflows for Codex and Claude Code](.github/assets/social-preview.png)

Get 11 evidence-led workflows for technical SEO, topical planning, entity coverage, content production, visual SEO, and AI search visibility in Codex and Claude Code. Semantic SEO Geek packages them as one open-source plugin.

Use it when you need a repeatable way to audit, plan, write, or review search-focused work without treating an SEO tactic as a guaranteed outcome. Each workflow separates verified evidence from inference and unresolved questions.

> **License:** This project is open source under the [Apache License 2.0](LICENSE). Use it, modify it, and redistribute it under the license's conditions, which include retaining the [license](LICENSE) and [notice](NOTICE.md) files. The license grants no trademark rights: the Semantic SEO Geek name and logo stay with the [trademark policy](TRADEMARKS.md). Read [License and permitted use](docs/license.md) for a plain-language summary.

## What you can do

- audit crawlability, indexability, rendering, canonicals, sitemaps, redirects, and structured-data delivery;
- design topical maps, page relationships, URL structures, and internal-link plans;
- model entities, attributes, values, and supported Schema.org vocabulary;
- draft, assemble, humanize, and audit evidence-controlled web content;
- improve titles, visible main headings, and document structure;
- plan useful, accessible visual content and image metadata; and
- assess source clarity, crawler access, and measurement for AI-assisted search.

The plugin routes broad requests to the smallest useful specialist set. You can also name a specialist when you already know which workflow you need.

## Install

The GitHub marketplace commands below require the canonical repository to be public. They will not resolve before publication.

### Codex

```bash
codex plugin marketplace add nipun-arora/semantic-seo-geek --ref main
codex plugin add semantic-seo-geek@semantic-seo-geek
codex plugin list --available --json
```

Start a new Codex session after installation.

### Claude Code

```bash
claude plugin marketplace add nipun-arora/semantic-seo-geek
claude plugin install semantic-seo-geek@semantic-seo-geek
```

Open a new Claude Code session, or reload the active session, after installation.

See [Installation](docs/installation.md) for local validation and publication-dependent steps.

## Choose a workflow

| Skill | Use it for |
| --- | --- |
| `using-semantic-seo-geek` | Route a broad or multi-part request to the right specialists. |
| `technical-seo` | Review crawling, indexing, rendering, directives, canonicals, sitemaps, redirects, links, or structured-data delivery. |
| `topical-map-architect` | Plan site hierarchy, topical coverage, page relationships, URLs, and internal links. |
| `eav-optimizer` | Model entities, attributes, values, relationships, and truthful Schema.org mappings. |
| `algorithmic-writer` | Draft or revise search-aware copy from an approved brief and source pack. |
| `content-auditor` | Find evidence, usefulness, clarity, and policy problems without automatically rewriting the page. |
| `content-humanizer` | Refine approved copy for natural voice and rhythm while preserving claims and qualifiers. |
| `page-production` | Assemble a publish-ready page from approved evidence, copy, metadata, links, and media requirements. |
| `title-heading-optimizer` | Improve title elements, main titles, heading structure, and title-heading alignment. |
| `visual-semantics` | Plan image purpose, alternative text, image discovery, licensing details, and visual accessibility. |
| `aiseo-strategist` | Assess source clarity, crawler controls, citations, measurement, and reputation across AI-mediated search. |

Read [Skills](docs/skills.md) for selection guidance, outputs, and useful combinations.

## Ask for the outcome you need

You do not need a special prompt format. Describe the artifact and the decision you need the workflow to support.

Examples:

```text
Audit this site's crawl and index controls. Separate observed defects from unknowns.
```

```text
Build a topical map for this product documentation set from the supplied inventory.
```

```text
Use the content auditor. Report findings only; do not rewrite the page.
```

```text
Model the entities and supported facts on this page before proposing JSON-LD.
```

## Evidence stays visible

The general workflows use four labels for material claims:

- **Observed** — directly verified in a supplied artifact, page, report, dataset, or first-party record.
- **Sourced** — supported by a cited current primary source.
- **Inferred** — reasoned from evidence, with the reasoning stated.
- **Unknown** — not verified, with the missing evidence identified.

Editorial workflows preserve those records in an uppercase claim ledger. Upstream `Unknown` becomes `UNSOURCED` and stays out of publishable copy; upstream evidence is not promoted into an approved editorial source pack automatically.

The labels keep recommendations auditable. They do not create a universal SEO score, ranking prediction, or guarantee.

## One implementation for Codex and Claude

Codex and Claude Code load the same skill bodies from `plugins/semantic-seo-geek/skills/`. Platform-specific manifests describe the package; the functional workflows stay shared.

Version 1 targets Codex and Claude Code. Other agent environments are not packaged or supported yet. See [Compatibility](docs/compatibility.md).

## What the package does not contain

The public package contains functional workflow instructions and narrow validation helpers. It contains no private reference collection, classroom material, publication text, transcripts, paid resources, private research, or personal notes.

The release boundary is checked for excluded files and stale private references. These mechanical checks do not replace factual, legal, accessibility, rendered-page, or provider-specific validation.

## Read next

- [Installation](docs/installation.md)
- [Skills](docs/skills.md)
- [How it works](docs/how-it-works.md)
- [Compatibility](docs/compatibility.md)
- [Frequently asked questions](docs/faq.md)
- [License and permitted use](docs/license.md)
- [Acknowledgements](ACKNOWLEDGEMENTS.md)
- [Public source register](plugins/semantic-seo-geek/SOURCES.md)
- [Security policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)

## License and publisher

Copyright © 2026 Nipun Arora.

Semantic SEO Geek is available under the [Apache License 2.0](LICENSE). Redistribution and modified versions are permitted under the license's conditions, including retention of the [`LICENSE`](LICENSE) and [`NOTICE.md`](NOTICE.md) files. The license grants no trademark rights: the name and logo are governed by the [trademark policy](TRADEMARKS.md), so a fork or derived product must use its own branding and must not present itself as the official Semantic SEO Geek project.

The canonical repository is <https://github.com/nipun-arora/semantic-seo-geek>.
