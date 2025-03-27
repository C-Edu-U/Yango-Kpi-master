from django.db import models

class Agent(models.Model):
    operator_login = models.CharField(max_length=50, primary_key=True)
    agent_name = models.CharField(max_length=100, unique=True)
    team = models.CharField(max_length=100)

    def __str__(self):
        return self.agent_name

class WeeklyMetrics(models.Model):
    operator_login = models.ForeignKey(Agent, on_delete=models.CASCADE)
    segment = models.CharField(max_length=50)
    week_start = models.DateField()
    week_end = models.DateField()
    sessions_cnt = models.IntegerField()
    actions_cnt = models.IntegerField()
    action_close_cnt = models.IntegerField()
    productivity = models.DecimalField(max_digits=10, decimal_places=2)
    AHT_sec = models.IntegerField()
    SL_session_duration = models.DecimalField(max_digits=5, decimal_places=2)
    ratio_close_any = models.DecimalField(max_digits=5, decimal_places=2)
    closed_sessions_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    CSAT_cnt = models.IntegerField()
    CSAT_avg = models.DecimalField(max_digits=5, decimal_places=2)
    worktime_mins = models.IntegerField()
    postcall_avg_sec = models.IntegerField()
    OCC = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = (('operator_login', 'segment', 'week_start', 'week_end'),)
        # Esto asegura que no se registren duplicados para cada combinación de agente, segmento y semana.

    def __str__(self):
        return f"{self.operator_login} - {self.segment} ({self.week_start} to {self.week_end})"

class QAEvaluation(models.Model):
    evaluation_key = models.CharField(max_length=100, primary_key=True)
    priority = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    # Actualizamos la relación para que referencie al campo 'agent_name'
    agent = models.ForeignKey(
        Agent, 
        on_delete=models.CASCADE, 
        to_field='agent_name', 
        related_name="qa_evaluations"
    )
    interaction_date = models.DateTimeField()
    # Para el supervisor, se puede hacer lo mismo si se desea referenciar por nombre
    supervisor = models.ForeignKey(
        Agent, 
        on_delete=models.SET_NULL, 
        null=True, 
        to_field='agent_name', 
        related_name="supervisor_evaluations"
    )
    status = models.CharField(max_length=50)
    updated = models.DateTimeField()
    total_final_score = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.evaluation_key
