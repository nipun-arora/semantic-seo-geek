# Codex and Claude Code compatibility

Semantic SEO Geek version 1 targets Codex and Claude Code. Both environments load the same 11 skill bodies; only the marketplace and plugin manifests differ.

## Supported package surfaces

| Environment | Marketplace manifest | Plugin manifest | Functional skills | Release status |
| --- | --- | --- | --- | --- |
| Codex | `.agents/plugins/marketplace.json` | `plugins/semantic-seo-geek/.codex-plugin/plugin.json` | `plugins/semantic-seo-geek/skills/` | Version 1 release target |
| Claude Code | `.claude-plugin/marketplace.json` | `plugins/semantic-seo-geek/.claude-plugin/plugin.json` | `plugins/semantic-seo-geek/skills/` | Version 1 release target |

“Release target” identifies the intended compatibility surface. It is not a claim that an unpublished GitHub install has been tested. Remote marketplace smoke tests require the canonical repository to be public.

## Shared behavior

The package avoids separate Codex and Claude versions of the SEO workflows. A change to a skill's scope, evidence labels, guardrails, or output contract applies to both environments.

This shared layout reduces drift in:

- workflow selection;
- evidence handling;
- specialist handoffs;
- claims and policy boundaries; and
- public source references.

Platform manifests may expose different metadata, but they point to the same package directory.

## Helper-script runtime

The core workflows are Markdown instructions and remain usable without a shell runtime. Two
optional mechanical helpers require Bash plus a POSIX-compatible `awk`:

- `content-humanizer/scripts/scan-copy-patterns.sh`
- `page-production/scripts/page-structure-audit.sh`

On native Windows or another host without those commands, the agent should perform the documented
checks manually and record that the optional helper was skipped. Install Git Bash, WSL, or an
equivalent POSIX environment only if local policy permits it; plugin use does not require doing so.

## Validation scopes

Different checks answer different questions:

| Check | What it can establish | What it cannot establish |
| --- | --- | --- |
| `python3 scripts/validate.py check` | Repository structure, manifest consistency, public-boundary rules, and other deterministic release checks implemented by the project | That either platform can fetch an unpublished repository or that SEO advice is current |
| `python3 -m unittest discover -s tests -v` | Expected behavior of the included validator and release tooling | Agent-specific discovery or remote installation |
| `claude plugin validate . --strict` | Claude marketplace structure against the installed validator | Codex compatibility or remote availability |
| `claude plugin validate ./plugins/semantic-seo-geek --strict` | Nested Claude plugin structure against the installed validator | Remote marketplace installation |
| Codex marketplace add and install | Codex can resolve and install the public repository in the tested environment | Claude compatibility or SEO outcomes |
| Claude marketplace add and install | Claude Code can resolve and install the public repository in the tested environment | Codex compatibility or SEO outcomes |

A release report should record which checks actually ran and their results. These documentation files do not claim an unrecorded pass.

## Publication-dependent commands

After the canonical repository is public, Codex users can add it with:

```bash
codex plugin marketplace add nipun-arora/semantic-seo-geek --ref main
```

Claude Code users can add it with:

```bash
claude plugin marketplace add nipun-arora/semantic-seo-geek
```

See [Installation](installation.md) for the complete command sequence.

## Other agent environments

The skill bodies are plain Markdown, but version 1 does not provide an installer, manifest, compatibility promise, or support policy for other agent environments. Portability should be tested against each environment's current skill-discovery rules before it is advertised.

Support for another environment should reuse the shared functional skills unless the platform requires a documented exception. A platform-specific copy of the workflows would create a second source of truth and is not the preferred design.

## Provider behavior is a separate compatibility question

Plugin compatibility does not make a platform-specific SEO claim current. Search features, crawler identities, structured-data requirements, and AI-assisted search behavior can change independently of the plugin manifests.

For time-sensitive recommendations, verify the current primary documentation linked in the [public source register](../plugins/semantic-seo-geek/SOURCES.md). Keep eligibility, selection, and performance as separate questions.
