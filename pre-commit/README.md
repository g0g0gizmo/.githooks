## pre commit 

This hook is called before obtaining the proposed commit message. Exiting with anything other than zero will abort the commit. It is used to check the commit itself (rather than the message).

## invoked by 

```bash
git commit
```

## pre commit git hooks for:

* **dotenvx.hook** - Environment variable validation hook
* **format-code.hook** - Code formatting hook  
* **search-term.hook** - Search for prohibited terms in code
* **spell-check-md-files.hook** - Spell check markdown files
* **verify-name-and-email.hook** - Verify Git user name and email configuration

## support

If you have a question, find a bug, or just want to say hi, please open an [issue on GitHub](https://github.com/aitemr/awesome-git-hooks/issues/new). 

## license

[![CC0](http://mirrors.creativecommons.org/presskit/buttons/88x31/svg/cc-zero.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

To the extent possible under law, [Islam Temirbek](https://aitemr.github.io) has waived all copyright and related or neighboring rights to this work.