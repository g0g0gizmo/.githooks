---
description: 'Prompt for publishing Python packages to Viasat Artifactory PyPI repository'
tags: ['python', 'pypi', 'artifactory', 'publishing', 'ci-cd']
variables:
  - name: PACKAGE_NAME
    description: 'Name of the Python package to publish'
    example: 'my-awesome-package'
  - name: PACKAGE_VERSION
    description: 'Version of the package (e.g., 1.0.0)'
    example: '1.0.0'
  - name: ARTIFACTORY_REPO
    description: 'Name of the Artifactory PyPI repository'
    example: 'my-pypi-repo'
  - name: ARTIFACTORY_USERNAME
    description: 'Artifactory username (use environment variable in production)'
    example: 'your-username'
  - name: ARTIFACTORY_PASSWORD
    description: 'Artifactory API key or password (use environment variable in production)'
    example: '${ARTIFACTORY_PASSWORD}'
  - name: ARTIFACTORY_BASE_URL
    description: 'Base URL of Artifactory PyPI API'
    default: 'https://artifactory.viasat.com/artifactory/api/pypi'
    example: 'https://artifactory.viasat.com/artifactory/api/pypi'
---

# Publish Python Package to Artifactory

## Task

Publish a Python package (`{{PACKAGE_NAME}}` v{{PACKAGE_VERSION}}) to the Viasat Artifactory PyPI repository at `{{ARTIFACTORY_REPO}}`.

## Prerequisites

- ✅ Python 3.7+ installed
- ✅ Build tools installed: `setuptools >= 45`, `wheel`, `twine >= 3.4`
- ✅ Artifactory account with deploy permissions
- ✅ Network access to `{{ARTIFACTORY_BASE_URL}}`
- ✅ `{{PACKAGE_NAME}}` source code ready with `pyproject.toml` or `setup.py`

## Step 1: Build the Package

Ensure `pyproject.toml` or `setup.py` contains:

- **name**: `{{PACKAGE_NAME}}`
- **version**: `{{PACKAGE_VERSION}}`
- **description**: Concise package description

```bash
# Build distribution artifacts
python -m build
# Output: dist/{{PACKAGE_NAME}}-{{PACKAGE_VERSION}}.tar.gz and dist/{{PACKAGE_NAME}}-{{PACKAGE_VERSION}}-py3-*.whl

# Verify build
ls -la dist/
```

## Step 2: Set Up Environment Variables

```bash
# Linux/macOS
export ARTIFACTORY_USERNAME="{{ARTIFACTORY_USERNAME}}"
export ARTIFACTORY_PASSWORD="{{ARTIFACTORY_PASSWORD}}"
export ARTIFACTORY_REPO="{{ARTIFACTORY_REPO}}"

# Windows (PowerShell)
[Environment]::SetEnvironmentVariable("ARTIFACTORY_USERNAME", "{{ARTIFACTORY_USERNAME}}", "User")
[Environment]::SetEnvironmentVariable("ARTIFACTORY_PASSWORD", "{{ARTIFACTORY_PASSWORD}}", "User")
[Environment]::SetEnvironmentVariable("ARTIFACTORY_REPO", "{{ARTIFACTORY_REPO}}", "User")
```

## Step 3: Configure `.pypirc` (Optional)

Create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi-artifactory

[pypi-artifactory]
repository = {{ARTIFACTORY_BASE_URL}}/{{ARTIFACTORY_REPO}}
username = __env__:ARTIFACTORY_USERNAME
password = __env__:ARTIFACTORY_PASSWORD
```

## Step 4: Publish to Artifactory

### Option A: Using Twine with Environment Variables (Recommended)

```bash
twine upload dist/* \
  --repository-url {{ARTIFACTORY_BASE_URL}}/$ARTIFACTORY_REPO \
  -u $ARTIFACTORY_USERNAME \
  -p $ARTIFACTORY_PASSWORD
```

### Option B: Using `.pypirc` Configuration

```bash
twine upload dist/* --repository pypi-artifactory
```

## Step 5: Verify Upload

```bash
# Check artifact in Artifactory
curl -u $ARTIFACTORY_USERNAME:$ARTIFACTORY_PASSWORD \
  {{ARTIFACTORY_BASE_URL}}/{{ARTIFACTORY_REPO}}/simple/{{PACKAGE_NAME}}/ | grep -i "{{PACKAGE_VERSION}}"

# Or query via API
curl -u $ARTIFACTORY_USERNAME:$ARTIFACTORY_PASSWORD \
  {{ARTIFACTORY_BASE_URL}}/{{ARTIFACTORY_REPO}}/simple/{{PACKAGE_NAME}}/
```

## Troubleshooting

| Error                      | Solution                                                                  |
| -------------------------- | ------------------------------------------------------------------------- |
| **401 Unauthorized**       | Verify `ARTIFACTORY_USERNAME` and `ARTIFACTORY_PASSWORD` are correct      |
| **403 Forbidden**          | Confirm user has deploy permissions to `{{ARTIFACTORY_REPO}}`             |
| **404 Not Found**          | Repository `{{ARTIFACTORY_REPO}}` doesn't exist; create it first          |
| **Package already exists** | Update version in `pyproject.toml` or `setup.py` to `{{PACKAGE_VERSION}}` |
| **SSL Certificate Error**  | Run: `pip install --upgrade certifi`                                      |
| **Network timeout**        | Check VPN and network access to `{{ARTIFACTORY_BASE_URL}}`                |

## Security Notes

- ✅ Always use environment variables for credentials (never hardcode)
- ✅ Use API keys instead of passwords when possible
- ✅ Add `.pypirc` to `.gitignore` if storing credentials locally
- ✅ Rotate credentials regularly
- ❌ Never commit credentials to version control
- ❌ Never share API keys in chat, email, or documentation

## Next Steps

1. Package successfully published to `{{ARTIFACTORY_REPO}}`
2. Verify availability in Artifactory web UI
3. Update project documentation with installation instructions
4. Tag release in Git: `git tag v{{PACKAGE_VERSION}} && git push origin v{{PACKAGE_VERSION}}`
5. Consider adding CI/CD automation (see `publish-pypi-artifactory.instructions.md` for GitHub Actions example)

---

**Reference**: See [publish-pypi-artifactory.instructions.md](../instructions-wip/publish-pypi-artifactory.instructions.md) for complete guide and advanced options.
