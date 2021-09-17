from django.views.generic import TemplateView
from .services import get_tutorial
from django.shortcuts import render

class GetTutorial(TemplateView):
    template_name = 'tutorial.html'
    def get_context_data(self, *args, **kwargs):
        context = {
            'tutorial' : get_tutorial(self),
        }
        return context

class HomePageView(TemplateView):
    template_name = 'search.html'

class SearchResultsView(TemplateView):
    def get_context_data(self, *args, **kwargs):
        context = {
            'tutorial' : get_tutorial(self),
        }
        return context
    template_name = 'tutorial.html'