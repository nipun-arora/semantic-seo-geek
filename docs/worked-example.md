# Semantic SEO worked example: topical map, EAV registers, and audit outputs

This page walks one fictional project through the workflows so you can see the shape of what each one produces. The scenario, the shop, and every finding below are illustrative demonstrations, not client data, and no traffic, ranking, or citation outcome is shown or implied. To see real outputs, run the prompts on your own project.

**Scenario:** a small retailer sells home espresso equipment through a 40-page site. The owner wants a content and structure plan the whole site can grow along.

## 1. Route the request

Prompt:

```text
Plan the SEO for my home espresso equipment shop. I have 40 pages and can publish 4 a month.
```

The router does not answer the question itself. It returns a plan-shaped selection:

```text
Specialists: eav-optimizer -> topical-map-architect -> technical-seo
Inputs needed: page inventory, current URL list, one representative product page
Sequence reason: entity coverage decides the map; the map decides what the
technical review must protect.
Handoffs: map feeds page-production per published page.
```

## 2. Model the entities (eav-optimizer)

The workflow decomposes the topic before any page is proposed. An excerpt of the entity register:

| Entity | Attribute | Type | Example values | Evidence state |
| --- | --- | --- | --- | --- |
| Espresso machine | Boiler configuration | Root | single, double, heat exchanger | Sourced |
| Espresso machine | Pressure profile | Root | 9 bar fixed, adjustable | Sourced |
| Espresso machine | Warranty length | Rare | 1 year, 2 years | Unknown — needs retailer policy |
| Grinder | Burr type | Root | flat, conical | Sourced |
| Grinder | Single-dose capability | Unique | yes, with bellows | Observed — product page |
| Portafilter | Basket standard | Root | 58 mm, 54 mm | Sourced |

`Unknown` rows are the point: they become questions for the owner, not guesses in the copy.

## 3. Architect the map (topical-map-architect)

Page allocation comes from attribute coverage, not a keyword dump. An excerpt of the hierarchy:

| Level | Page | Role | Covers |
| --- | --- | --- | --- |
| Root | Home espresso equipment guide | Informational hub | Entity overview, buying decision order |
| Seed | Espresso machines for home use | Commercial hub | Boiler configuration, pressure, budget tiers |
| Node | Single boiler or heat exchanger | Informational | One attribute contrast, links both hubs |
| Node | 58 mm and 54 mm baskets explained | Supporting | Basket standard, accessory compatibility |
| Seed | Grinders | Commercial hub | Burr type, retention, single dosing |

Each node names the attributes it must cover and the evidence gaps it inherits from the register.

## 4. Protect the structure (technical-seo)

The technical review reports findings with their evidence state, never a score:

```text
Observed  - 12 product URLs resolve with and without a trailing slash; no canonical.
Observed  - The grinder hub returns its heading in client-rendered JavaScript only.
Inferred  - Faceted color filters can mint crawlable duplicate URLs; needs a crawl to confirm.
Unknown   - No sitemap lastmod values; publishing cadence cannot be verified from the site.
```

Each finding carries an implementation note and what would change its label.

## 5. Produce a page (writing, auditing, humanizing)

For one node page, the editorial chain keeps claims traceable. A claim-ledger excerpt from `algorithmic-writer`:

```text
CLAIM: A heat exchanger machine can brew and steam at the same time.
STATE: SOURCED - manufacturer manual, page 4.
CLAIM: Most home users notice the difference within a week.
STATE: UNSOURCED - removed from draft.
```

`content-auditor` then reviews the draft findings-only, and `content-humanizer` revises rhythm and diction without touching a labeled claim. The uppercase ledger survives every pass.

## 6. Check AI-mediated visibility (aiseo-strategist)

The AiSEO review asks whether an assistant could quote the site safely:

```text
Observed  - The returns policy states two different restocking fees on two pages.
          An assistant cannot quote either safely. Resolve before anything else.
Observed  - No organization page states who operates the shop.
Inferred  - Product specification tables are extractable; keep them in HTML, not images.
```

Consistency defects rank first because they poison both search snippets and assistant answers.

## Run it on your project

```text
Use the eav-optimizer. Decompose my topic into an entity register with evidence states.
```

```text
Build a topical map from the attached page inventory. Mark coverage gaps.
```

```text
Audit this page's technical delivery. Separate observed defects from unknowns.
```

The workflows will ask for the inputs they need and will label what they could not verify. What they will not do is promise a ranking: the [FAQ](faq.md) records that boundary, and it applies to this example too.
