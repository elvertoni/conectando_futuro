from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect
from django.db import transaction
import json
import os

from .models import Resume
from .forms import ResumeForm, EducationForm, WorkExperienceForm
from .services import generate_pdf, WEASYPRINT_AVAILABLE

class ResumeWizardView(LoginRequiredMixin, TemplateView):
    template_name = 'resume/resume_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            resume = Resume.objects.prefetch_related('education', 'experience').get(user=self.request.user)
            context['resume'] = resume
            context['education_list'] = resume.education.all()
            context['experience_list'] = resume.experience.all()
            context['skills_str'] = ", ".join(resume.skills)
        except Resume.DoesNotExist:
            context['resume'] = None
            context['education_list'] = []
            context['experience_list'] = []
            context['skills_str'] = ""
        return context

class ResumeSubmitView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            
            objective = data.get('objective', '').strip()
            skills = data.get('skills', [])
            languages = data.get('languages', [])
            education_data = data.get('education', [])
            experience_data = data.get('experience', [])
            
            # 1. Validate Resume Objective
            resume_form = ResumeForm(data={'professional_objective': objective})
            if not resume_form.is_valid():
                return JsonResponse({'status': 'error', 'message': list(resume_form.errors.values())[0][0]}, status=400)
                
            # 2. Validate Education items
            education_forms = []
            for item in education_data:
                try:
                    start_year = int(item.get('start_year')) if item.get('start_year') else None
                except ValueError:
                    start_year = None
                try:
                    end_year = int(item.get('end_year')) if item.get('end_year') else None
                except ValueError:
                    end_year = None

                form_data = {
                    'institution': item.get('institution', '').strip(),
                    'course': item.get('course', '').strip(),
                    'level': item.get('level'),
                    'status': item.get('status'),
                    'start_year': start_year,
                    'end_year': end_year
                }
                form = EducationForm(data=form_data)
                if not form.is_valid():
                    error_msg = list(form.errors.values())[0][0]
                    return JsonResponse({
                        'status': 'error',
                        'message': f"Erro na formação '{form_data['course']}': {error_msg}"
                    }, status=400)
                education_forms.append(form)
                
            # 3. Validate Experience items
            experience_forms = []
            for item in experience_data:
                form_data = {
                    'role': item.get('role', '').strip(),
                    'company': item.get('company', '').strip(),
                    'description': item.get('description', '').strip(),
                    'start_date': item.get('start_date'),
                    'end_date': item.get('end_date') or None
                }
                form = WorkExperienceForm(data=form_data)
                if not form.is_valid():
                    error_msg = list(form.errors.values())[0][0]
                    return JsonResponse({
                        'status': 'error',
                        'message': f"Erro na experiência '{form_data['role']}': {error_msg}"
                    }, status=400)
                experience_forms.append(form)

            # Atomic transaction to guarantee DB consistency
            with transaction.atomic():
                resume, created = Resume.objects.get_or_create(user=request.user)
                if not created:
                    resume.version += 1
                
                resume.professional_objective = objective
                resume.skills = [s.strip() for s in skills if s.strip()]
                
                cleaned_languages = []
                for lang in languages:
                    l_name = lang.get('language', '').strip()
                    l_lvl = lang.get('level', '').strip()
                    if l_name and l_lvl:
                        cleaned_languages.append({'language': l_name, 'level': l_lvl})
                resume.languages = cleaned_languages
                resume.save()
                
                # Delete existing records to replace with new set
                resume.education.all().delete()
                resume.experience.all().delete()
                
                # Save nested items
                for form in education_forms:
                    education = form.save(commit=False)
                    education.resume = resume
                    education.save()
                    
                for form in experience_forms:
                    experience = form.save(commit=False)
                    experience.resume = resume
                    experience.save()
            
            # Generate PDF using WeasyPrint
            generate_pdf(resume.id)
            
            return JsonResponse({
                'status': 'success',
                'redirect_url': '/curriculo/download/'
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

class ResumeDownloadView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            resume = Resume.objects.prefetch_related('education', 'experience').get(user=request.user)
        except Resume.DoesNotExist:
            return redirect('resume:wizard')
            
        # Download PDF as FileResponse
        if request.GET.get('download') == '1':
            if resume.pdf_file and os.path.exists(resume.pdf_file.path):
                # Clean name for safe filename download
                safe_name = request.user.full_name.replace(" ", "_") if request.user.full_name else "curriculo"
                return FileResponse(
                    open(resume.pdf_file.path, 'rb'), 
                    content_type='application/pdf',
                    filename=f'curriculo_{safe_name}.pdf'
                )
            else:
                # If WeasyPrint failed, return printable HTML fallback
                context = {
                    'resume': resume,
                    'user': request.user,
                    'education_list': resume.education.all(),
                    'experience_list': resume.experience.all(),
                    'print_fallback': True,
                }
                return render(request, 'resume/pdf_template.html', context)
                
        # Render the success page
        context = {
            'resume': resume,
            'weasyprint_available': WEASYPRINT_AVAILABLE,
        }
        return render(request, 'resume/resume_download.html', context)
