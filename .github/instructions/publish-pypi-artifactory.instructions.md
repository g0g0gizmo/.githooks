
---
description: 'Complete guide for building and publishing Python packages to Viasat Artifactory PyPI repository'
applyTo: '**/*.py, **/pyproject.toml, **/setup.py, **/.pypirc'
status: Active
---

# Publishing PyPI Packages to Artifactory

Complete guide for building, configuring, and publishing Python packages to the Viasat Artifactory PyPI repository.

**Repository Base URL**: `https://artifactory.viasat.com/artifactory/api/pypi/`

## Prerequisites

- Python 3.7+
- Build tools: `setuptools >= 45`, `wheel`, `twine >= 3.4`
- Artifactory account with deploy permissions to your target repository
- Artifactory API key or username/password (use environment variables, never hardcode)
- Network access to `artifactory.viasat.com`

## 0. Create the Artifactory PyPI Repository (if not present)

If your Artifactory PyPI repository does not exist, you must create it first. **Admin permissions required.**

## Option 1: Using the Artifactory Web UI

1. Log in to [Artifactory](https://artifactory.viasat.com/).
2. Go to **Admin** > **Repositories** > **Repositories** > **Local**.
3. Click **New** and select **PyPI** as the package type.
4. Enter a repository key (e.g., `my-pypi-repo`).
5. Configure permissions, storage, and other settings as needed.
6. Click **Save & Finish**.

## Option 2: Using the Artifactory REST API

Create a repository via API (requires admin API key):

```bash
ADMIN_USER="your-admin-user"
ADMIN_API_KEY="your-admin-api-key"
REPO_NAME="my-pypi-repo"

curl -u "$ADMIN_USER:$ADMIN_API_KEY" -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "rclass": "local",
    "packageType": "pypi",
    "repoLayoutRef": "simple-default"
  }' \
  "https://artifactory.viasat.com/artifactory/api/repositories/$REPO_NAME"
```

**Success Response**: HTTP 201 Created

---

## 1. Build the Package

Ensure your project has a `pyproject.toml` or `setup.py` with version, name, and description.

```bash
# Modern build (recommended)
python -m build

# Or, using legacy setup.py
python setup.py sdist bdist_wheel
```

Built artifacts appear in `dist/` directory (source distribution `.tar.gz` and wheel `.whl`).

**Verify the build**:
```bash
ls -la dist/
```

## 2. Set Up Environment Variables (Recommended)

Store credentials securely using environment variables instead of hardcoding in config files:

```bash
# Linux/macOS (add to ~/.bashrc or ~/.zshrc)
export ARTIFACTORY_USERNAME="your-username"
export ARTIFACTORY_PASSWORD="your-api-key-or-password"
export ARTIFACTORY_REPO="my-pypi-repo"

# Windows (PowerShell)
[Environment]::SetEnvironmentVariable("ARTIFACTORY_USERNAME", "your-username", "User")
[Environment]::SetEnvironmentVariable("ARTIFACTORY_PASSWORD", "your-api-key-or-password", "User")
[Environment]::SetEnvironmentVariable("ARTIFACTORY_REPO", "my-pypi-repo", "User")
```

**Never commit credentials to version control.** Add `.pypirc` to `.gitignore` if using it.

## 3. Configure PyPI Repository

Create or edit `~/.pypirc` for credential management:

```ini
[distutils]
index-servers =
    pypi-artifactory

[pypi-artifactory]
repository = https://artifactory.viasat.com/artifactory/api/pypi/my-pypi-repo
username = __env__:ARTIFACTORY_USERNAME
password = __env__:ARTIFACTORY_PASSWORD
```

Alternatively, use environment variables directly in the publish command (see Step 4).

## 4. Publish to Artifactory

### Option A: Using Twine (Recommended)

```bash
twine upload dist/* \
  --repository-url https://artifactory.viasat.com/artifactory/api/pypi/$ARTIFACTORY_REPO \
  -u $ARTIFACTORY_USERNAME \
  -p $ARTIFACTORY_PASSWORD
```

### Option B: Using .pypirc Configuration

If you've configured `~/.pypirc` (Step 3), publish with:

```bash
twine upload dist/* --repository pypi-artifactory
```

### Option C: Using Custom Script or Tool

If your organization has a custom publish tool:

```bash
publish -r $ARTIFACTORY_REPO --build
```

### Verify Upload

After publishing, verify in Artifactory:

```bash
curl -u $ARTIFACTORY_USERNAME:$ARTIFACTORY_PASSWORD \
  https://artifactory.viasat.com/artifactory/api/storage/my-pypi-repo/ | jq .
```

## 5. CI/CD Integration

### GitHub Actions Example

```yaml
name: Publish to Artifactory

on:
  release:
    types: [created]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install build twine
      - run: python -m build
      - run: twine upload dist/* \
          --repository-url https://artifactory.viasat.com/artifactory/api/pypi/${{ secrets.ARTIFACTORY_REPO }} \
          -u ${{ secrets.ARTIFACTORY_USERNAME }} \
          -p ${{ secrets.ARTIFACTORY_PASSWORD }}
```

**Store these as GitHub Secrets**: `ARTIFACTORY_REPO`, `ARTIFACTORY_USERNAME`, `ARTIFACTORY_PASSWORD`

## 6. Troubleshooting

| Issue                      | Solution                                                               |
| -------------------------- | ---------------------------------------------------------------------- |
| **401 Unauthorized**       | Verify username/API key and permissions in Artifactory                 |
| **403 Forbidden**          | Check that your user has deploy rights to the repository               |
| **404 Not Found**          | Repository doesn't exist; see Step 0 to create it                      |
| **SSL Certificate Error**  | Verify CA certificates are up-to-date: `pip install --upgrade certifi` |
| **Package already exists** | Update version in `pyproject.toml` or `setup.py`                       |
| **Network timeout**        | Check VPN connection and network access to Artifactory                 |

## 7. Security Best Practices

- ✅ **Use API keys** instead of passwords when possible
- ✅ **Rotate credentials** regularly
- ✅ **Store secrets** in environment variables or CI/CD secret managers
- ✅ **Add `.pypirc` to `.gitignore`** if storing credentials in files
- ✅ **Use HTTPS only** for all connections
- ✅ **Restrict repository permissions** to least-privilege access
- ❌ Never commit credentials to version control
- ❌ Never share API keys in chat, email, or documentation

## References

- [Artifactory PyPI Repositories](https://jfrog.com/help/r/jfrog-artifactory-documentation/pypi-repositories)
- [Twine Documentation](https://twine.readthedocs.io/en/stable/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [PEP 517 – Build System Interface](https://peps.python.org/pep-0517/)

---

**Last Updated**: 2025-12-15
