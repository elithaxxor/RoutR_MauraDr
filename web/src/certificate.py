import socket
import ssl
from datetime import datetime
from typing import Dict, List, Any


def check_certificate(host: str, port: int = 443) -> Dict[str, Any]:
    """Return certificate info for ``host`` or an error message."""
    ctx = ssl.create_default_context()
    try:
        with ctx.wrap_socket(socket.socket(), server_hostname=host) as sock:
            sock.settimeout(5)
            sock.connect((host, port))
            cert = sock.getpeercert()
    except Exception as exc:
        return {"error": str(exc)}

    not_after = cert.get("notAfter")
    expires = None
    days_left = None
    if not_after:
        try:
            expires = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
            days_left = (expires - datetime.utcnow()).days
        except Exception:
            pass

    subject_cn = None
    for tup in cert.get("subject", []):
        for k, v in tup:
            if k == "commonName":
                subject_cn = v
                break
    matches = False
    if subject_cn:
        if subject_cn.startswith("*"):
            matches = host.endswith(subject_cn.lstrip("*"))
        else:
            matches = host == subject_cn

    return {
        "expires": expires.isoformat() if expires else None,
        "days_left": days_left,
        "subject": subject_cn,
        "hostname_match": matches,
    }


def check_https_certificates(host_data: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Update ``host_data`` with certificate info where port 443 is open."""
    for host, info in host_data.items():
        ports: List[int] = info.get("open_ports", [])
        if 443 not in ports:
            continue
        cert_info = check_certificate(host)
        info["certificate"] = cert_info
        if cert_info.get("days_left") is not None and cert_info.get("days_left") <= 30:
            info.setdefault("warnings", []).append("Certificate expiring soon")
        if cert_info.get("hostname_match") is False:
            info.setdefault("warnings", []).append("Certificate hostname mismatch")
    return host_data
