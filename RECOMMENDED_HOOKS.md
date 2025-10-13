# Recommended Hooks Additions

This repository includes a dispatcher-based pre-commit runner. The following additions bolster day-to-day safety and developer ergonomics. All new hooks live under `pre-commit/` and are executed by `dispatcher.py` in filename order.

## Added in this update

- trailing-whitespace.hook — trims trailing spaces in staged text files.
- end-of-file-fixer.hook — ensures files end with a single `\n`.
- mixed-line-ending.hook — normalizes CRLF/LF to LF in text files.
- check-merge-conflict.hook — blocks unresolved conflict markers.
- check-added-large-files.hook — blocks newly added files over 500 KB (edit threshold in file).
- check-json.hook — JSON syntax check.
- check-toml.hook — TOML syntax check (uses `tomllib` or `tomli`).
- check-yaml.hook — YAML syntax/policy (uses `yamllint` if available, else `PyYAML`).
- shellcheck.hook — runs ShellCheck on shell scripts via `shellcheck-py`.
- detect-secrets.hook — enforces `.secrets.baseline` using `detect-secrets` to block new secrets.

## One-time setup for secrets

```powershell
python -m pip install detect-secrets
detect-secrets scan > .secrets.baseline
detect-secrets audit .secrets.baseline
```

Commit the baseline and re-run the commit.

## Windows notes

- ShellCheck is provided via the `shellcheck-py` wheel, so no external binary installation is required.
- `yamllint` is optional but recommended; hook falls back to `PyYAML` syntax validation.

## Customization

- Large file threshold: edit `MAX_KB` in `check-added-large-files.hook`.
- To disable any hook, rename the file extension or remove the `.hook` file.
- Ordering: hooks execute in lexicographic order; prefix filenames to adjust ordering if necessary.
