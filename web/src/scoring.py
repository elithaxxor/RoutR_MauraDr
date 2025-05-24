from .config import config
from .logging import setup_logger
import functools

logger = setup_logger(config['database'])

@functools.lru_cache(maxsize=100)
def lookup_cve(cve_id):
    """
    Placeholder for CVE lookup with caching.
    
    Args:
        cve_id (str): CVE identifier
    
    Returns:
        dict: Mocked CVE data (severity, CVSS score)
    """
    # In a real implementation, this would query an API like NVD
    logger.debug(f"Looking up CVE: {cve_id}")
    return {"severity": "HIGH", "cvss": 7.5}

def calculate_vulnerability_score(host_data):
    """
    Calculate a vulnerability score for the host based on collected data.
    
    Args:
        host_data (dict): Host data including vulnerabilities, ports, etc.
    
    Returns:
        tuple: (score, category)
    """
    weights = config['scoring_weights']
    high_risk_ports = config['high_risk_ports']
    
    score = 100  # Start with a perfect score
    
    # Vulnerability penalties
    vuln_count = len(host_data["vulnerabilities"])
    score -= vuln_count * weights["vuln_penalty"]
    
    # Open port penalties
    for port in host_data["open_ports"]:
        score -= weights["port_penalty"]
        if port in high_risk_ports:
            score -= weights["high_risk_penalty"]
    
    # Plaintext credentials penalty
    score -= host_data["plaintext_creds"] * weights["creds_penalty"]
    
    # Missing patches penalty
    score -= host_data["missing_patches"] * weights["patch_penalty"]
    
    # Ensure score stays within bounds
    final_score = max(score, 0)
    
    # Determine risk category
    category = (
        "Low" if final_score >= 80 else
        "Medium" if final_score >= 50 else
        "High" if final_score >= 20 else
        "Critical"
    )
    
    return final_score, category

def generate_remediation(host_data):
    """
    Generate remediation recommendations based on host data.
    
    Args:
        host_data (dict): Host data including vulnerabilities
    
    Returns:
        list: List of remediation steps
    """
    remediation = []
    if "SMBv1 Enabled" in host_data["vulnerabilities"]:
        remediation.append("Disable SMBv1 on the host to prevent exploitation (e.g., EternalBlue).")
    if host_data["plaintext_creds"] > 0:
        remediation.append("Enforce strong password policies and disable accounts with no passwords.")
    if host_data["missing_patches"] > 0:
        remediation.append("Apply available security patches to the system.")
    return remediation
