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

## 7. Modular Plugin Framework
- Allow new scanning modules to be dropped into a `plugins/` directory and loaded dynamically.
- Provide hooks for enumeration, scoring, and reporting extensions.

## 8. Offline Results Export
- Include a command to export scan results to JSON or CSV for analysis on systems without network access.

## 9. Dynamic Configuration Management
- Implement a mechanism to reload configuration files at runtime without restarting the service.
- Support overrides from environment variables and document sample configs for common scenarios.

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
- Leverage the `web/tooling/smb_hash.py` script to automatically back up Samba password hashes.
- Provide a CLI option and REST endpoint to schedule periodic backups.
- Notify administrators when hash files are modified unexpectedly.

## 14. Scheduled Task Automation
- Integrate a lightweight scheduler to periodically run scans and hash backups.
- Offer CLI commands to list, add, and remove scheduled jobs.

## 15. Notification Integrations
- Send scan summaries and important alerts via email or Slack.
- Allow configuration of multiple notification channels.

## 16. Real-Time Alerting Dashboard
- Implement WebSocket support in the web interface to push scan results and alerts instantly to connected clients.
- Allow users to customize alert thresholds and notification methods.

## 17. Anomaly Detection Engine
- Collect baseline network metrics and use simple heuristics to flag unusual activity.
- Provide summary reports highlighting new devices or unexpected open ports.

## 18. Firmware Bug Search Automation
- Automatically cross-reference router firmware versions with known vulnerability lists.
- Highlight issues directly in the CLI output and dashboard.

## 19. Visual Network Mapping
- Generate interactive network topology maps from scan results.
- Offer export options to PNG or HTML for easy sharing.

## 18. Automated Firmware Bug Search
- Combine firmware detection with offline CVE data to flag known exploits automatically.
- Attempt SSH login with default credentials when a vulnerable firmware version is found.

## 19. Visual Network Mapping
- Generate a graphical map of discovered hosts and connections for easier analysis.
- Offer export options to PNG or SVG for integration into reports.

## 20. Community Plugin Repository
- Allow installation of third-party scanning modules from a curated list.
- Provide version checks and signatures to maintain security when fetching plugins.

## 20. Community Plugin Repository
- Package plugins with metadata so they can be shared easily.
- Provide a helper script to submit plugins to a community repository.
