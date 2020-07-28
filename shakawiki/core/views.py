from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView


class BaseTemplateView(TemplateView):
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    context['cache_key'] = settings.VERSION_ID

    return context

  def render_to_response(self, context, response_kwargs={}):
    context = self.get_context_data(**context)
    return super().render_to_response(context, **response_kwargs)
