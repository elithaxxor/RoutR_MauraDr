# Feature Proposal

This document outlines proposed enhancements for the RoutR_MauraDr project.

## 1. Automated Firmware Vulnerability Lookup
- Integrate with an offline CVE database to match detected firmware versions against known issues.
- Provide a command-line option and REST API endpoint for vulnerability reports.

## 2. Default Credential Brute-Force Module
- Add an optional module that attempts default router credentials after detection.
- Include configurable dictionaries and rate limiting to avoid lockouts.

## 3. IPv6 and Extended Network Discovery
- Extend scanning routines to discover IPv6 hosts and services.
- Offer options for scanning custom subnets beyond the default CIDR.

## 4. Improved Web Dashboard
- Add real-time charts for scan progress and historical results.
- Include user authentication and role-based access control.

## 5. Containerization and Deployment
- Provide Dockerfiles for the main script and web interface.
- Document deployment steps for local testing and cloud environments.

## 6. Automated Testing Suite
- Implement basic unit tests for Python modules and shell scripts.
- Add CI configuration to run tests on each commit.

## 7. Modular Plugin Architecture
- Provide a `plugins/` directory where custom modules can be added.
- Plugins are discovered and loaded at runtime to extend scanning features.

## 8. Offline Mode and Data Export
- Enable execution without network connectivity using cached data.
- Offer utilities to export scan results to JSON or CSV for later review.

## 9. Dynamic Configuration Management
- Combine existing INI and YAML files into a single config loader that supports overrides from environment variables.
- Document sample configs for common deployment scenarios.

## 10. REST API Usage Logging
- Record all API requests and responses for auditing purposes.
- Provide optional real-time alerts when administrative actions occur.

## 11. Automated SSH Access with Default Credentials
- After detecting router details, optionally attempt to log in via SSH using known default usernames and passwords.
- Provide logging and configurable credential lists to avoid brute-force issues.

## 12. Expanded CVE Dataset Integration
- Extend the vulnerability lookup to include community-maintained IoT and router exploit databases.
- Allow offline synchronization of CVE data so scans work without Internet access.

## 13. SMB Hash Backup and Alerting
- Leverage the new `web/tooling/smb_hash.py` script to automatically back up Samba password hashes.
- Provide a CLI option and REST endpoint to schedule periodic backups.
- Notify administrators when hash files are modified unexpectedly.

## 14. Scheduled Task Automation
- Integrate a lightweight scheduler to periodically run scans and hash backups.
- Offer CLI commands to list, add, and remove scheduled jobs.

## 15. Notification Integrations
- Send scan summaries and important alerts via email or Slack.
- Allow configuration of multiple notification channels.
