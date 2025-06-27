"""Endpoint to trigger quick scans from the browser."""
try:
    from flask import Blueprint, jsonify, request
except Exception:  # pragma: no cover - Flask optional for tests
    class _Dummy:
        def route(self, *_args, **_kwargs):
            def wrapper(func):
                return func

            return wrapper

    def Blueprint(*_args, **_kwargs):  # type: ignore
        return _Dummy()

    def jsonify(data):
        return data

    class request:  # type: ignore
        args = {}
from .quick_scan import quick_port_scan

bp = Blueprint('browser_quick_scan', __name__)


@bp.route('/quick-scan')
def quick_scan_endpoint():  # pragma: no cover - simple wrapper
    target = request.args.get('target', '192.168.1.1')
    result = quick_port_scan(target)
    return jsonify(result)
