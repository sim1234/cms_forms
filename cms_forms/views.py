from cms.plugin_rendering import ContentRenderer
from cms.utils.plugins import get_plugins
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views import View
from sekizai.context import SekizaiContext


def get_plugin(request, model, form_pk):
    form_obj = get_object_or_404(model, pk=form_pk)
    for plugin in get_plugins(request, form_obj.placeholder, None):
        if form_pk == plugin.pk:
            return plugin
    raise Http404()


class BaseFormSubmissionView(View):
    model = None

    def get_plugin(self, request, form_pk):
        plugin = get_plugin(request, self.model, form_pk)
        _, plugin_pl = plugin.get_plugin_instance()
        plugin.render_inner_only = True
        return plugin

    def render(self, request, plugin):
        context = SekizaiContext({"request": request, "inner_only": True})
        content = ContentRenderer(request).render_plugin(plugin, context)
        return HttpResponse(content)

    def get(self, request, form_pk):
        plugin = self.get_plugin(request, form_pk)
        return self.render(request, plugin)

    def post(self, request, form_pk):
        plugin = self.get_plugin(request, form_pk)
        form = plugin.build_form_cls()(request.POST, request.FILES)
        plugin.form = form
        if form.is_valid():
            print("OK")  # TODO
        else:
            print("NO", form.errors)
        return self.render(request, plugin)
