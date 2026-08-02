# DevSecOps for Git

> Adapted from [02-DevSecOps in Git.md](../02-DevSecOps%20in%20Git.md)

This note preserves the full DevSecOps content and presents it as a complete teaching document for Git-focused engineering teams.

## 1. What is DevSecOps?

Modern software delivery is not only about speed and automation; it also requires trust and protection. DevSecOps brings security into the development pipeline from the beginning so that risks are reduced before they become expensive problems.

DevSecOps combines DevOps practices with a security-first mindset.

## 2. DevOps vs DevSecOps

Traditional DevOps often treated security as a late-stage activity. DevSecOps moves security earlier into the development lifecycle.

## 3. Shift Left Principle

The earlier a security issue is detected, the cheaper and faster it is to fix. This principle encourages teams to introduce checks during development rather than waiting until deployment.

Security must be applied from the start of development, not only before deployment.

## 4. AI and Security

AI-generated code may introduce vulnerable or outdated dependencies, so automated security checks remain essential.

## 5. Threat Modeling

Threat modeling is the practice of identifying risks before they are exploited.

### OWASP Threat Dragon

A free tool for creating visual threat models and generating reports.

### STRIDE Framework

The STRIDE model covers:

- Spoofing
- Tampering
- Repudiation
- Information Disclosure
- Denial of Service
- Elevation of Privilege

## 6. DevSecOps for Git

Git repositories often contain source code, configuration files, CI/CD definitions, and sometimes secrets. Securing Git is therefore a critical part of protecting the broader software delivery system.

Git often contains source code, CI/CD pipeline files, infrastructure definitions, and secrets. Securing Git is therefore a high priority.

### .gitignore

```gitignore
.env
*.pem
*.key
id_rsa
*.tfstate
*.tfvars
credentials
config
```

### Pre-commit Hooks

```bash
cd .git/hooks/
touch pre-commit
chmod +x pre-commit
```

### Pre-commit framework with GitLeaks

```bash
brew install pre-commit
pip install pre-commit
```

```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.24.2
    hooks:
      - id: gitleaks
```

```bash
pre-commit install
```

### GitLeaks scan commands

```bash
gitleaks detect
```

### GitLeaks in CI/CD

A GitHub Actions workflow can enforce scanning on every PR or push.

## 7. Branch Protection Rules and Pull Request Controls

Even with good local practices, a team still needs centralized controls to prevent unsafe changes from reaching the main branch. Branch protection and review policies add a safety net around collaboration.

Use branch protection, mandatory review, CODEOWNERS, and Dependabot to reduce risk.

## 8. Defence in Depth

Security should be layered using multiple controls:

- .gitignore
- pre-commit hooks
- GitLeaks
- CI/CD checks
- branch protection
- role-based access control
