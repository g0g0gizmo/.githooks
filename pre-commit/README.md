
## pre commit

This hook is called before obtaining the proposed commit message. Exiting with anything other than zero will abort the commit. It is used to check the commit itself (rather than the message).

## invoked by 

```bash
git commit
```


## pre commit git hooks for:

* **block-labview-binaries.hook** - Blocks common LabVIEW binary files from being committed (e.g., .aliases, .lvlps, .lvbitx, .lvappimg, .lvuser, .lvmodel, .lvsc, .lvxlib, .lvlibp, .lvbit, .lvappimgx, .lvtest, .lvproj, .ctt)
* **lv-diff-report.hook** - Generates LVCompare reports for staged LabVIEW files by diffing against HEAD (requires LVCompare.exe)
* **warn-if-lv-hooks-missing.hook** - Warns if LabVIEW files are staged but LabVIEW Git Hooks are not installed
* **dotenvx.hook** - Environment variable validation hook
* **format-code.hook** - Code formatting hook
* **search-term.hook** - Search for prohibited terms in code
* **spell-check-md-files.hook** - Spell check markdown files
* **verify-name-and-email.hook** - Verify Git user name and email configuration


## LabVIEW-specific notes

LabVIEW projects benefit from the following hooks:

- **block-labview-binaries.hook**: Prevents accidental commits of LabVIEW-generated binary artifacts. Add these files to your .gitignore for best results.
- **lv-diff-report.hook**: If LVCompare.exe is available, generates HTML diff reports for staged LabVIEW files. Reports are saved under .lvcompare-reports/.
- **warn-if-lv-hooks-missing.hook**: Notifies you if LabVIEW files are staged but LabVIEW-specific hooks are not installed.

For more advanced LabVIEW automation, see https://gitlab.com/felipe_public/lv-git-hooks

If you have a question, find a bug, or just want to say hi, please open an [issue on GitHub](https://github.com/aitemr/awesome-git-hooks/issues/new). 

## license

[![CC0](http://mirrors.creativecommons.org/presskit/buttons/88x31/svg/cc-zero.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

To the extent possible under law, [Islam Temirbek](https://aitemr.github.io) has waived all copyright and related or neighboring rights to this work.