import io
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import pandas as pd


def render_to_pdf(template_src, context_dict={}):
    """
    Renderiza un template HTML a PDF usando xhtml2pdf.
    """
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

# Función auxiliar que convierte valores nulos o inválidos.
def safe_int(value, default=0):
    """Convierte el valor a entero de forma segura. Si es nulo o inválido, devuelve el valor por defecto."""
    if pd.isnull(value):
        return default
    try:
        return int(float(value))
    except Exception:
        return default

def safe_float(value, default=0.0):
    """Convierte el valor a float de forma segura. Si es nulo o inválido, devuelve el valor por defecto."""
    if pd.isnull(value):
        return default
    try:
        return float(value)
    except Exception:
        return default
