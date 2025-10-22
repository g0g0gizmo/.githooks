
import subprocess
import sys

import click

LANG_PATTERNS = {
    "python": (".py",),
    "javascript": (".js", ".jsx", ".mjs", ".cjs"),
    "typescript": (".ts", ".tsx"),
    "shell": (".sh", ".bash", ".zsh", ".ksh", ".csh"),
    "perl": (".pl", ".pm", ".t"),
    "json": (".json",),
    "yaml": (".yaml", ".yml"),
    "toml": (".toml",),
    "markdown": (".md",),
    "labview": (
        ".vi",
        ".vim",
        ".vit",
        ".ctl",
        ".ctt",
        ".lvclass",
        ".lvlib",
        ".lvproj",
        ".lvlibp",
    ),
}


def run_perl(files):
    if not files:
        return 0
    # Prefer perlcritic for lint, perltidy for format
    if which("perlcritic"):
        r = run(["perlcritic", *files])
        if r.returncode != 0:
            return r.returncode
    if which("perltidy"):
        for f in files:
            run(["perltidy", "-b", f])
    return 0


def run(cmd, cwd=None, check=False):
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True)


def get_staged_files():
    r = subprocess.run(
        [
            "git",
            "diff",
            "--cached",
            "--name-only"
        ],
        capture_output=True,
        text=True
    )
    if r.returncode != 0:
        return []
    return [line.strip() for line in r.stdout.splitlines() if line.strip()]


def group_by_language(files):
    groups = {k: [] for k in LANG_PATTERNS}
    for f in files:
        low = f.lower()
        for lang, exts in LANG_PATTERNS.items():
            if any(low.endswith(ext) for ext in exts):
                groups[lang].append(f)
                break
    return groups


def which(cmd):
    from shutil import which as _which

    return _which(cmd)


def run_python(files):
    if not files:
        return 0
    # isort then black then flake8
    if which("isort"):
        run(["isort", "--filter-files", *files])
    if which("black"):
        run(["black", "--quiet", *files])
    if which("flake8"):
        r = run(["flake8", *files])
        if r.returncode != 0:
            return r.returncode
    return 0


def run_js_ts(js_files, ts_files):
    files = js_files + ts_files
    if not files:
        return 0
    # Prefer prettier if available
    if which("npx"):
        run([
            "npx",
            "--no-install",
            "prettier",
            "--write",
            *files
        ])
        # eslint for linting if present
        run([
            "npx",
            "--no-install",
            "eslint",
            "--max-warnings",
            "0",
            *files
        ])
    return 0


def run_shell(files):
    if not files:
        return 0
    # shellcheck via shellcheck-py provides shellcheck executable on PATH when venv active
    if which("shellcheck"):
        for f in files:
            arg0 = "shellcheck"
            arg1 = f
            run([arg0, arg1])
    return 0


def run_json(files):
    # Validation is enforced by existing hooks; here we just prettify with jq if available
    if not files:
        return 0
    if which("jq"):
        for f in files:
            arg0 = "jq"
            arg1 = "."
            arg2 = f
            run([arg0, arg1, arg2])
    return 0


def run_yaml(files):
    if not files:
        return 0
    if which("yamllint"):
        for f in files:
            arg0 = "yamllint"
            arg1 = f
            r = run([arg0, arg1])
            if r.returncode != 0:
                return r.returncode
    return 0


def run_toml(files):
    return 0


def run_markdown(files):
    # Prettier formats markdown if available
    if not files:
        return 0
    if which("npx"):
        run([
            "npx",
            "--no-install",
            "prettier",
            "--write",
            *files
        ])
    return 0


def run_labview(files):
    # Defer heavy lifting to the dedicated LV hooks; we only ensure the warning hook fires
    return 0


@click.command()
@click.option(
    "--staged-only", is_flag=True, default=True, help="Operate only on staged files"
)
def main(staged_only):
    files = get_staged_files() if staged_only else []
    groups = group_by_language(files)
    status = 0
    status |= run_python(groups["python"])
    status |= run_js_ts(
        groups["javascript"],
        groups["typescript"]
    )
    status |= run_shell(groups["shell"])
    status |= run_perl(groups["perl"])
    status |= run_json(groups["json"])
    status |= run_yaml(groups["yaml"])
    status |= run_toml(groups["toml"])
    status |= run_markdown(groups["markdown"])
    status |= run_labview(groups["labview"])
    exit_code = 0 if status == 0 else 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
