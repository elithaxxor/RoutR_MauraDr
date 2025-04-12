from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..scanning import discover_smb_hosts, run_nmap_scan
from ..enumeration import enumerate_lan_hosts
from ..scoring import calculate_vulnerability_score, generate_remediation
from ..tasks.scan_tasks import run_full_scan
from ..logging import setup_logger
from ..utils import validate_cidr, validate_time, update_celery_schedule
from ..config import config
import sqlite3
from datetime import datetime

logger = setup_logger(config['database'])
api_ns = Namespace('api', description='SMB-Scor3 operations')

scan_model = api_ns.model('Scan', {
    'network_cidr': fields.String(required=True, description='Network CIDR to scan'),
    'intensity': fields.String(default='low', enum=['low', 'medium', 'high'])
})

schedule_model = api_ns.model('Schedule', {
    'network_cidr': fields.String(required=True, description='Network CIDR to scan'),
    'intensity': fields.String(required=True, enum=['low', 'medium', 'high']),
    'frequency': fields.String(required=True, enum=['immediate', 'daily', 'weekly']),
    'time': fields.String(description='Time in HH:MM format for daily/weekly scans')
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

@api_ns.route('/schedule')
class Schedule(Resource):
    @jwt_required()
    @api_ns.expect(schedule_model)
    def post(self):
        """Create or update a scan schedule."""
        data = api_ns.payload
        network_cidr = data.get('network_cidr')
        intensity = data.get('intensity')
        frequency = data.get('frequency')
        time_str = data.get('time')
        username = get_jwt_identity()

        if not validate_cidr(network_cidr):
            return {'message': 'Invalid CIDR format'}, 400
        if intensity not in ['low', 'medium', 'high']:
            return {'message': 'Invalid intensity'}, 400
        if frequency not in ['immediate', 'daily', 'weekly']:
            return {'message': 'Invalid frequency'}, 400
        if frequency != 'immediate' and (not time_str or not validate_time(time_str)):
            return {'message': 'Invalid or missing time (format: HH:MM)'}, 400

        try:
            with sqlite3.connect(config['database']) as conn:
                c = conn.cursor()
                c.execute('''
                    INSERT OR REPLACE INTO scan_schedules 
                    (network_cidr, intensity, frequency, time, created_at, created_by)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    network_cidr,
                    intensity,
                    frequency,
                    time_str,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    username
                ))
                c.execute('SELECT id FROM scan_schedules WHERE network_cidr = ?', (network_cidr,))
                schedule_id = c.fetchone()[0]
                conn.commit()

            update_celery_schedule(schedule_id, network_cidr, intensity, frequency, time_str)
            logger.info(f"Schedule updated for {network_cidr} by {username}")
            return {'message': f'Schedule set for {network_cidr} ({frequency})', 'schedule_id': schedule_id}, 200
        except Exception as e:
            logger.error(f"Failed to set schedule: {e}")
            return {'message': f'Error setting schedule: {e}'}, 500

    @jwt_required()
    def get(self):
        """Retrieve all scan schedules."""
        try:
            with sqlite3.connect(config['database']) as conn:
                c = conn.cursor()
                c.execute('SELECT id, network_cidr, intensity, frequency, time, created_at, created_by FROM scan_schedules')
                schedules = [
                    {
                        'id': row[0],
                        'network_cidr': row[1],
                        'intensity': row[2],
                        'frequency': row[3],
                        'time': row[4],
                        'created_at': row[5],
                        'created_by': row[6]
                    }
                    for row in c.fetchall()
                ]
            return {'schedules': schedules}, 200
        except Exception as e:
            logger.error(f"Failed to retrieve schedules: {e}")
            return {'message': f'Error retrieving schedules: {e}'}, 500

@api_ns.route('/schedule/<int:schedule_id>')
class ScheduleDetail(Resource):
    @jwt_required()
    def delete(self, schedule_id):
        """Delete a scan schedule."""
        username = get_jwt_identity()
        try:
            with sqlite3.connect(config['database']) as conn:
                c = conn.cursor()
                c.execute('SELECT network_cidr FROM scan_schedules WHERE id = ?', (schedule_id,))
                result = c.fetchone()
                if not result:
                    return {'message': 'Schedule not found'}, 404
                network_cidr = result[0]
                c.execute('DELETE FROM scan_schedules WHERE id = ?', (schedule_id,))
                conn.commit()

            # Remove from Celery Beat
            task_name = f"scan_{schedule_id}"
            if task_name in celery.conf.beat_schedule:
                del celery.conf.beat_schedule[task_name]
                celery.conf.update(beat_schedule=celery.conf.beat_schedule)
                logger.info(f"Removed schedule {task_name} for {network_cidr} by {username}")
            return {'message': f'Schedule {schedule_id} deleted'}, 200
        except Exception as e:
            logger.error(f"Failed to delete schedule {schedule_id}: {e}")
            return {'message': f'Error deleting schedule: {e}'}, 500
