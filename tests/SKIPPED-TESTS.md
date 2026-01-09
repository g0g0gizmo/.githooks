# Skipped Tests Report (pytest)

Generated: 2025-12-16

Below is a summary of all skipped tests and the reasons provided by pytest:

| Test                                                                                                         | Reason                                                                                                                   |
| ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| tests/test_applypatch_msg_check_log_message.py::test_hook_exists                                             | Script not found or not executable by Bash; skipping test.                                                               |
| tests/test_applypatch_msg_check_log_message.py::test_hook_validates_commit_message[fix: valid commit-0]      | (No explicit reason, likely related to missing script/executable.)                                                       |
| tests/test_applypatch_msg_check_log_message.py::test_hook_validates_commit_message[random message-1]         | (No explicit reason, likely related to missing script/executable.)                                                       |
| tests/test_autoversion.py::test_autoversion_hook_exists                                                      | Hook is disabled: C:\Users\jtuttle\Projects\.githooks\tests\../post-commit/autoversion-conventional-commit.hook.disabled |
| tests/test_autoversion.py::test_autoversion_hook_importable                                                  | Not a Python file; skipping import test.                                                                                 |
| tests/test_autoversion_conventional_commit.py::test_hook_exists                                              | Hook is disabled: C:\Users\jtuttle\Projects\.githooks\tests\../post-commit/autoversion-conventional-commit.hook.disabled |
| tests/test_autoversion_conventional_commit.py::test_hook_importable                                          | Hook is disabled: C:\Users\jtuttle\Projects\.githooks\tests\../post-commit/autoversion-conventional-commit.hook.disabled |
| tests/test_autoversion_conventional_commit.py::test_hook_behavior_on_commit_message[feat: add feature-True]  | Hook is disabled: C:\Users\jtuttle\Projects\.githooks\tests\../post-commit/autoversion-conventional-commit.hook.disabled |
| tests/test_autoversion_conventional_commit.py::test_hook_behavior_on_commit_message[fix: bug fix-True]       | Hook is disabled: C:\Users\jtuttle\Projects\.githooks\tests\../post-commit/autoversion-conventional-commit.hook.disabled |
| tests/test_autoversion_conventional_commit.py::test_hook_behavior_on_commit_message[docs: update docs-False] | Hook is disabled: C:\Users\jtuttle\Projects\.githooks\tests\../post-commit/autoversion-conventional-commit.hook.disabled |
| tests/test_autoversion_conventional_commit.py::test_hook_behavior_on_commit_message[random message-False]    | Hook is disabled: C:\Users\jtuttle\Projects\.githooks\tests\../post-commit/autoversion-conventional-commit.hook.disabled |
| tests/test_autoversion_conventional_commit_error.py::test_hook_missing_git                                   | (No explicit reason, likely related to missing git.)                                                                     |
| tests/test_autoversion_conventional_commit_hook.py::test_hook_exists                                         | Hook is disabled: C:/Users/jtuttle/Projects/.githooks/post-commit/autoversion-conventional-commit.hook.disabled          |
| tests/test_autoversion_conventional_commit_hook.py::test_hook_importable                                     | Hook is disabled: C:/Users/jtuttle/Projects/.githooks/post-commit/autoversion-conventional-commit.hook.disabled          |
| tests/test_classify_commit_type_by_diff.py::test_classify_commit_type_by_diff_hook_executable                | (No explicit reason, likely related to missing script/executable.)                                                       |
| tests/test_classify_commit_type_by_diff_hook.py::test_hook_importable                                        | Could not load Python module spec; skipping import test.                                                                 |
| tests/test_classify_commit_type_by_diff_hook.py::test_hook_executable                                        | (No explicit reason, likely related to missing script/executable.)                                                       |
| tests/test_commit_msg_jira.py::test_hook_executable                                                          | Bash or git not available in test environment; skipping test.                                                            |
| tests/test_commit_msg_jira.py::test_hook_validates_jira_ticket[JT_PTEAE-1234: add feature-0]                 | (No explicit reason, likely related to missing dependencies.)                                                            |
| tests/test_commit_msg_jira.py::test_hook_validates_jira_ticket[no ticket in message-1]                       | (No explicit reason, likely related to missing dependencies.)                                                            |
| tests/test_commit_msg_smart_commit_hook.py::test_hook_importable                                             | Could not load Python module spec; skipping import test.                                                                 |
| tests/test_conventional_commitlint.py::test_conventional_commitlint_hook_exists                              | (No explicit reason, likely related to missing or disabled hook.)                                                        |
| tests/test_conventional_commitlint.py::test_conventional_commitlint_hook_importable                          | (No explicit reason, likely related to missing or disabled hook.)                                                        |
| tests/test_delete_pyc_files.py::test_script_runs_without_error                                               | Not a Python file; skipping import test.                                                                                 |
| tests/test_delete_pyc_files.py::test_deletes_pyc_files                                                       | Not a Python file; skipping import test.                                                                                 |
| tests/test_delete_pyc_files_hook.py::test_hook_executable                                                    | Script not found or not executable by Bash; skipping test.                                                               |
| tests/test_dispatcher.py::test_dispatcher_hook_importable                                                    | Not a Python file; skipping import test.                                                                                 |
| tests/test_dispatcher_hook.py::test_hook_executable                                                          | Script not found or not executable by Bash; skipping test.                                                               |
| tests/test_dotenvx.py::test_dotenvx_hook_exists                                                              | Hook is disabled (.hook.disabled)                                                                                        |
| tests/test_dotenvx.py::test_dotenvx_hook_importable                                                          | Not a Python file; skipping import test.                                                                                 |
| tests/test_dotenvx_hook.py::test_hook_exists                                                                 | Hook is disabled (.hook.disabled)                                                                                        |
| tests/test_dotenvx_hook.py::test_hook_executable                                                             | Hook script not found or not executable on this platform.                                                                |
| tests/test_enforce_insert_issue_number.py::test_enforce_insert_issue_number_hook_importable                  | (No explicit reason, likely related to import error.)                                                                    |
| tests/test_format_code.py::test_format_code_hook_exists                                                      | Hook not found: C:\Users\jtuttle\Projects\.githooks\tests\../pre-commit/format-code.hook (and no .disabled version)      |
| tests/test_format_code.py::test_format_code_hook_importable                                                  | Not a Python file; skipping import test.                                                                                 |

---

**Note:** All skipped tests are due to missing, disabled, or non-executable hook scripts, missing dependencies (like Bash or git), or tests that are not Python files.

---

## Details: Skipped Tests Due to Missing Dependencies

The following tests in `test_commit_msg_jira.py` were skipped with the reason "No explicit reason, likely related to missing dependencies.":

- `tests/test_commit_msg_jira.py::test_hook_validates_jira_ticket[JT_PTEAE-1234: add feature-0]`
- `tests/test_commit_msg_jira.py::test_hook_validates_jira_ticket[no ticket in message-1]`

**Root Cause:**
These tests are parameterizations of `test_hook_validates_jira_ticket`. They are skipped if:
- The `commit-msg-jira` hook script is missing, or
- On Windows, if Bash or git is not available in the test environment.

**Skip Logic in Code:**
```python
if not os.path.isfile(HOOK_PATH):
	pytest.skip("Hook script not found; skipping test.")
if sys.platform.startswith("win"):
	git_check = subprocess.run(["bash", "-c", "which git"], ...)
	if git_check.returncode != 0:
		pytest.skip("Bash or git not available in test environment; skipping test.")
```

**Summary:**
These tests are skipped if the test environment does not have Bash and git available (common in Windows CI or minimal setups), or if the hook script is missing. The "missing dependencies" are Bash and git.

To ensure these tests run, make sure:
- Bash (e.g., Git Bash) and git are installed and available in the test environment's PATH.
- The `commit-msg-jira` hook script exists and is executable.
