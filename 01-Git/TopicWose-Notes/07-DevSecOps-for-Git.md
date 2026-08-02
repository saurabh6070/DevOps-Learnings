# DevSecOps for Git

> Adapted from [02-DevSecOps in Git.md](../02-DevSecOps%20in%20Git.md)

## 1. What is DevSecOps?

DevSecOps combines DevOps with a security-first mindset.

- Security is shifted left into development
- It applies through coding, Git, CI/CD, containers, and infrastructure

## 2. Shift Left Principle

Security checks should happen early, not only at deployment.

## 3. AI and Security

AI-generated code still needs security validation.

## 4. Threat Modeling

Threat modeling helps identify vulnerabilities before deployment.

- OWASP Threat Dragon
- STRIDE framework

## 5. Git Security Practices

### .gitignore

```gitignore
.env
*.pem
*.key
id_rsa
*.tfstate
*.tfvars
```

### Pre-commit Hooks

```bash
cd .git/hooks/
touch pre-commit
chmod +x pre-commit
```

### GitLeaks

```bash
gitleaks detect
```

### Branch Protection and Review Controls

- Branch protection rules
- Mandatory pull requests
- CODEOWNERS
- Dependabot
- Role-based access control (RBAC)

## 6. Defence in Depth

Use multiple controls together:

- .gitignore
- pre-commit hooks
- GitLeaks scans
- CI/CD checks
- branch protection
