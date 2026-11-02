# KeyCodes

Two standalone GUI utilities that show the keycode a framework reports when you press a key. PyQt5 and Pygame return different values for the same key. Users run the script that matches their framework.

## Gotchas

- Both scripts need a display. Under WSL, run them from Windows/PowerShell, or with a working WSLg/X server.
- `LICENSE` (0BSD) is authoritative. The `__license__` strings inside the scripts are stale and do not match it.

## Conventions

- `_version.py` is the single source of the version string. Do not set a version anywhere else.
- Keep the two scripts behaviorally consistent: print each event to the console and the window, and quit on double-Esc (any other key resets the Esc counter).
- The scripts share no code beyond `_version.py`. Keep each one self-contained.

## Build / test

- No tests, no linter config, no build step.

## Scanning & review

Policy lives in `~/.config/agents/AGENTS.md` -> "Dependency, code, and secret
scanning" and "Model delegation & cross-provider review". It is not restated
here; read it there. What is specific to this repo:

- CI runs `gitleaks` and `osv-scanner` on every PR, every push to `main`, and
  weekly (`.github/workflows/security.yml`). The npm jobs from the shared
  workflow are deliberately absent: there is no committed `package-lock.json`,
  so `npm ci` cannot run and the check would be permanently red.
- Dependabot config is committed, with grouped security PRs (`.github/dependabot.yml`),
  covering `pip` (`requirements.txt`) and `github-actions`.
- Dependabot **alerts** are a per-repo GitHub setting; a config file does not
  turn them on. Without them the config above governs version updates only.
  Check: `gh api -X GET repos/lelandg/KeyCodes/vulnerability-alerts` -- exit 0 = on,
  404 = off, and **403 = the token has no admin on this repo**, which is not
  the same as off. Enable: same path with `-X PUT`.
- Alerts and automatic security **updates** are two switches, not one. Alerts
  only report; the half that opens PRs is `automated-security-fixes` (same API
  shape). It is deliberately OFF here: this repo took its first scan with a
  pre-existing advisory backlog, and enabling it would open that backlog as
  PRs at once. Turn it on per repo once the backlog is cleared.
- PR reviewers configured for this repo: **Codex** (run locally against the
  committed branch before opening the PR) and **CodeRabbit**
  (`coderabbitai[bot]`). How to read their checks -- which one re-reviews a
  push, why a green check does not mean "no findings", and which label skips
  which bot -- is in the global policy cited above and is deliberately not
  repeated here.
