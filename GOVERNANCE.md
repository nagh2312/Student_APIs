# Governance

## Principles

1. **Student usefulness first** — APIs must solve real student project needs.
2. **Standards over sprawl** — Prefer fewer, well-designed APIs over many inconsistent ones.
3. **Open data legality** — No dataset without a clear, redistributable license.
4. **Provider independence** — Consumer contracts must not leak provider formats.
5. **Transparent maintenance** — Every API has an owner, tests, and documented sources.

## API review process

New APIs require a GitHub issue using the **New API Proposal** template and review against:

* Usefulness / roadmap score
* Standardization potential
* Open data availability and license
* Security and privacy
* Maintenance cost
* Developer experience (docs, mock mode, examples)

Approval is required from at least one maintainer before merge of a new public module.

## Status levels

| Status | Meaning |
|--------|---------|
| experimental | May change without notice |
| beta | Mostly stable; minor breaking changes possible with changelog |
| stable | Breaking changes require `/v2` |
| deprecated | Scheduled for removal; migration path documented |

## Maintainers

Maintainers are listed in the GitHub repository settings / CODEOWNERS (when configured).
