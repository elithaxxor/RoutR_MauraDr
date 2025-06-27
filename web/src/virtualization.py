"""Interact with common hypervisor APIs."""
import logging
from typing import List

logger = logging.getLogger(__name__)


class Hypervisor:
    def list_guests(self) -> List[str]:  # pragma: no cover - placeholder
        raise NotImplementedError


class LibvirtHypervisor(Hypervisor):
    def list_guests(self) -> List[str]:
        try:
            import libvirt  # type: ignore
            conn = libvirt.open(None)
            guests = [dom.name() for dom in conn.listAllDomains()]
            conn.close()
            return guests
        except Exception as exc:
            logger.warning("Libvirt integration failed: %s", exc)
            return []
