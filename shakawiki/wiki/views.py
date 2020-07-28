from core.views import BaseTemplateView


class TopView(BaseTemplateView):

    template_name = "wiki/top.html"

    def get(self, request, **kwargs):
        context = {}
        return self.render_to_response(context)
