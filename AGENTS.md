# KeyCodes

Two standalone GUI utilities that show the keycode a framework reports when you press a key. Qt (PySide6) and Pygame return different values for the same key. Users run the script that matches their framework.

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

Policy lives in `~/.config/agents/AGENTS.md` -> "Dependencies, advisories, and
scanning", "Shipping autonomy" (the review council) and "Model delegation &
cross-provider review". It is not restated here; read it there. What is
specific to this repo:

- CI runs `gitleaks`, `osv-scanner` and `zizmor` on every PR, every push to `main`, and
  weekly (`.github/workflows/security.yml`). The shared workflow's two npm jobs are present but skip with
  a notice, because there is no root `package-lock.json`.
- Dependabot config is committed (`.github/dependabot.yml`): `pip`
  (`requirements.txt`) gets grouped security PRs plus grouped version updates;
  `github-actions` gets version updates only (why: `Docs/Security-Scanning.md`).
- Dependabot/zizmor specifics for this repo (pinned actions get no alerts, how
  to check the alerts switch, why automated-security-fixes is off):
  `Docs/Security-Scanning.md`.
- **PR reviewers.** The review council in the global rules applies here; its
  members are whatever `~/.config/agents/council.toml` seats, and the runner
  and commands are in `~/.claude/instructions/model-delegation.md`. This repo
  adds **CodeRabbit** (`coderabbitai[bot]`, configured in `.coderabbit.yaml`):
  automatic on every non-draft PR, it re-reviews every push, skips
  `dependabot[bot]` and `renovate[bot]`, and is skipped by the `no-ai-review`
  label, which must be on the PR when the review fires. The list is additive,
  not closed: nothing named here replaces a council member. A green
  `CodeRabbit` check does not mean "no findings", or even that a review ran:
  read the check's output title and the inline comments. How, and the rest of
  the bot's behaviour, is in the comments in `.coderabbit.yaml` and in
  `~/.claude/instructions/pr-review-automation.md`; it is deliberately not
  repeated here.
