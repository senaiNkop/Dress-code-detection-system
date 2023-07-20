from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from .models import DataAnalysis
# Create your views here.


COMPANY_NAME = 'SENAI'


class DataAnalysisView(TemplateView):

    def setup(self, request, *args, **kwargs):
        super(DataAnalysisView, self).setup(request, args, kwargs)
        self.template_name = f"data_analysis/children/{kwargs['project_name']}.html"

    def get_context_data(self, **kwargs):
        context = super(DataAnalysisView, self).get_context_data(**kwargs)

        data_analysis = get_object_or_404(DataAnalysis, slug=kwargs['project_name'])

        context['data'] = data_analysis
        context['company_name'] = COMPANY_NAME

        return context



