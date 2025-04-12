from celery import Celery
from ..scanning import discover_smb_hosts
from ..enumeration import enumerate_lan_hosts
from ..scoring import calculate_vulnerability_score, generate_remediation

celery = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@celery.task
def run_full_scan(network_cidr, intensity):
    hosts = discover_smb_hosts(network_cidr)
    host_data = enumerate_lan_hosts(hosts, intensity)
    results = {}
    for host, data in host_data.items():
        score, category = calculate_vulnerability_score(data)
        remediation = generate_remediation(data)
        results[host] = {'score': score, 'category': category, 'remediation': remediation}
    return results
