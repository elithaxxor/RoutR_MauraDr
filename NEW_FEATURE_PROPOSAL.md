# Additional Feature Proposal

This document proposes several features that could expand RoutR_MauraDr while complementing the current roadmap. These ideas focus on usability, automation, and integration with other tools.

## 1. PyPI Distribution
- Package RoutR_MauraDr for installation via `pip`.
- Provide compiled wheels for common platforms using GitHub Actions.

## 2. Scheduled Scan Profiles
- Allow predefined scan profiles to be executed on a schedule (daily/weekly/monthly).
- Store schedules in a simple JSON file so they can be edited manually or via the GUI.

## 3. Centralized Reporting Server
- Optionally push completed scan results to a central server.
- Provide a lightweight Flask application that aggregates results and generates charts.

## 4. Auto-Update for Vulnerability Databases
- Implement a `routR update-db` command to download the latest CVE and exploit data.
- Integrate with the proposed scheduler to check for updates automatically.

## 5. Plugin Testing Harness
- Extend the unit test suite with fixtures that validate new plugins.
- Offer a CLI command to run plugin tests before they are enabled in production.

## 6. Cross-Platform Packaging
- Provide scripts for building standalone executables via PyInstaller.
- This allows running RoutR_MauraDr on systems without a Python environment.

