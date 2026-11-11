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
  weekly (`.github/workflows/security.yml`). The shared workflow's two npm jobs are present but skip with
  a notice, because there is no root `package-lock.json`.
- Dependabot config is committed (`.github/dependabot.yml`): `pip`
  (`requirements.txt`) gets grouped security PRs plus grouped version updates;
  `github-actions` gets version updates only (see the next point).
- SHA-pinned actions get **no Dependabot alerts**: GitHub generates them only
  for actions on semantic versions (docs: "About Dependabot alerts"). So no
  security-update PR can ever fire for a pinned action, an
  `applies-to: security-updates` group over github-actions is dead config, and
  the weekly version update is their only automatic remediation -- which is why
  the github-actions block carries no semver-major ignore. The only detection
  is osv-scanner's `github/actions` plugin (not a default, so `security.yml`
  names it), and it is weak: checked 2026-11-11 with osv-scanner 2.7.0, it did
  not flag `tj-actions/changed-files` (GHSA-mrrh-fwg8-r2c3) at a vulnerable
  SHA or at a vulnerable tag. Read an action's advisories before approving its
  bump; a clean osv-scanner run does not clear an action.
- Dependabot **alerts** are a per-repo GitHub setting; a config file does not
  turn them on. Without them the config above governs version updates only.
  Check it by HTTP STATUS, not by exit code -- `gh api` exits 0 on success
  and 1 on any failure, and never exits 404 or 403:
  `gh api -i -X GET repos/lelandg/KeyCodes/vulnerability-alerts | head -1`
  204 = on, 403 = the token has no admin on this repo (NOT the same as off),
  404 = off only when an admin token gets it: GitHub also answers 404 to a
  token without the permission, so confirm with an admin token first. Enable: same path with `-X PUT`.
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
