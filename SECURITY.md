# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.x     | Yes       |

## Reporting a vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Please report via GitHub Security Advisories on this repository, or email the
maintainers if an advisory channel is unavailable.

Include:

* Description of the issue
* Steps to reproduce
* Impact assessment
* Any suggested fix

We aim to acknowledge reports within 7 days.

## Security practices

* Never commit secrets, API keys, or credentials
* API keys are hashed (SHA-256 + pepper) before storage
* Rate limiting is enforced for anonymous and authenticated clients
* Dependencies should be pinned; CI runs basic security checks
* Containers run as non-root users

## Out of scope

* Denial of service via intentional rate-limit exhaustion on local/dev deployments
* Issues that only apply when `DEBUG=true` or `MOCK_MODE=true` in production
  (do not run production with those settings)
