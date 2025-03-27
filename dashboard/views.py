from django.shortcuts import render, redirect
from .models import Agent
from .forms import AgentForm
import pandas as pd
from django.shortcuts import render, redirect
from .models import Agent, WeeklyMetrics
from django.db.models import Avg


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

import pandas as pd
import re
from datetime import datetime
from django.shortcuts import render
from .models import Agent, QAEvaluation

def qa_evaluations_view(request):
    context = {}
    if request.method == 'POST':
        file = request.FILES.get('file')
        if not file:
            context['error'] = "No se ha seleccionado ningún archivo."
            return render(request, 'dashboard/qa_evaluations.html', context)
        
        try:
            df = pd.read_excel(file)
        except Exception as e:
            context['error'] = f"Error al leer el archivo: {e}"
            return render(request, 'dashboard/qa_evaluations.html', context)
        
        # Columnas requeridas
        required_columns = ["Priority", "Type", "Key", "Summary", "Assignee", "Status", "Updated", "Total final score"]
        for col in required_columns:
            if col not in df.columns:
                context['error'] = f"Falta la columna requerida: {col}"
                return render(request, 'dashboard/qa_evaluations.html', context)
        
        count = 0
        for index, row in df.iterrows():
            priority = row["Priority"]
            eval_type = row["Type"]
            evaluation_key = row["Key"]
            summary = row["Summary"]
            assignee = row["Assignee"]
            status = row["Status"]
            updated_str = row["Updated"]
            total_final_score = row["Total final score"]
            
            # Procesar "Summary": separar el nombre del agente y la fecha de interacción.
            # Ejemplo: "Ximena Torres Quintana 2023-10-27 18:58:20"
            try:
                summary_parts = summary.strip().split(" ")
                if len(summary_parts) < 3:
                    continue  # formato incorrecto, saltar registro
                # La fecha se compone de los dos últimos elementos.
                interaction_date_str = " ".join(summary_parts[-2:])
                agent_name_extracted = " ".join(summary_parts[:-2])
                interaction_date = datetime.strptime(interaction_date_str, "%Y-%m-%d %H:%M:%S")
            except Exception as e:
                # Si falla el procesamiento, se omite este registro
                continue
            
            # Procesar "Assignee": separar el nombre del supervisor y su operator_login.
            # Ejemplo: "Fernando Rodriguez Torrico(fernandorodriguez44)"
            try:
                match = re.match(r"(.+)\((.+)\)", assignee)
                if match:
                    supervisor_name_extracted = match.group(1).strip()
                    supervisor_operator_login = match.group(2).strip()
                else:
                    continue  # Si no se puede extraer, omitir el registro
            except Exception as e:
                continue
            
            # Buscar en la tabla Agent el agente evaluado, basado en el nombre
            try:
                agent = Agent.objects.get(agent_name=agent_name_extracted)
            except Agent.DoesNotExist:
                continue  # Si el agente no existe, omitir el registro
            
            # Buscar el supervisor basado en su operator_login
            try:
                supervisor = Agent.objects.get(operator_login=supervisor_operator_login)
            except Agent.DoesNotExist:
                supervisor = None  # El supervisor puede ser nulo
            
            # Procesar la fecha "Updated". Suponemos el formato "03-11-2023 19:15"
            try:
                updated = datetime.strptime(updated_str, "%d-%m-%Y %H:%M")
            except Exception as e:
                continue  # Si falla el procesamiento, omitir el registro
            
            # Crear el registro de QAEvaluation
            try:
                QAEvaluation.objects.create(
                    evaluation_key=evaluation_key,
                    priority=priority,
                    type=eval_type,
                    agent=agent,
                    interaction_date=interaction_date,
                    supervisor=supervisor,
                    status=status,
                    updated=updated,
                    total_final_score=total_final_score
                )
                count += 1
            except Exception as e:
                continue
        
        context['success'] = f"Se importaron {count} evaluaciones de QA correctamente."
        return render(request, 'dashboard/qa_evaluations.html', context)
    
    return render(request, 'dashboard/qa_evaluations.html')


def weekly_metrics_report_view(request):
    # Obtener filtros desde los parámetros GET
    agent_filter = request.GET.get('agent')
    week_start = request.GET.get('week_start')
    week_end = request.GET.get('week_end')
    segment_filter = request.GET.get('segment')
    
    # Consulta inicial para WeeklyMetrics
    metrics = WeeklyMetrics.objects.all().select_related('operator_login')
    
    if agent_filter:
        metrics = metrics.filter(operator_login__operator_login=agent_filter)
    if segment_filter:
        metrics = metrics.filter(segment=segment_filter)
    if week_start:
        metrics = metrics.filter(week_start__gte=week_start)
    if week_end:
        metrics = metrics.filter(week_end__lte=week_end)
    
    agents = Agent.objects.all()
    
    context = {
        'metrics': metrics,
        'agents': agents,
        'selected_agent': agent_filter,
        'selected_segment': segment_filter,
        'week_start': week_start,
        'week_end': week_end,
    }
    return render(request, 'dashboard/weekly_metrics_report.html', context)


def qa_report_view(request):
    # Obtener filtros desde los parámetros GET
    agent_filter = request.GET.get('agent')
    week_start = request.GET.get('week_start')
    week_end = request.GET.get('week_end')
    team_filter = request.GET.get('team')
    
    # Consulta inicial para QA Evaluations
    qa_evals = QAEvaluation.objects.all().select_related('agent', 'supervisor')
    if agent_filter:
        qa_evals = qa_evals.filter(agent__agent_name=agent_filter)
    if team_filter:
        qa_evals = qa_evals.filter(agent__team=team_filter)
    if week_start:
        qa_evals = qa_evals.filter(interaction_date__gte=week_start)
    if week_end:
        qa_evals = qa_evals.filter(interaction_date__lte=week_end)
    
    # Calcular promedio de total_final_score de las evaluaciones filtradas
    qa_avg = qa_evals.aggregate(avg_score=Avg('total_final_score'))['avg_score']
    
    # Lista de agentes y equipos para el dropdown
    agents = Agent.objects.all()
    teams = Agent.objects.values_list('team', flat=True).distinct()
    
    context = {
        'qa_evals': qa_evals,
        'agents': agents,
        'teams': teams,
        'selected_agent': agent_filter,
        'selected_team': team_filter,
        'week_start': week_start,
        'week_end': week_end,
        'qa_avg': qa_avg,
    }
    return render(request, 'dashboard/qa_report.html', context)

