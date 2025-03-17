from django.shortcuts import render, redirect
from .models import Agent
from .forms import AgentForm
import pandas as pd
from django.shortcuts import render, redirect
from .models import Agent, WeeklyMetrics

def agents_view(request):
    if request.method == 'POST':
        form = AgentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agents')  # Redirige a la misma página para evitar reenvío de formulario
    else:
        form = AgentForm()
    
    agents = Agent.objects.all()  # Obtiene la lista de agentes existentes
    return render(request, 'dashboard/agents.html', {'form': form, 'agents': agents})


def weekly_metrics_view(request):
    context = {}
    if request.method == 'POST':
        # Obtener datos del formulario
        segment = request.POST.get('segment')
        week_start = request.POST.get('week_start')
        week_end = request.POST.get('week_end')
        file = request.FILES.get('file')

        if not file:
            context['error'] = "No se ha seleccionado ningún archivo."
            return render(request, 'dashboard/weekly_metrics.html', context)

        try:
            # Leer el archivo XLSX utilizando Pandas
            df = pd.read_excel(file)
        except Exception as e:
            context['error'] = f"Error al leer el archivo: {e}"
            return render(request, 'dashboard/weekly_metrics.html', context)

        # Columnas requeridas en el archivo XLSX
        required_columns = [
            'operator_login',
            'Sessions cnt',
            'Actions cnt',
            'Action Close cnt',
            'Productivity, actions/hour',
            'AHT, sec',
            'SL session duration(%)',
            'cnt close / cnt any_actions',
            '% closed sessions',
            'CSAT_cnt',
            'CSAT_avg',
            'Worktime, mins',
            'postcall avg, sec',
            'OCC'
        ]
        
        # Verificar que todas las columnas requeridas estén presentes
        for col in required_columns:
            if col not in df.columns:
                context['error'] = f"Falta la columna requerida: {col}"
                return render(request, 'dashboard/weekly_metrics.html', context)
        
        # Contador para los registros insertados
        count = 0
        
        # Procesar cada fila del DataFrame
        for index, row in df.iterrows():
            operator_login_value = row['operator_login']
            try:
                # Buscar el agente por su operator_login
                agent = Agent.objects.get(operator_login=operator_login_value)
            except Agent.DoesNotExist:
                # Si el agente no existe, se puede optar por omitir el registro o registrar un error.
                # Aquí se omite el registro.
                continue

            # Crear un nuevo registro de WeeklyMetrics
            WeeklyMetrics.objects.create(
                operator_login = agent,
                segment = segment,
                week_start = week_start,
                week_end = week_end,
                sessions_cnt = int(row['Sessions cnt']),
                actions_cnt = int(row['Actions cnt']),
                action_close_cnt = int(row['Action Close cnt']),
                productivity = row['Productivity, actions/hour'],
                AHT_sec = int(row['AHT, sec']),
                SL_session_duration = row['SL session duration(%)'],
                ratio_close_any = row['cnt close / cnt any_actions'],
                closed_sessions_percentage = row['% closed sessions'],
                CSAT_cnt = int(row['CSAT_cnt']),
                CSAT_avg = row['CSAT_avg'],
                worktime_mins = int(row['Worktime, mins']),
                postcall_avg_sec = int(row['postcall avg, sec']),
                OCC = row['OCC']
            )
            count += 1
        
        context['success'] = f"Se importaron {count} registros exitosamente."
        return render(request, 'dashboard/weekly_metrics.html', context)
    
    return render(request, 'dashboard/weekly_metrics.html', context)

def qa_evaluations_view(request):
    if request.method == 'POST':
        # Aquí se procesará la carga del archivo XLSX para QA Evaluations
        pass  # Lógica de procesamiento pendiente
    return render(request, 'dashboard/qa_evaluations.html')
