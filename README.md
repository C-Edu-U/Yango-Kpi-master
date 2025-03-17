# Yango KPI Master

Este proyecto tiene como objetivo centralizar y analizar las métricas semanales (Weekly Metrics) y las evaluaciones de calidad (QA Evaluations) de agentes de atención al cliente, proporcionando una interfaz para la carga de archivos XLSX y la generación de reportes y dashboards.

## Características

- **Gestión de Agentes:** Permite registrar y actualizar información de los agentes (operator_login, nombre completo, equipo).
- **Carga de Weekly Metrics:** Proporciona una interfaz para subir archivos XLSX con métricas semanales, indicando el segmento (repartidores, clientes, restaurantes o general) y el rango de fechas.
- **Carga de Evaluaciones de QA:** Permite subir archivos XLSX que contienen evaluaciones de calidad, extrayendo el nombre del agente, fecha de interacción y datos del supervisor.
- **Integridad de Datos:** Garantiza la referencia adecuada entre agentes, supervisores y métricas.
- **Interfaz Web Sencilla:** Incluye un menú lateral para navegar entre la gestión de agentes, carga de Weekly Metrics y carga de QA Evaluations.
- **Administración con Django Admin:** Permite la administración de registros (agentes, métricas, evaluaciones) desde la interfaz de administración de Django.

---

## Requisitos del Sistema

- **Python 3.8+**  
- **pip** (Administrador de paquetes de Python)  
- **Entorno virtual (opcional, pero recomendado)**  
- **Django 3.2+** (o la versión especificada en `requirements.txt`)  
- **openpyxl**, **pandas** (si se requiere el procesamiento avanzado de archivos XLSX)  

---

## Instalación en Windows

1. **Clonar o descargar el repositorio**  
   Abre una terminal (PowerShell o CMD) y ejecuta:  
   ```bash
   git clone https://github.com/tu_usuario/yango-kpi-master.git
   cd yango-kpi-master
   ```

2. **Crear y activar un entorno virtual (opcional pero recomendado)**  
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instalar dependencias**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Realizar migraciones**  
   ```bash
   python manage.py migrate
   ```

5. **Crear un superusuario (opcional)**  
   ```bash
   python manage.py createsuperuser
   ```

6. **Ejecutar el servidor de desarrollo**  
   ```bash
   python manage.py runserver
   ```
   Accede a [http://127.0.0.1:8000/](http://127.0.0.1:8000/) en tu navegador.

---

## Instalación en Linux (Ubuntu / Debian / similar)

1. **Clonar o descargar el repositorio**  
   Abre una terminal y ejecuta:  
   ```bash
   git clone https://github.com/tu_usuario/yango-kpi-master.git
   cd yango-kpi-master
   ```

2. **Crear y activar un entorno virtual (opcional pero recomendado)**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Realizar migraciones**  
   ```bash
   python manage.py migrate
   ```

5. **Crear un superusuario (opcional)**  
   ```bash
   python manage.py createsuperuser
   ```

6. **Ejecutar el servidor de desarrollo**  
   ```bash
   python manage.py runserver
   ```
   Accede a [http://127.0.0.1:8000/](http://127.0.0.1:8000/) en tu navegador.

---

## Estructura Principal del Proyecto

```plaintext
YangoKpiMaster/
├── dashboard/                 
│   ├── __init__.py
│   ├── admin.py               # Registro de modelos para Django Admin
│   ├── apps.py
│   ├── forms.py               # Formularios de Django (p.ej., AgentForm)
│   ├── models.py              # Modelos de la aplicación (Agent, WeeklyMetrics, QAEvaluation)
│   ├── tests.py
│   ├── views.py               # Vistas (p.ej., agents_view, weekly_metrics_view, qa_evaluations_view)
│   ├── templates/
│   │   └── dashboard/
│   │       ├── base.html      # Plantilla base con menú lateral
│   │       ├── agents.html    # Gestión de agentes
│   │       ├── weekly_metrics.html   # Carga de Weekly Metrics
│   │       └── qa_evaluations.html   # Carga de Evaluaciones QA
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

---

## Uso

1. **Acceder al Panel de Administración**  
   - Ir a [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) e iniciar sesión con las credenciales de superusuario para gestionar agentes, métricas y evaluaciones directamente desde Django Admin.

2. **Operaciones**
    - Para ingresar a las páginas de operaciones del proyecto nos dirigimos al link: http://127.0.0.1:8000/agents/ 

3. **Gestionar Agentes**  
   - En la interfaz web principal (menú lateral), ir a "Agentes" para registrar nuevos agentes o revisar la lista de agentes existentes.

4. **Cargar Weekly Metrics**  
   - En "Weekly Metrics", subir el archivo XLSX junto con el segmento y el rango de fechas de la semana. El sistema procesará y almacenará la información asociándola con los agentes correspondientes.

5. **Cargar Evaluaciones QA**  
   - En "QA Evaluations", subir el archivo XLSX con las evaluaciones de calidad. El sistema extraerá el nombre del agente, fecha de interacción y supervisor para vincular la información.

---

## Contribuir

1. Haz un fork del repositorio.
2. Crea una rama con la nueva característica o corrección de errores:
   ```bash
   git checkout -b feature/mi-nueva-feature
   ```
3. Realiza tus cambios y haz commits.
4. Envía tus cambios con un Pull Request al repositorio principal.

---

## Licencia

Este proyecto se distribuye bajo la licencia [MIT](https://opensource.org/licenses/MIT). Puedes usarlo y modificarlo libremente, citando la fuente.

---

**¡Gracias por usar Yango KPI Master!**  
Si tienes preguntas o sugerencias, no dudes en abrir un issue o contactar a los colaboradores del proyecto.