"""Helpers for generating HTML and PDF reports from scan data."""
import json
import logging
from typing import Dict
try:
    from jinja2 import Template
except Exception:  # pragma: no cover - jinja2 may be absent in tests
    class Template:  # type: ignore
        """Fallback Template if jinja2 is unavailable."""

        def __init__(self, text: str) -> None:
            self.text = text

        def render(self, **kwargs: Dict[str, str]) -> str:
            rendered = self.text
            for key, value in kwargs.items():
                rendered = rendered.replace(f"{{{{ {key} }}}}", str(value))
                rendered = rendered.replace(f"{{{{{key}}}}}", str(value))
            return rendered

try:
    import pdfkit
except Exception:  # pragma: no cover - optional dependency
    pdfkit = None

logger = logging.getLogger(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Scan Report</title></head>
<body>
<h1>Scan Summary</h1>
<pre>{{ data }}</pre>
</body>
</html>
"""


def export_html(data: Dict, output_file: str = "report.html") -> str:
    """Write scan data to an HTML file using a simple template."""
    template = Template(HTML_TEMPLATE)
    rendered = template.render(data=json.dumps(data, indent=2))
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rendered)
    logger.info("HTML report written to %s", output_file)
    return output_file


def export_pdf(data: Dict, output_file: str = "report.pdf") -> str:
    """Export scan data to a PDF. Requires pdfkit."""
    html_file = export_html(data, output_file + ".html")
    if pdfkit:
        try:
            pdfkit.from_file(html_file, output_file)
            logger.info("PDF report written to %s", output_file)
            return output_file
        except Exception as exc:
            logger.error("PDF generation failed: %s", exc)
    return html_file
