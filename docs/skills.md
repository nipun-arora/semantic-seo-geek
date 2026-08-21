# Semantic SEO Geek skills

Semantic SEO Geek packages 11 workflows for planning, producing, and reviewing search-focused work. Each skill has a defined scope, evidence rules, output contract, and handoff conditions.

## Pick the smallest useful workflow

Use `using-semantic-seo-geek` when a request spans several areas or when you do not know where to start. If you already know the deliverable, name the specialist directly. The router preserves explicitly requested specialists.

| Skill | Choose it when you need | Typical deliverable |
| --- | --- | --- |
| `using-semantic-seo-geek` | Routing for a broad, ambiguous, or multi-part SEO request | A selected specialist, sequence, inputs, and handoffs—or execution of the selected workflow |
| `technical-seo` | Crawlability, indexability, rendering, canonicals, sitemaps, redirects, links, directives, or structured-data delivery | Evidence-led technical findings and implementation guidance |
| `topical-map-architect` | Site hierarchy, page allocation, topical coverage, URL structure, clusters, or internal links | A page and relationship plan with scope and evidence gaps |
| `eav-optimizer` | Entity identity, attributes, values, relationships, disambiguation, or Schema.org mapping | Entity and attribute registers, vocabulary mapping, gaps, and optional implementation fields |
| `algorithmic-writer` | A new draft or evidence-controlled revision from an approved brief and source pack | Publishable copy, claim ledger, source notes, editorial notes, and validation |
| `content-auditor` | A findings-only review of usefulness, evidence, clarity, completeness, trust, structure, or policy risk | Prioritized findings, claim coverage, strengths, and handoff plan |
| `content-humanizer` | Voice, rhythm, diction, and specificity edits to approved copy | Revised copy, preservation check, change log, questions, and validation |
| `page-production` | Assembly of an evidence-approved page across copy, metadata, links, media, and publishing checks | A publish-ready page package and pre-publication checks |
| `title-heading-optimizer` | Title elements, visible main titles, heading hierarchy, duplicate patterns, or title-link diagnostics | Recommended title set, heading outline, template rules, and validation plan |
| `visual-semantics` | Image purpose, alternative text, visual accessibility, image discovery, licensing, or ImageObject planning | A visual inventory, treatment decisions, metadata guidance, and checks |
| `aiseo-strategist` | Source clarity, crawler controls, citations, reputation, measurement, or visibility across AI-mediated search | A provider-aware evidence register, priorities, controls, and measurement plan |

## Evidence labels

Every material recommendation should keep its evidence state visible:

| Label | Meaning |
| --- | --- |
| **Observed** | Directly verified in a supplied page, file, report, dataset, record, or test result |
| **Sourced** | Supported by a cited current primary source |
| **Inferred** | Reasoned from evidence, with the reasoning made explicit |
| **Unknown** | Not verified; the workflow identifies the evidence needed to resolve it |

Writing and editing workflows preserve upstream evidence IDs and translate them into an editorial claim ledger with uppercase labels: `OBSERVED`, `SOURCED`, `INFERRED`, and `UNSOURCED`. An upstream `Unknown` becomes a linked `UNSOURCED` editorial entry and must not be published as fact. Upstream observations and sources still require approval for the editorial source pack.

These labels describe evidence. They are not confidence theatre, ranking scores, or performance forecasts.

## Useful sequences

### Improve an existing page

1. Use `content-auditor` for findings.
2. Resolve factual gaps with the responsible owner or `eav-optimizer`.
3. Use `algorithmic-writer` only when a rewrite is requested.
4. Use `title-heading-optimizer` for the title and section promise.
5. Use `content-humanizer` after claims are approved.
6. Use `page-production` for final assembly.

### Plan a new section of a site

1. Use `technical-seo` to identify access or delivery constraints.
2. Use `topical-map-architect` to allocate page purposes and relationships.
3. Use `eav-optimizer` to model verified subjects and facts.
4. Send approved briefs to the writing and page-production workflows.

### Prepare structured data

1. Use `eav-optimizer` to model page-visible, verified facts.
2. Use `technical-seo` to review placement, rendering, and validation.
3. Check the target provider's current feature eligibility and policies separately.

Valid syntax or vocabulary does not guarantee a search feature, presentation, ranking, or citation.

### Review an image-heavy page

1. Use `visual-semantics` to classify each image's purpose.
2. Use `technical-seo` for discovery and delivery defects.
3. Use `page-production` to reconcile media, copy, links, and markup.

### Assess AI-assisted search visibility

1. Use `aiseo-strategist` to separate provider-specific access, source clarity, mentions, and measurement questions.
2. Use `technical-seo` for crawl controls and page delivery.
3. Use a content or entity specialist only for a concrete gap supported by evidence.

## Boundaries shared by every skill

The workflows do not:

- promise rankings, indexing, traffic, rich results, conversions, or AI citations;
- fabricate observations, sources, tests, demand data, or performance results;
- convert an unsupported tactic into a ranking factor;
- impose universal word counts, title lengths, keyword densities, entity counts, or schema quotas;
- recommend deceptive markup, fabricated mentions, doorway pages, or scaled low-value variants; or
- replace factual, legal, accessibility, rendered-page, or provider-specific review.

Platform behavior changes. Use the [public source register](../plugins/semantic-seo-geek/SOURCES.md) as a starting point, then verify current primary documentation for time-sensitive recommendations.

## Ask with enough context

A good request names the artifact, the desired decision or output, the usable evidence, and any limits.

```text
Audit this draft for an audience of first-time store owners. Use only the attached brief and source pack. Report findings; do not rewrite.
```

```text
Map the primary entity and supported product attributes on this page. Mark missing provenance as Unknown and do not generate JSON-LD yet.
```

```text
Review the current title and heading outline for clarity and accessibility. Do not use fixed character limits.
```

When a required fact is missing, the workflow should identify the Unknown rather than manufacture a complete-looking answer.
