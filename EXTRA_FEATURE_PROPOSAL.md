# Additional Feature Proposal

The following ideas could further enhance RoutR_MauraDr and complement the existing roadmap:

1. **Slack/Discord Notifications**
   - Send scan completion alerts and important events to a team chat.
   - Allow configuration of webhooks through the CLI and web interface.

2. **Containerized Execution**
   - Offer Docker images for isolated tool runs.
   - Provide options to spawn containers automatically when executing scans to avoid local dependencies.

3. **Dynamic Target Discovery**
   - Integrate ARP and mDNS probes to automatically expand target lists before running tools.
   - Present discovered hosts in the dashboard for quick selection.

4. **Custom Report Templates**
   - Allow users to define Jinja2 templates for reports.
   - Support exporting to HTML or PDF with branding and custom sections.

