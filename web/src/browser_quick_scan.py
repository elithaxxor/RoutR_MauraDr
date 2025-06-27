"""Endpoint to trigger quick scans from the browser."""
from flask import Blueprint, jsonify, request
from .quick_scan import quick_port_scan

bp = Blueprint('browser_quick_scan', __name__)


@bp.route('/quick-scan')
def quick_scan_endpoint():  # pragma: no cover - simple wrapper
    target = request.args.get('target', '192.168.1.1')
    result = quick_port_scan(target)
    return jsonify(result)
