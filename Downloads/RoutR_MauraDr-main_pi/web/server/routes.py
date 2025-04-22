from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from ..tasks.scan_tasks import run_full_scan
from ..tasks.exploit_task import run_exploitation
from ..payload_manager import PayloadManager
from ..logging import setup_logger
from ..utils import validate_cidr

logger = setup_logger('smb_enum.db')
api_ns = Namespace('api', description='SMB-Scor3 operations')

# Add rate limiting
limiter = Limiter(key_func=get_remote_address)

scan_model = api_ns.model('Scan', {
    'network_cidr': fields.String(required=True, description='Network CIDR to scan'),
    'intensity': fields.String(default='low', enum=['low', 'medium', 'high'])
})

payload_manager = PayloadManager()

@api_ns.route('/scan')
class Scan(Resource):
    decorators = [limiter.limit('5/minute')]
    @jwt_required()
    @api_ns.expect(scan_model)
    def post(self):
        data = api_ns.payload
        network_cidr = data.get('network_cidr')
        intensity = data.get('intensity', 'low')
        
        if not validate_cidr(network_cidr):
            logger.warning(f"Invalid CIDR format: {network_cidr}")
            return {'message': 'Invalid CIDR format'}, 400
        if intensity not in ['low', 'medium', 'high']:
            logger.warning(f"Invalid intensity: {intensity}")
            return {'message': 'Invalid intensity value'}, 400
        # Trigger async scan
        try:
            task = run_full_scan.delay(network_cidr, intensity)
            logger.info(f"Started scan task {task.id} for {network_cidr}")
            return {'task_id': task.id}, 202
        except Exception as e:
            logger.error(f"Failed to start scan: {e}")
            return {'message': 'Failed to start scan'}, 500

@api_ns.route('/results/<task_id>')
class Results(Resource):
    decorators = [limiter.limit('10/minute')]
    @jwt_required()
    def get(self, task_id):
        from celery.result import AsyncResult
        try:
            result = AsyncResult(task_id)
            if result.ready():
                if result.successful():
                    return {'status': 'completed', 'results': result.get()}, 200
                logger.error(f"Task {task_id} failed: {result.get(propagate=False)}")
                return {'status': 'failed', 'error': str(result.get(propagate=False))}, 500
            return {'status': 'pending'}, 202
        except Exception as e:
            logger.error(f"Error fetching results for {task_id}: {e}")
            return {'status': 'error', 'error': str(e)}, 500

@api_ns.route('/payloads')
class Payloads(Resource):
    @jwt_required()
    def get(self):
        vendor = api_ns.payload.get('vendor') if api_ns.payload else None
        model = api_ns.payload.get('model') if api_ns.payload else None
        firmware = api_ns.payload.get('firmware') if api_ns.payload else None
        payloads = payload_manager.list_payloads(vendor, model, firmware)
        return [{
            'path': p.path,
            'metadata': p.metadata
        } for p in payloads], 200

@api_ns.route('/exploit')
class Exploit(Resource):
    @jwt_required()
    def post(self):
        data = api_ns.payload
        targets = data.get('targets', [])
        payload_option = data.get('payload_option', 'all')
        params = data.get('params', {})
        try:
            task = run_exploitation.delay(targets, payload_option, params)
            logger.info(f"Started exploit task {task.id} for {len(targets)} targets")
            return {'task_id': task.id}, 202
        except Exception as e:
            logger.error(f"Failed to start exploit: {e}")
            return {'message': 'Failed to start exploit'}, 500

@api_ns.route('/exploit/results/<task_id>')
class ExploitResults(Resource):
    @jwt_required()
    def get(self, task_id):
        from celery.result import AsyncResult
        try:
            result = AsyncResult(task_id)
            if result.ready():
                if result.successful():
                    return {'status': 'completed', 'results': result.get()}, 200
                logger.error(f"Task {task_id} failed: {result.get(propagate=False)}")
                return {'status': 'failed', 'error': str(result.get(propagate=False))}, 500
            return {'status': 'pending'}, 202
        except Exception as e:
            logger.error(f"Error fetching exploit results for {task_id}: {e}")
            return {'status': 'error', 'error': str(e)}, 500
