# Semantic SEO Geek: Semantic SEO and Technical SEO Skills for Claude Code and Codex

[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![CI](https://github.com/nipun-arora/semantic-seo-geek/actions/workflows/validate.yml/badge.svg)](https://github.com/nipun-arora/semantic-seo-geek/actions/workflows/validate.yml)

![Semantic SEO Geek — semantic SEO and technical SEO skills for Claude Code and Codex](.github/assets/social-preview.png)

Give Claude Code and Codex a semantic SEO practice, not a checklist. Semantic SEO Geek packages entity and attribute modeling, topical map architecture, technical SEO review, evidence-controlled content work, and AI search visibility into one open-source plugin with eleven specialist workflows.

Use it when you need a repeatable way to audit, plan, write, or review search-focused work without treating an SEO tactic as a guaranteed outcome. Each workflow separates verified evidence from inference and unresolved questions.

Three things distinguish it from SEO audit skills:

- **Entity-first.** Topics decompose into entities, attributes, and values before any page, title, or schema decision. See [Entity and attribute analysis](#entity-and-attribute-eav-analysis-for-semantic-seo).
- **Two coding agents, one implementation.** The same skill bodies run in Claude Code and in the Codex CLI.
- **Instructions, not tooling.** No crawler, no API keys, no accounts, no telemetry. See [what installing actually adds](#instructions-not-tooling).

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

## Install in Claude Code or the Codex CLI

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

## Entity and attribute (EAV) analysis for semantic SEO

Treating a site as a set of connected entities rather than a list of keywords is the core of semantic SEO. The `eav-optimizer` workflow makes that concrete: it decomposes a topic into entities, attributes, and values, records what the available evidence supports, and only then maps the supported facts to Schema.org vocabulary.

The entity registers feed the other workflows. `topical-map-architect` allocates pages from attribute coverage instead of keyword lists, `algorithmic-writer` drafts against the recorded facts, and `aiseo-strategist` uses the same registers to review how clearly sources describe the entity for AI-mediated search.

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

## Instructions, not tooling

Installing Semantic SEO Geek adds workflow instructions and two small local shell helpers to your coding agent. It adds no crawler, no rank tracker, no external API dependency, no account, and no telemetry. Your pages, briefs, and findings stay between you and your agent provider.

That boundary cuts both ways: the plugin works from the artifacts you supply and the fetching your agent can already do, and it will say so when a question needs crawl data or measurement it does not have.

## How it compares to SEO SaaS and audit skills

The table states capability boundaries, not quality judgments. Categories are generalized; individual products vary.

| Capability | SEO SaaS platforms | SEO audit skills for coding agents | Semantic SEO Geek |
| --- | --- | --- | --- |
| Runs where | Vendor servers | Your coding agent | Your coding agent |
| Crawling and rank data | Built in | Varies | None; works from artifacts you supply and fetching your agent already does |
| Accounts and API keys | Required | Sometimes required | None |
| Entity and EAV modeling | Varies | Rarely a stated focus | Core workflow, feeds mapping, writing, and AiSEO review |
| Supported agents | Not applicable | Often one provider | Claude Code and Codex from one implementation |
| Evidence labels on claims | Not typical | Not typical | Every material claim: observed, sourced, inferred, or unknown |
| Cost | Subscription | Usually free | Free, Apache 2.0 |

The deliberate trade-off: this package replaces neither a crawler nor a rank tracker. When a decision needs crawl coverage, log files, or measurement the workflows do not have, they say so instead of guessing.

## Built with its own workflows

Every public-facing page in this repository was drafted, audited, and revised through the plugin's own writing, auditing, and humanizing workflows, and the copy-pattern helper gates the documentation in this repository. The maintainer uses the same workflows on production SEO delivery. None of that guarantees your outcome; it does mean the instructions are exercised on real work rather than written speculatively.

## What the package does not contain

The public package contains functional workflow instructions and narrow validation helpers. It contains no private reference collection, classroom material, publication text, transcripts, paid resources, private research, or personal notes.

The release boundary is checked for excluded files and stale private references. These mechanical checks do not replace factual, legal, accessibility, rendered-page, or provider-specific validation.

## FAQ

### How do I do semantic SEO with Claude Code?

Install the plugin, then describe the deliverable you need. The router selects specialists, and the workflows start from entity and coverage analysis rather than keyword lists. You can also name a specialist directly, such as `eav-optimizer` or `topical-map-architect`.

### Does it work with the OpenAI Codex CLI?

Yes. Codex and Claude Code load the same skill bodies; only the manifests differ. The [install commands](#install-in-claude-code-or-the-codex-cli) cover both.

### How do I build a topical map with an AI coding agent?

Ask for one and supply your inventory: `Build a topical map for this documentation set from the supplied inventory.` The `topical-map-architect` workflow allocates pages from entity and attribute coverage and reports its evidence gaps. See [Skills](docs/skills.md) for sequences that combine it with entity analysis.

### Is Semantic SEO Geek free?

Yes. The whole package is open source under the Apache License 2.0, with no accounts, paid tiers, or API keys.

### Does it guarantee rankings, traffic, or AI citations?

No, and it will not claim to. Search and AI systems decide outcomes; the workflows keep every material claim labeled so you can see what is verified and what is not. See the [full FAQ](docs/faq.md) for the complete guarantee policy.

### Can it audit or humanize AI-written content?

`content-auditor` reviews any supplied content and reports findings without rewriting. `content-humanizer` revises approved copy for voice and rhythm while preserving claims and qualifiers; it is a style workflow, not a detector-evasion tool.

More questions are answered in the [full FAQ](docs/faq.md).

## Docs

- [Installation](docs/installation.md) — Codex and Claude Code install commands, local validation, and publication-dependent steps
- [Skills](docs/skills.md) — the selection table, evidence labels, and workflow sequences for common jobs
- [How it works](docs/how-it-works.md) — the deliverable-first method, evidence register, specialist contracts, and validation layers
- [Compatibility](docs/compatibility.md) — supported package surfaces, shared behavior, and helper-script runtime
- [Frequently asked questions](docs/faq.md) — scope, licensing, guarantees, and installation answers
- [License and permitted use](docs/license.md) — a plain-language Apache 2.0 summary and the trademark boundary
- [Acknowledgements](ACKNOWLEDGEMENTS.md) — educational influences and the independent-implementation boundary
- [Public source register](plugins/semantic-seo-geek/SOURCES.md) — the public primary sources the workflows draw on
- [Security policy](SECURITY.md) — how to report a vulnerability privately
- [Contributing](CONTRIBUTING.md) — issue forms and the version-1 contribution boundary

## Work with the maintainer

Semantic SEO Geek is maintained by [Nipun Arora](https://nipunarora.me), who uses the same workflows on production SEO delivery. For hands-on help — audits, topical architecture, content programs, or an engagement — see <https://nipunarora.me>. For plugin defects and workflow ideas, the [issue forms](CONTRIBUTING.md) remain the right channel, and no engagement is needed to get a bug fixed.

## License and publisher

Copyright © 2026 Nipun Arora.

The project is available under the [Apache License 2.0](LICENSE). Redistribution and modified versions are permitted under the license's conditions, including retention of the [`LICENSE`](LICENSE) and [`NOTICE.md`](NOTICE.md) files. The license grants no trademark rights: the name and logo are governed by the [trademark policy](TRADEMARKS.md), so a fork or derived product must use its own branding and must not present itself as the official Semantic SEO Geek project.

The canonical repository is <https://github.com/nipun-arora/semantic-seo-geek>.
