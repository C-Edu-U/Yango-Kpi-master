# KPI Master

Este proyecto tiene como objetivo centralizar y analizar las métricas semanales (Weekly Metrics) y las evaluaciones de calidad (QA Evaluations) de agentes de atención al cliente, proporcionando una interfaz para la carga de archivos XLSX y la generación de reportes y dashboards.

## Características

- **Gestión de Agentes:** Permite registrar y actualizar información de los agentes (operator_login, nombre completo, equipo).
- **Carga de Weekly Metrics:** Proporciona una interfaz para subir archivos XLSX con métricas semanales, indicando el segmento (repartidores, clientes, restaurantes o general) y el rango de fechas.
- **Carga de Evaluaciones de QA:** Permite subir archivos XLSX que contienen evaluaciones de calidad, extrayendo el nombre del agente, fecha de interacción y datos del supervisor.
- **Integridad de Datos:** Garantiza la referencia adecuada entre agentes, supervisores y métricas.
- **Interfaz Web Sencilla:** Incluye un menú lateral para navegar entre la gestión de agentes, carga de Weekly Metrics, carga de QA Evaluations, reportes y dashboard.
- **Administración con Django Admin:** Permite la administración de registros (agentes, métricas, evaluaciones) desde la interfaz de administración de Django.
- **Descarga de Reportes y Dashboard en PDF:** Permite generar PDFs de los reportes y del dashboard con gráficos e información filtrada.
- **Pruebas de Integración:** Se utilizan pruebas con pytest-django para validar la funcionalidad del sistema.

## Requisitos del Sistema

- Python 3.8+
- pip (Administrador de paquetes de Python)
- Entorno virtual (opcional, pero recomendado)
- Django 3.2+ (o la versión especificada en `requirements.txt`)
- openpyxl, pandas (para el procesamiento avanzado de archivos XLSX)
- mysqlclient (en caso de conectarse a una base de datos MariaDB en producción)

## Repositorio

El código fuente se encuentra alojado en GitHub. Para clonar el proyecto, utiliza la siguiente URL y asegúrate de extraer la rama **main**:

[https://github.com/C-Edu-U/Yango-Kpi-master/tree/main](https://github.com/C-Edu-U/Yango-Kpi-master/tree/main)

Para clonar el repositorio en la rama main, ejecuta:

```bash
git clone -b main https://github.com/C-Edu-U/Yango-Kpi-master.git
```

Si ya has clonado el repositorio y deseas cambiar a la rama main, puedes hacerlo con:

```bash
cd Yango-Kpi-master
git checkout main
Nota: Asegúrate de trabajar en la rama main para disponer de todas las actualizaciones y el contenido del proyecto.
```

## Instalación en Windows

1. Clona el repositorio:
   ```bash
   git clone -b main https://github.com/C-Edu-U/Yango-Kpi-master.git
   cd Yango-Kpi-master
   ```

2. Crea y activa un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Realiza las migraciones:
   ```bash
   python manage.py migrate
   ```

5. Crea un superusuario (opcional):
   ```bash
   python manage.py createsuperuser
   ```

6. Ejecuta el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```
   Accede a [http://127.0.0.1:8000/](http://127.0.0.1:8000/) en tu navegador.

## Instalación en Linux (Ubuntu / Debian / Similar)

1. Clona el repositorio:
   ```bash
   git clone -b main https://github.com/C-Edu-U/Yango-Kpi-master.git
   cd Yango-Kpi-master
   ```

2. Crea y activa un entorno virtual (opcional pero recomendado):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Realiza las migraciones:
   ```bash
   python manage.py migrate
   ```

5. Crea un superusuario (necesario para loggearse en la aplicación y en el backend de django):
   ```bash
   python manage.py createsuperuser
   ```

6. Ejecuta el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```
   Accede a [http://127.0.0.1:8000/](http://127.0.0.1:8000/) en tu navegador.

7. Dirigirse al botón de login e ingresar con el usuario y contraseña.

## Estructura Principal del Proyecto

```
YangoKpiMaster/
├── dashboard/                 
│   ├── __init__.py
│   ├── admin.py               # Registro de modelos para Django Admin
│   ├── apps.py
│   ├── forms.py               # Formularios de Django (e.g., AgentForm, QAEvaluationCommentsForm)
│   ├── models.py              # Modelos de la aplicación (Agent, WeeklyMetrics, QAEvaluation)
│   ├── tests.py
│   ├── views.py               # Vistas (e.g., agents_view, weekly_metrics_view, qa_evaluations_view, dashboard_view)
│   ├── utils.py               # Funciones auxiliares (e.g., safe_int, safe_float, render_to_pdf)
│   ├── templates/
│   │   └── dashboard/
│   │       ├── base.html      # Plantilla base con menú lateral y usuario logueado
│   │       ├── agents.html    # Gestión de agentes (incluye edición y eliminación)
│   │       ├── weekly_metrics.html   # Carga de Weekly Metrics
│   │       ├── qa_evaluations.html   # Carga de Evaluaciones QA
│   │       ├── weekly_metrics_report.html  # Reporte de Weekly Metrics
│   │       ├── qa_report.html             # Reporte de Evaluaciones QA
│   │       ├── dashboard.html             # Dashboard con gráficos
│   │       ├── weekly_metrics_report_pdf.html  # Template PDF para Weekly Metrics Report
│   │       ├── qa_report_pdf.html         # Template PDF para QA Report
│   │       └── dashboard_pdf.html         # Template PDF para Dashboard
│   └── urls.py                # Enrutamiento de la aplicación
├── YangoKpiMaster/            
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py            # Configuración global del proyecto
│   ├── urls.py                # Enrutamiento principal del proyecto
│   └── wsgi.py
├── db.sqlite3                 # Base de datos de desarrollo (SQLite)
├── manage.py
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Documento de información del proyecto
```

## Uso

### Acceso al Panel de Administración

- Ir a [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) e iniciar sesión con las credenciales de superusuario para gestionar agentes, métricas y evaluaciones desde Django Admin.

### Operaciones

- **Gestión de Agentes:**  
  Accede a [http://127.0.0.1:8000/agents/](http://127.0.0.1:8000/agents/) para registrar nuevos agentes, editar o eliminar los existentes.

- **Carga de Weekly Metrics:**  
  En [http://127.0.0.1:8000/weekly-metrics/](http://127.0.0.1:8000/weekly-metrics/), sube el archivo XLSX junto con el segmento y el rango de fechas.

- **Carga de Evaluaciones QA:**  
  En [http://127.0.0.1:8000/qa-evaluations/](http://127.0.0.1:8000/qa-evaluations/), sube el archivo XLSX con las evaluaciones de calidad.  
  Además, en la lista de evaluaciones (o en el reporte de QA) se ofrece la opción de agregar o editar comentarios y el link del ticket.

- **Reportes y Dashboard:**  
  - Reporte de Weekly Metrics: [http://127.0.0.1:8000/report/weekly/](http://127.0.0.1:8000/report/weekly/)
  - Reporte de QA: [http://127.0.0.1:8000/report/qa/](http://127.0.0.1:8000/report/qa/)
  - Dashboard: [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/)
  En estas páginas se pueden aplicar filtros y descargar los informes en PDF.

## Contribuir

1. Haz un fork del repositorio.
2. Crea una rama con la nueva característica o corrección de errores:
   ```bash
   git checkout -b feature/mi-nueva-feature
   ```
3. Realiza tus cambios y haz commits.
4. Envía tus cambios con un Pull Request al repositorio principal.

## Licencia

Este proyecto se distribuye bajo la licencia [MIT](https://opensource.org/licenses/MIT). Puedes usarlo y modificarlo libremente, citando la fuente.

---
**¡Gracias por usar Yango KPI Master!**  
Si tienes preguntas o sugerencias, no dudes en abrir un issue o contactar a los colaboradores del proyecto.
