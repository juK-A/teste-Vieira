from django import forms
from tarefas.models import Activities

class ActivitiesModelForm(forms.ModelForm):
    class Meta:
        model = Activities
        fields = ['name_activity', 'description', 'responsible', 'done', 'due_date']
        labels = {
            'name_activity': 'Nome da Atividade',
            'description': 'Descrição',
            'responsible': 'Responsável',
            'done': 'Concluído',
            'due_date': 'Prazo',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows':10}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }