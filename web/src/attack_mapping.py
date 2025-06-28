from typing import Dict, Any, List

ATTACK_PORTS = {
    23: "T1041",  # Remote Service - Telnet
    21: "T1041",  # Remote Service - FTP
    3389: "T1021",  # Remote Services - RDP
}


def correlate_attack(host_data: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    for host, info in host_data.items():
        techniques: List[str] = []
        for port in info.get("open_ports", []):
            tech = ATTACK_PORTS.get(port)
            if tech and tech not in techniques:
                techniques.append(tech)
        if techniques:
            info["attack_techniques"] = techniques
    return host_data
