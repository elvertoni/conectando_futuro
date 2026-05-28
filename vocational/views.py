from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse
from django.shortcuts import redirect
from django.db.models import Q
import json

from .models import Question, VocationalProfile
from .services import analyze_profile
from jobs.models import Job

class QuestionnaireView(LoginRequiredMixin, TemplateView):
    template_name = 'vocational/questionnaire.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Prefetch options to prevent N+1 queries
        context['questions'] = Question.objects.prefetch_related('options').all().order_by('order', 'id')
        return context

class SubmitAnswersView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            answers = data.get('answers', {})
            
            # Simple validation: ensure answers is a dictionary and not empty
            if not isinstance(answers, dict) or not answers:
                return JsonResponse({'status': 'error', 'message': 'Respostas inválidas.'}, status=400)
                
            # Create or update VocationalProfile
            profile, created = VocationalProfile.objects.get_or_create(user=request.user)
            profile.answers = answers
            profile.save()
            
            # Run analysis (either calls API or runs local fallback)
            analyze_profile(profile.id)
            
            return JsonResponse({
                'status': 'success', 
                'redirect_url': '/vocational/resultado/'
            })
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'JSON inválido.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

class VocationalResultView(LoginRequiredMixin, TemplateView):
    template_name = 'vocational/result.html'

    def get(self, request, *args, **kwargs):
        # Redirect users who haven't completed the questionnaire yet
        try:
            profile = request.user.vocational_profile
            if not profile.profile_summary:
                return redirect('vocational:questionnaire')
        except VocationalProfile.DoesNotExist:
            return redirect('vocational:questionnaire')
            
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.vocational_profile
        context['profile'] = profile
        
        # Filter jobs based on suggested vocational areas
        suggested = profile.suggested_areas
        recommended_jt = profile.recommended_job_types
        
        active_jobs = Job.objects.active()
        
        # Build query for matching areas (case-insensitive)
        area_queries = Q()
        if suggested:
            for area in suggested:
                area_queries |= Q(area__icontains=area)
                
        jobs = active_jobs.filter(area_queries)
        
        # If no jobs match, fallback to match by recommended job types
        if not jobs.exists() and recommended_jt:
            jt_queries = Q()
            for jt in recommended_jt:
                jt_queries |= Q(job_type=jt)
            jobs = active_jobs.filter(jt_queries)
            
        # Get up to 6 recommended jobs
        context['recommended_jobs'] = jobs.distinct()[:6]
        
        return context
