.githooks/
├── githooks/               # Main package (was: lib/)
│   ├── **init**.py
│   ├── cli/               # CLI commands as subpackage
│   │   ├── **init**.py
│   │   ├── start.py
│   │   ├── finish.py
│   │   ├── publish.py
│   │   ├── status.py
│   │   └── commitmint.py
│   ├── hooks/             # Hook implementation modules
│   │   ├── **init**.py
│   │   ├── jira_add_push_worklog.py
│   │   ├── jira_transition_worklog.py
│   │   ├── jira_feature_instructions.py
│   │   └── popup_error.py
│   └── core/              # Shared utilities (was: lib/)
│       ├── **init**.py
│       ├── constants.py
│       ├── git_config.py
│       ├── git_operations.py
│       ├── github_utils.py
│       ├── jira_client.py
│       ├── jira_helpers.py
│       ├── output.py
│       ├── repo_helpers.py
│       └── utils.py
├── install.py             # Installer (stays at root - it's a tool, not part of package)
├── git-go                 # CLI dispatcher (stays at root - backwards compat)
├── pyproject.toml         # Add [project.scripts] entry points
└── pre-commit/, post-commit/, etc.  # Hook directories (unchanged)
