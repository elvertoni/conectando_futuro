from django.views.generic import TemplateView

class DesignDraftView(TemplateView):
    template_name = 'core/design_draft.html'
