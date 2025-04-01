from django.shortcuts import render, redirect, get_object_or_404
from .forms import AgentForm, QAEvaluationCommentsForm
import pandas as pd
from django.shortcuts import render, redirect
from django.db.models import Avg
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import Agent, WeeklyMetrics, QAEvaluation
import pandas as pd
import re
from datetime import datetime
from django.contrib.auth import logout
from .utils import render_to_pdf, safe_int, safe_float, parse_date



def landing_view(request):
    """Vista para la landing page del sitio."""
    return render(request, 'dashboard/landing.html')

class CustomLoginView(LoginView):
    template_name = 'dashboard/login.html'

    def get_success_url(self):
        """Redirige al usuario autenticado si es staff, de lo contrario a la landing page."""
        if self.request.user.is_staff:
            return '/agents/'
        return '/'

@login_required
def agents_view(request):
    # Lógica para agregar un agente individual
    if request.method == 'POST' and 'operator_login' in request.POST:
        form = AgentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agents')
    # Lógica para importar agentes desde XLSX
    elif request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES.get('file')
        try:
            df = pd.read_excel(file)
        except Exception as e:
            context = {'error': f"Error al leer el archivo: {e}"}
            # Se carga la lista actual de agentes para la vista
            context['agents'] = Agent.objects.all()
            context['form'] = AgentForm()
            return render(request, 'dashboard/agents.html', context)
        
        # Columnas requeridas en el archivo XLSX
        required_columns = ['operator_login', 'agent_name', 'team']
        for col in required_columns:
            if col not in df.columns:
                context = {'error': f"Falta la columna requerida: {col}"}
                context['agents'] = Agent.objects.all()
                context['form'] = AgentForm()
                return render(request, 'dashboard/agents.html', context)
        
        count = 0
        for index, row in df.iterrows():
            operator_login_value = str(row['operator_login']).strip()
            agent_name_value = str(row['agent_name']).strip()
            team_value = str(row['team']).strip()
            # Si el agente ya existe, actualiza; si no, crea uno nuevo.
            agent, created = Agent.objects.update_or_create(
                operator_login=operator_login_value,
                defaults={'agent_name': agent_name_value, 'team': team_value}
            )
            count += 1
        context = {'success': f"Se importaron {count} agentes correctamente."}
        # Continuamos mostrando la lista actualizada
        context['agents'] = Agent.objects.all()
        context['form'] = AgentForm()
        return render(request, 'dashboard/agents.html', context)
    
    else:
        form = AgentForm()
    
    agents = Agent.objects.all()
    context = {'form': form, 'agents': agents}
    return render(request, 'dashboard/agents.html', context)

@login_required
def weekly_metrics_view(request):
    context = {}
    if request.method == 'POST':
        segment = request.POST.get('segment')
        week_start = request.POST.get('week_start')
        week_end = request.POST.get('week_end')
        file = request.FILES.get('file')

        if not file:
            context['error'] = "No se ha seleccionado ningún archivo."
            return render(request, 'dashboard/weekly_metrics.html', context)

        try:
            df = pd.read_excel(file)
        except Exception as e:
            context['error'] = f"Error al leer el archivo: {e}"
            return render(request, 'dashboard/weekly_metrics.html', context)

        required_columns = [
            'operator_login',
            'Sessions cnt',
            'Actions cnt',
            'Action Close cnt',
            'Productivity, actions/hour',
            'AHT, sec',
            'SL  session duration',  # Actualizado al nombre correcto
            'cnt close / cnt any_actions',
            '% closed sessions',
            'CSAT_cnt',
            'CSAT_avg',
            'Worktime, mins',
            'postcall avg, sec',
            'OCC'
        ]
        
        for col in required_columns:
            if col not in df.columns:
                context['error'] = f"Falta la columna requerida: {col}"
                return render(request, 'dashboard/weekly_metrics.html', context)
        
        count = 0
        
        for index, row in df.iterrows():
            operator_login_value = row['operator_login']
            try:
                agent = Agent.objects.get(operator_login=operator_login_value)
            except Agent.DoesNotExist:
                # Si el agente no existe, se omite el registro.
                continue

            try:
                WeeklyMetrics.objects.create(
                    operator_login = agent,
                    segment = segment,
                    week_start = week_start,
                    week_end = week_end,
                    sessions_cnt = safe_int(row['Sessions cnt']),
                    actions_cnt = safe_int(row['Actions cnt']),
                    action_close_cnt = safe_int(row['Action Close cnt']),
                    productivity = safe_float(row['Productivity, actions/hour']),
                    AHT_sec = safe_int(row['AHT, sec']),
                    SL_session_duration = safe_float(row['SL  session duration']),
                    ratio_close_any = safe_float(row['cnt close / cnt any_actions']),
                    closed_sessions_percentage = safe_float(row['% closed sessions']),
                    CSAT_cnt = safe_int(row['CSAT_cnt']),
                    CSAT_avg = safe_float(row['CSAT_avg']),
                    worktime_mins = safe_int(row['Worktime, mins']),
                    postcall_avg_sec = safe_int(row['postcall avg, sec']),
                    OCC = safe_float(row['OCC'])
                )
                count += 1
            except Exception as e:
                # Puedes registrar el error o ignorar la fila
                continue
        
        context['success'] = f"Se importaron {count} registros exitosamente."
        return render(request, 'dashboard/weekly_metrics.html', context)
    
    return render(request, 'dashboard/weekly_metrics.html', context)

@login_required
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
            
            # Procesar la fecha "Updated" usando la función parse_date
            try:
                updated = parse_date(updated_str)
            except ValueError as e:
                # Si falla el parseo, omitir el registro
                continue
            
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

@login_required
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

@login_required
def qa_report_view(request):
    agent_filter = request.GET.get('agent') or ""
    week_start = request.GET.get('week_start') or ""
    week_end = request.GET.get('week_end') or ""
    team_filter = request.GET.get('team') or ""
    
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

    # Calcular el promedio y el total de evaluaciones
    qa_avg = qa_evals.aggregate(avg_score=Avg('total_final_score'))['avg_score']
    qa_count = qa_evals.count()
    
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
        'qa_count': qa_count,
    }
    return render(request, 'dashboard/qa_report.html', context)


def custom_logout_view(request):
    # Realiza el logout del usuario
    logout(request)
    # Redirige al usuario a la página de login (o landing page)
    return redirect('landing')

@login_required
def edit_agent_view(request, operator_login):
    agent = get_object_or_404(Agent, operator_login=operator_login)
    if request.method == 'POST':
        form = AgentForm(request.POST, instance=agent)
        if form.is_valid():
            form.save()
            return redirect('agents')
    else:
        form = AgentForm(instance=agent)
    return render(request, 'dashboard/edit_agent.html', {'form': form, 'agent': agent})

@login_required
def delete_agent_view(request, operator_login):
    agent = get_object_or_404(Agent, operator_login=operator_login)
    if request.method == 'POST':
        agent.delete()
        return redirect('agents')
    return render(request, 'dashboard/delete_agent.html', {'agent': agent})

@login_required
def dashboard_view(request):
    agent_filter = request.GET.get('agent')
    team_filter = request.GET.get('team')
    week_start = request.GET.get('week_start')
    week_end = request.GET.get('week_end')
    
    # Filtrar Weekly Metrics
    metrics = WeeklyMetrics.objects.all().select_related('operator_login')
    if week_start:
        metrics = metrics.filter(week_start__gte=week_start)
    if week_end:
        metrics = metrics.filter(week_end__lte=week_end)
    if agent_filter:
        metrics = metrics.filter(operator_login__agent_name=agent_filter)
    if team_filter:
        metrics = metrics.filter(operator_login__team=team_filter)
    
    # Calcular promedios para Weekly Metrics
    aht_data = metrics.filter(segment='general').aggregate(avg_aht=Avg('AHT_sec'))['avg_aht']
    sl_data = metrics.filter(segment='general').aggregate(avg_sl=Avg('SL_session_duration'))['avg_sl']
    csat_clientes = metrics.filter(segment='clientes').aggregate(avg_csat=Avg('CSAT_avg'))['avg_csat']
    csat_repartidores = metrics.filter(segment='repartidores').aggregate(avg_csat=Avg('CSAT_avg'))['avg_csat']
    csat_restaurantes = metrics.filter(segment='restaurantes').aggregate(avg_csat=Avg('CSAT_avg'))['avg_csat']
    csat_general = metrics.filter(segment='general').aggregate(avg_csat=Avg('CSAT_avg'))['avg_csat']
    
    # Filtrar QA Evaluations
    qa_evals = QAEvaluation.objects.all().select_related('agent', 'supervisor')
    if week_start:
        qa_evals = qa_evals.filter(interaction_date__gte=week_start)
    if week_end:
        qa_evals = qa_evals.filter(interaction_date__lte=week_end)
    if agent_filter:
        qa_evals = qa_evals.filter(agent__agent_name=agent_filter)
    if team_filter:
        qa_evals = qa_evals.filter(agent__team=team_filter)
    qa_avg = qa_evals.aggregate(avg_qa=Avg('total_final_score'))['avg_qa']
    
    # Obtener listas de agentes y equipos para el filtro
    agents = Agent.objects.values_list('agent_name', flat=True).distinct()
    teams = Agent.objects.values_list('team', flat=True).distinct()
    
    context = {
        'aht_data': aht_data,
        'sl_data': sl_data,
        'csat_clientes': csat_clientes,
        'csat_repartidores': csat_repartidores,
        'csat_restaurantes': csat_restaurantes,
        'csat_general': csat_general,
        'qa_avg': qa_avg,
        'agents': agents,
        'teams': teams,
        'selected_agent': agent_filter,
        'selected_team': team_filter,
        'week_start': week_start,
        'week_end': week_end,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def download_weekly_metrics_pdf(request):
    # Obtener parámetros de la URL
    agent_filter = request.GET.get('agent') or ""
    week_start = request.GET.get('week_start') or ""
    week_end = request.GET.get('week_end') or ""
    segment_filter = request.GET.get('segment') or ""

    # Si llegan como "None", reemplazarlos por cadena vacía
    if week_start == "None":
        week_start = ""
    if week_end == "None":
        week_end = ""

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
    pdf = render_to_pdf('dashboard/weekly_metrics_report_pdf.html', context)
    return pdf

@login_required
def download_qa_pdf(request):
    agent_filter = request.GET.get('agent')
    week_start = request.GET.get('week_start')
    week_end = request.GET.get('week_end')
    team_filter = request.GET.get('team')
    
    qa_evals = QAEvaluation.objects.all().select_related('agent', 'supervisor')
    if agent_filter:
        qa_evals = qa_evals.filter(agent__agent_name=agent_filter)
    if team_filter:
        qa_evals = qa_evals.filter(agent__team=team_filter)
    if week_start:
        qa_evals = qa_evals.filter(interaction_date__gte=week_start)
    if week_end:
        qa_evals = qa_evals.filter(interaction_date__lte=week_end)
    
    qa_avg = qa_evals.aggregate(avg_score=Avg('total_final_score'))['avg_score']
    qa_count = qa_evals.count()
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
        'qa_count': qa_count,
    }
    pdf = render_to_pdf('dashboard/qa_report_pdf.html', context)
    return pdf

@login_required
def download_dashboard_pdf(request):
    agent_filter = request.GET.get('agent')
    team_filter = request.GET.get('team')
    week_start = request.GET.get('week_start')
    week_end = request.GET.get('week_end')
    
    metrics = WeeklyMetrics.objects.all().select_related('operator_login')
    if week_start:
        metrics = metrics.filter(week_start__gte=week_start)
    if week_end:
        metrics = metrics.filter(week_end__lte=week_end)
    if agent_filter:
        metrics = metrics.filter(operator_login__agent_name=agent_filter)
    if team_filter:
        metrics = metrics.filter(operator_login__team=team_filter)
    
    # Calcular promedios para gráficos
    aht_data = metrics.filter(segment='general').aggregate(avg_aht=Avg('AHT_sec'))['avg_aht']
    sl_data = metrics.filter(segment='general').aggregate(avg_sl=Avg('SL_session_duration'))['avg_sl']
    csat_clientes = metrics.filter(segment='clientes').aggregate(avg_csat=Avg('CSAT_avg'))['avg_csat']
    csat_repartidores = metrics.filter(segment='repartidores').aggregate(avg_csat=Avg('CSAT_avg'))['avg_csat']
    csat_restaurantes = metrics.filter(segment='restaurantes').aggregate(avg_csat=Avg('CSAT_avg'))['avg_csat']
    csat_general = metrics.filter(segment='general').aggregate(avg_csat=Avg('CSAT_avg'))['avg_csat']
    
    qa_evals = QAEvaluation.objects.all().select_related('agent', 'supervisor')
    if week_start:
        qa_evals = qa_evals.filter(interaction_date__gte=week_start)
    if week_end:
        qa_evals = qa_evals.filter(interaction_date__lte=week_end)
    if agent_filter:
        qa_evals = qa_evals.filter(agent__agent_name=agent_filter)
    if team_filter:
        qa_evals = qa_evals.filter(agent__team=team_filter)
    qa_avg = qa_evals.aggregate(avg_qa=Avg('total_final_score'))['avg_qa']
    
    agents = Agent.objects.values_list('agent_name', flat=True).distinct()
    teams = Agent.objects.values_list('team', flat=True).distinct()
    
    context = {
        'aht_data': aht_data,
        'sl_data': sl_data,
        'csat_clientes': csat_clientes,
        'csat_repartidores': csat_repartidores,
        'csat_restaurantes': csat_restaurantes,
        'csat_general': csat_general,
        'qa_avg': qa_avg,
        'agents': agents,
        'teams': teams,
        'selected_agent': agent_filter,
        'selected_team': team_filter,
        'week_start': week_start,
        'week_end': week_end,
    }
    pdf = render_to_pdf('dashboard/dashboard_pdf.html', context)
    return pdf

@login_required
def add_comments_view(request, evaluation_key):
    evaluation = get_object_or_404(QAEvaluation, evaluation_key=evaluation_key)
    if request.method == 'POST':
        form = QAEvaluationCommentsForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            return redirect('qa_evaluations')  # Redirige a la lista de evaluaciones QA
    else:
        form = QAEvaluationCommentsForm(instance=evaluation)
    return render(request, 'dashboard/add_comments.html', {'form': form, 'evaluation': evaluation})

@login_required
def qa_ranking_view(request):
    # Obtener filtros desde los parámetros GET
    agent_filter = request.GET.get('agent') or ""
    team_filter = request.GET.get('team') or ""
    week_start = request.GET.get('week_start') or ""
    week_end = request.GET.get('week_end') or ""
    
    # Filtrar las evaluaciones QA según los parámetros recibidos
    qa_evals = QAEvaluation.objects.all().select_related('agent')
    if agent_filter:
        qa_evals = qa_evals.filter(agent__agent_name=agent_filter)
    if team_filter:
        qa_evals = qa_evals.filter(agent__team=team_filter)
    if week_start:
        qa_evals = qa_evals.filter(interaction_date__gte=week_start)
    if week_end:
        qa_evals = qa_evals.filter(interaction_date__lte=week_end)
    
    # Agrupar por agente y calcular el promedio de total_final_score
    ranking = qa_evals.values('agent__agent_name').annotate(avg_qa=Avg('total_final_score')).order_by('-avg_qa')
    
    context = {
        'ranking': ranking,
        'selected_agent': agent_filter,
        'selected_team': team_filter,
        'week_start': week_start,
        'week_end': week_end,
    }
    return render(request, 'dashboard/qa_ranking.html', context)