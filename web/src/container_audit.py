"""Utilities for basic container security auditing."""
import subprocess
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


def scan_image(image: str) -> Optional[Dict[str, str]]:
    """Run 'trivy' against a container image if available."""
    if not image:
        return None
    try:
        result = subprocess.check_output(["trivy", "-q", "--format", "json", image], text=True)
        logger.info("Trivy scan completed for %s", image)
        return {"image": image, "report": result}
    except Exception as exc:
        logger.error("Container scan failed: %s", exc)
        return None


def audit_dockerfile(path: str) -> Optional[str]:
    """Run 'docker scan' on a Dockerfile if available."""
    try:
        subprocess.check_call(["docker", "scan", path])
        logger.info("Dockerfile audit finished")
        return "Scan completed"
    except Exception as exc:
        logger.error("Dockerfile audit failed: %s", exc)
        return None
