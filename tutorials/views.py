from django.views.generic import TemplateView
from .services import get_tutorial

class GetTutorial(TemplateView):
    template_name = 'tutorial.html'
    def get_context_data(self, *args, **kwargs):
        context = {
            'tutorial' : get_tutorial(self),
        }
        return context