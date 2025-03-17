from django.contrib import admin
from .models import Agent, WeeklyMetrics, QAEvaluation

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('operator_login', 'agent_name', 'team')

@admin.register(WeeklyMetrics)
class WeeklyMetricsAdmin(admin.ModelAdmin):
    list_display = ('operator_login', 'segment', 'week_start', 'week_end')

@admin.register(QAEvaluation)
class QAEvaluationAdmin(admin.ModelAdmin):
    list_display = ('evaluation_key', 'priority', 'type', 'agent', 'interaction_date', 'supervisor', 'status', 'updated', 'total_final_score')
