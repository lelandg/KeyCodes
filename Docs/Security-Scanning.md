# Security scanning: Dependabot and zizmor specifics

Moved from the "Scanning & review" section of `AGENTS.md`, which keeps the
short list of what runs and points here; word for word except the
`automated-security-fixes` GET response, corrected in the last bullet. Policy is in
`~/.config/agents/AGENTS.md` -> "Dependencies, advisories, and scanning". "The
config above" below means `.github/dependabot.yml`.

- SHA-pinned actions get **no Dependabot alerts**: GitHub generates them only
  for actions on semantic versions (docs: "About Dependabot alerts"). So no
  security-update PR can ever fire for a pinned action, an
  `applies-to: security-updates` group over github-actions is dead config, and
  the weekly version update is their only automatic remediation -- which is why
  the github-actions block carries no semver-major ignore. DETECTION comes
  from the `zizmor` job in `security.yml`: it maps each SHA pin to its
  release tag and fails on a known-vulnerable, impostor or unpinned action.
  osv-scanner's `github/actions` plugin only lists the pinned actions: with
  osv-scanner 2.7.0 it did not flag `tj-actions/changed-files`
  (GHSA-mrrh-fwg8-r2c3) at a vulnerable SHA or tag. zizmor looks up a SHA
  pin by one tag: for a root action (owner/repo@sha) the longest tag
  without a `/`, for a sub-action the longest tag under its path or its
  last directory (else the longest of all). The job fails unless that tag, and any tag tied
  with it, is a plain release version (v1, v1.2.3): an untagged commit,
  a non-version tag or a path-prefixed tag matches no advisory. Pin
  released versions.
- Dependabot **alerts** are a per-repo GitHub setting; a config file does not
  turn them on. Without them the config above governs version updates only.
  Check it by HTTP STATUS, not by exit code -- `gh api` exits 0 on success
  and 1 on any failure, and never exits 404 or 403:
  `gh api -i -X GET repos/lelandg/KeyCodes/vulnerability-alerts | head -1`
  204 = on, 403 = the token has no admin on this repo (NOT the same as off),
  404 = off only when an admin token gets it: GitHub also answers 404 to a
  token without the permission, so confirm with an admin token first. Enable: same path with `-X PUT`.
- Alerts and automatic security **updates** are two switches, not one. Alerts
  only report; the half that opens PRs is `automated-security-fixes` (same
  path shape and the same `-X PUT` to enable, but its GET answers differently:
  HTTP 200 with a JSON body, `"enabled": true` or `false`, plus `paused` --
  never 204, so read the body, not the status line:
  `gh api -X GET repos/lelandg/KeyCodes/automated-security-fixes`).
  It is deliberately OFF here: this repo took its first scan with a
  pre-existing advisory backlog, and enabling it would open that backlog as
  PRs at once. Turn it on per repo once the backlog is cleared.
