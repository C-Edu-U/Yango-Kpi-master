from django import forms
from .models import Agent, QAEvaluation

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['operator_login', 'agent_name', 'team']

class QAEvaluationCommentsForm(forms.ModelForm):
    class Meta:
        model = QAEvaluation
        fields = ['ticket', 'comments_on_interaction']
        widgets = {
            'ticket': forms.URLInput(attrs={'placeholder': 'https://'}),
            'comments_on_interaction': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Ingrese comentarios sobre la interacción...'}),
        }
