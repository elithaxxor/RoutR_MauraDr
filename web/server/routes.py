from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from ..scanning import discover_smb_hosts, run_nmap_scan
from ..enumeration import enumerate_lan_hosts
from ..scoring import calculate_vulnerability_score, generate_remediation
from ..tasks.scan_tasks import run_full_scan
from ..logging import setup_logger
from ..utils import validate_cidr

logger = setup_logger('smb_enum.db')
api_ns = Namespace('api', description='SMB-Scor3 operations')

scan_model = api_ns.model('Scan', {
    'network_cidr': fields.String(required=True, description='Network CIDR to scan'),
    'intensity': fields.String(default='low', enum=['low', 'medium', 'high'])
})

@api_ns.route('/scan')
class Scan(Resource):
    @jwt_required()
    @api_ns.expect(scan_model)
    def post(self):
        data = api_ns.payload
        network_cidr = data.get('network_cidr')
        intensity = data.get('intensity', 'low')
        
        if not validate_cidr(network_cidr):
            return {'message': 'Invalid CIDR format'}, 400
        
        # Trigger async scan
        task = run_full_scan.delay(network_cidr, intensity)
        logger.info(f"Started scan task {task.id} for {network_cidr}")
        return {'task_id': task.id}, 202

@api_ns.route('/results/<task_id>')
class Results(Resource):
    @jwt_required()
    def get(self, task_id):
        from celery.result import AsyncResult
        result = AsyncResult(task_id)
        if result.ready():
            if result.successful():
                return {'status': 'completed', 'results': result.get()}, 200
            return {'status': 'failed', 'error': str(result.get(propagate=False))}, 500
        return {'status': 'pending'}, 202
