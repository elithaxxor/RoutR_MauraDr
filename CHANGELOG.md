# Changelog

## [Unreleased]
### Added
- Tool wrappers for masscan, arp-scan, hydra, gvm-cli, miniupnpc, nikto, sqlmap and pgrok.
- Async tool dispatcher (`routR/tools/runner.py`).
- REST API v2 with endpoints `/api/v2/scan`, `/api/v2/report/<id>`, `/api/v2/health`.
- Tkinter GUI checkboxes and progress bars for new tools.
- GitHub Actions CI with black, pytest and shellcheck.
- Install helper scripts for apt and brew.
### Changed
- requirements updated with new dependencies.
