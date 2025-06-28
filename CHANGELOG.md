# Changelog

## [2.0.0] - 2025-06-27
### Added
- Tool wrappers for masscan, arp-scan, hydra, gvm-cli, miniupnpc, nikto, sqlmap and pgrok.
- Async tool dispatcher (`routR/tools/runner.py`).
- REST API v2 with endpoints `/api/v2/scan`, `/api/v2/report/<id>`, `/api/v2/health`.
- Tkinter GUI checkboxes and progress bars for new tools.
- GitHub Actions CI with black, pytest and shellcheck.
- Install helper scripts for apt and brew.
- GPU monitoring module with optional nvidia-smi/rocm-smi support.
### Changed
- requirements updated with new dependencies.

## [2.1.0] - 2025-07-01
### Added
- Certificate health checks for HTTPS services.
- D3.js interactive topology export.
- Configuration baseline alerts for risky ports.
- MITRE ATT&CK correlation of findings.
- Unit tests for the certificate, baseline and D3 modules, and the
  interactive topology export.
### Fixed
- Test runner import issue in `tests/test_runner.py`.
