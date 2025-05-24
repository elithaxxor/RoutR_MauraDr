"""Integration helpers for external vulnerability scanners."""
import subprocess
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def run_openvas(target: str) -> Optional[str]:
    """Run an OpenVAS scan on the target and return the report path."""
    try:
        # Placeholder command - requires openvas installation
        cmd = ["gvm-script", "--gmp-username", "admin", "--gmp-password", "password", "ssh", target]
        subprocess.run(cmd, check=True)
        report_path = f"openvas_report_{target}.xml"
        logger.info("OpenVAS scan complete")
        return report_path
    except Exception as exc:
        logger.error(f"OpenVAS scan failed: {exc}")
        return None


def run_nessus(target: str) -> Optional[str]:
    """Run a Nessus scan on the target and return the report path."""
    try:
        cmd = ["nessus", "-q", target]
        subprocess.run(cmd, check=True)
        report_path = f"nessus_report_{target}.xml"
        logger.info("Nessus scan complete")
        return report_path
    except Exception as exc:
        logger.error(f"Nessus scan failed: {exc}")
        return None
