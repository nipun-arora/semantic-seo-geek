# Install Semantic SEO Geek in Codex or Claude Code

Semantic SEO Geek version 1 uses one shared set of skills with separate manifests for Codex and Claude Code. Choose the installer for your agent environment.

The remote commands in this guide require <https://github.com/nipun-arora/semantic-seo-geek> to be publicly available. Before publication, use the local validation steps from a release candidate checkout instead.

## Before you install

- Read the [license summary](license.md) and the governing [`LICENSE`](../LICENSE).
- Confirm that your Codex or Claude Code installation supports plugins.
- Start a new agent session after installation so the environment can discover the skills.

A workflow may ask for files, URLs, reports, or supporting references needed for the task you give it.

## Install in Codex

Add the canonical GitHub repository as a plugin marketplace:

```bash
codex plugin marketplace add nipun-arora/semantic-seo-geek --ref main
```

Install the plugin from that marketplace:

```bash
codex plugin add semantic-seo-geek@semantic-seo-geek
```

Confirm that Codex can list the marketplace entry:

```bash
codex plugin list --available --json
```

Start a new Codex session after installation.

These repository-based commands depend on the public GitHub repository. They cannot complete against an unpublished local release candidate.

## Install in Claude Code

Add the canonical GitHub repository as a plugin marketplace:

```bash
claude plugin marketplace add nipun-arora/semantic-seo-geek
```

Install the plugin from that marketplace:

```bash
claude plugin install semantic-seo-geek@semantic-seo-geek
```

Start a new Claude Code session, or reload the active session, after installation.

These commands also depend on the public GitHub repository.

## Validate a local release candidate

From the repository root, run the deterministic repository checks:

```bash
python3 scripts/validate.py check
python3 -m unittest discover -s tests -v
```

If Claude Code is installed, validate both the marketplace and nested plugin manifests:

```bash
claude plugin validate . --strict
claude plugin validate ./plugins/semantic-seo-geek --strict
```

These are local validation commands. They do not prove that a remote marketplace install works, and this guide does not claim that a command passed unless the accompanying release report records that result.

The maintainers run Codex and Claude installation smoke tests before a release. Remote smoke tests remain publication-dependent because both installers must resolve the canonical GitHub repository.

## Confirm the workflows are visible

In a new session, ask the agent to identify the Semantic SEO Geek skills or give it a task that clearly matches one of them, such as:

```text
Use the Semantic SEO Geek technical SEO workflow to review these crawl directives.
```

If the plugin is not visible:

1. confirm that the marketplace-add and plugin-install commands completed without an error;
2. confirm that the installed marketplace and plugin names are both `semantic-seo-geek`;
3. start a new session or reload the current one; and
4. inspect your agent's plugin listing or validation output before changing the package files.

Do not treat a successful manifest validation as proof that every platform behavior or SEO recommendation is current. Time-sensitive provider claims still require current primary documentation.

## Security reports

Report a vulnerability through GitHub private vulnerability reporting for the [canonical repository](https://github.com/nipun-arora/semantic-seo-geek). Do not place unpatched vulnerabilities or leaked credentials in a public issue. See the [security policy](../SECURITY.md).

## Official platform documentation

- [Codex plugins](https://developers.openai.com/plugins/build/plugins)
- [Codex skills](https://developers.openai.com/plugins/build/skills)
- [Claude Code plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Claude Code plugin reference](https://code.claude.com/docs/en/plugins-reference)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
