import io
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import pandas as pd
from datetime import datetime


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

def parse_date(date_input):
    """
    Intenta convertir el valor recibido a un objeto datetime.
    Si el valor ya es un datetime o un objeto Timestamp de pandas, lo convierte a datetime.
    Si es una cadena, intenta varios formatos.
    """
    # Si ya es un objeto datetime, lo devuelve directamente.
    if isinstance(date_input, datetime):
        return date_input

    # Si es un objeto que tiene el método to_pydatetime (como un pandas Timestamp), lo convierte.
    try:
        return date_input.to_pydatetime()
    except AttributeError:
        pass

    # Asegurarse de que es una cadena
    if not isinstance(date_input, str):
        date_input = str(date_input)

    # Lista de formatos que se intentarán.
    formats = [
        "%d-%m-%Y %H:%M",    # Ejemplo: 31-03-2025 19:09
        "%Y-%m-%d %H:%M:%S",  # Ejemplo: 2025-03-31 19:09:00
        "%d/%m/%Y %H:%M",    # Ejemplo: 31/03/2025 19:09
        "%d/%m/%Y %H:%M:%S",  # Ejemplo: 31/03/2025 19:09:00
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_input, fmt)
        except ValueError:
            continue
    raise ValueError(f"No se pudo parsear la fecha '{date_input}' con ninguno de los formatos definidos.")