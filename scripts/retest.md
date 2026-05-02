# Retest scripts (`retest`)

These wrappers only **shortcut** `python -m pytest` from the **SmartTicket-IDXS repository root**. That way `conftest.py` at the repo root and the `tests/` directory are picked up the same way as when you run `pytest` manually from the root.

## Prerequisites

- Use the **same Python environment** where project dependencies are installed (ideally an **activated venv**).
- **pytest** must be installed (`pip install pytest` or via `requirements.txt`).

## `retest.bat` (Command Prompt or double-click)

From the repo root or any folder, using a relative or absolute path:

```bat
scripts\retest.bat
```

Forward extra pytest arguments (everything after the script name is passed through):

```bat
scripts\retest.bat -v
scripts\retest.bat -v --lf
scripts\retest.bat tests\test_predict.py
```

## `retest.ps1` (PowerShell)

From the repo root:

```powershell
.\scripts\retest.ps1
```

With pytest arguments:

```powershell
.\scripts\retest.ps1 -v
.\scripts\retest.ps1 -v --lf
.\scripts\retest.ps1 tests\test_predict.py
```

If you hit an **execution policy** error (`running scripts is disabled`), run once for your user:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Or use `retest.bat` instead.

## Useful pytest flags (optional)

| Flag | Effect |
|------|--------|
| `-v` | Verbose: list each test. |
| `-x` | Stop after the first failure. |
| `--lf` | Run only tests that failed last time (last failed). |
| `-k text` | Run tests whose name contains `text`. |

## Without the script

From the **repository root**:

```powershell
python -m pytest
```

Same core command; the scripts only set the correct working directory and forward arguments.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'app'`** — run from the repo root (the scripts already `cd` there) and confirm the correct venv is active.
- **`python` not found** — use your venv’s interpreter (or the full path to `python.exe`).
