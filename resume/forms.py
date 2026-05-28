from django import forms
from .models import Resume, Education, WorkExperience
from datetime import date

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['professional_objective']
        widgets = {
            'professional_objective': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Descreva seu objetivo profissional de forma clara e objetiva (ex: Busco oportunidade de Jovem Aprendiz na área administrativa para desenvolver minhas habilidades e contribuir com a equipe).'
            })
        }

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'course', 'level', 'status', 'start_year', 'end_year']

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        start_year = cleaned_data.get('start_year')
        end_year = cleaned_data.get('end_year')

        current_year = date.today().year

        if start_year:
            if start_year < 1990 or start_year > current_year + 5:
                self.add_error('start_year', 'Ano de início inválido.')

        if status == 'concluido' and not end_year:
            self.add_error('end_year', 'Ano de conclusão é obrigatório para cursos concluídos.')

        if start_year and end_year:
            if end_year < start_year:
                self.add_error('end_year', 'O ano de conclusão não pode ser anterior ao ano de início.')

        return cleaned_data

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['role', 'company', 'description', 'start_date', 'end_date']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                self.add_error('end_date', 'A data de término não pode ser anterior à data de início.')

        return cleaned_data
