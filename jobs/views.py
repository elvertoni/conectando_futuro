from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Job


class JobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 12

    def get_queryset(self):
        queryset = Job.objects.active()

        # Capture GET parameters
        city = self.request.GET.get('city')
        job_type = self.request.GET.get('job_type')
        area = self.request.GET.get('area')

        # Apply filters
        if city:
            queryset = queryset.filter(city__iexact=city)
        if job_type:
            queryset = queryset.filter(job_type=job_type)
        if area:
            queryset = queryset.filter(area__iexact=area)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve unique cities and areas from active vacancies
        active_jobs = Job.objects.active()
        context['cities'] = active_jobs.values_list('city', flat=True).distinct().order_by('city')
        context['areas'] = active_jobs.values_list('area', flat=True).distinct().order_by('area')
        context['job_types'] = Job.JOB_TYPE_CHOICES

        # Maintain form field selections
        context['selected_city'] = self.request.GET.get('city', '')
        context['selected_job_type'] = self.request.GET.get('job_type', '')
        context['selected_area'] = self.request.GET.get('area', '')

        # Preserve query string for pagination links
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        context['queries'] = query_params.urlencode()

        return context


class JobDetailView(LoginRequiredMixin, DetailView):
    model = Job
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'

    def get_queryset(self):
        # Limit details to active jobs for regular users
        return Job.objects.active()
