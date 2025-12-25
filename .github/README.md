# GitHub Repository Setup

This directory contains GitHub-specific configuration files for the production-ml-system repository.

## Files

- `ISSUE_TEMPLATE/` - Issue templates for bug reports and feature requests
- `PULL_REQUEST_TEMPLATE.md` - PR template
- `workflows/` - GitHub Actions workflows
  - `ci.yml` - Continuous Integration
  - `codeql.yml` - Security analysis
  - `docker-publish.yml` - Docker image publishing
  - `release.yml` - Release automation
- `dependabot.yml` - Automated dependency updates
- `CODE_OF_CONDUCT.md` - Community guidelines
- `SECURITY.md` - Security policy

## Repository Settings

To fully enable all features:

1. **Enable GitHub Actions**: Settings → Actions → Allow all actions
2. **Enable Dependabot**: Settings → Security → Dependabot alerts
3. **Enable Discussions**: Settings → General → Features → Discussions
4. **Set up Secrets** (if needed):
   - Settings → Secrets → Actions
   - Add any required API keys or tokens

## Badges

Add these badges to your README (update URLs):

```markdown
![CI](https://github.com/yourusername/production-ml-system/workflows/CI/badge.svg)
![CodeQL](https://github.com/yourusername/production-ml-system/workflows/CodeQL/badge.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
```

